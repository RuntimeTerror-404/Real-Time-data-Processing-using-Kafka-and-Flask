from kafka import KafkaConsumer, KafkaProducer
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from collections import defaultdict

# Load environment variables
load_dotenv()

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['Transactions']  # Use Transactions database
collection = db['Records']    # Use Records collection

# Kafka setup
KAFKA_SERVER = 'localhost:9092'
INPUT_TOPIC = 'real_time_data'
OUTPUT_TOPIC = 'transaction_analytics'

# Country code mapping for validation
country_codes = {
    "India": "+91",
    "USA": "+1",
    "Canada": "+1",
    # Add more countries as needed
}

# Set up the Kafka consumer
consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',
    group_id='transaction-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Set up the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize analytics variables
transaction_count = 0
total_amount = 0.0
amount_by_country = defaultdict(float)
transaction_counts_by_country = defaultdict(int)
unique_countries = set()  # Set to store unique country names
transaction_types = defaultdict(int)

# Initialize new analytics variables
monthly_transaction_counts = defaultdict(int)  # Monthly transaction counts
monthly_transaction_amounts = defaultdict(float)  # Monthly transaction amounts
top_organizations = defaultdict(int)  # Transaction counts by organization
daily_transaction_counts = defaultdict(int)  # Daily transaction counts
average_transaction_amounts = defaultdict(list)  # List of transaction amounts by country for averaging

def detect_anomalies(transaction):
    """Detect anomalies in transactions."""
    anomalies = []
    
    # Check CVV length
    if 'cvv' in transaction and (len(transaction['cvv']) < 3 or len(transaction['cvv']) > 3):
        anomalies.append("CVV length is invalid.")
    
    # Check for suspicious transactions
    if 'country_code' in transaction and 'country' in transaction:
        expected_country_code = country_codes.get(transaction['country'])
        if expected_country_code and expected_country_code != transaction['country_code']:
            anomalies.append(f"Suspicious transaction: country_code {transaction['country_code']} does not match country {transaction['country']}.")

    return anomalies

def process_transaction(transaction):
    """Process the transaction and perform analytics."""
    global transaction_count, total_amount




    
    if 'transaction_id' not in transaction:
        print("Missing transaction_id in the message, skipping this transaction.")
        return
    
    # Update aggregates
    if 'amount' in transaction:
        total_amount += transaction['amount']
        transaction_count += 1
        print(f"Total transactions: {transaction_count}, Total amount: {total_amount:.2f}")

        # Check for the country in the transaction
        country_name = transaction.get("country")
        if country_name:
            # Only add the country if it doesn't exist in the unique_countries set
            if country_name not in unique_countries:
                unique_countries.add(country_name)  # Add country to unique countries
                print(f"Added new country: {country_name}")

            # Update amount by country
            amount_by_country[country_name] += transaction['amount']
            transaction_counts_by_country[country_name] += 1  # Count transactions by country

        # Track monthly transactions
        transaction_date = transaction['timestamp'][:7]  # Get YYYY-MM format
        monthly_transaction_counts[transaction_date] += 1
        monthly_transaction_amounts[transaction_date] += transaction['amount']
        
        # Track daily transactions
        transaction_day = transaction['timestamp'][:10]  # Get YYYY-MM-DD format
        daily_transaction_counts[transaction_day] += 1

        # Track top organizations
        organization = transaction.get("organization", "Unknown")
        top_organizations[organization] += 1
        
        # Track average transaction amounts by country
        country_name = transaction.get("country")
        if country_name:
            average_transaction_amounts[country_name].append(transaction['amount'])

    # Detect anomalies
    anomalies = detect_anomalies(transaction)
    if anomalies:
        for anomaly in anomalies:
            print(anomaly)

    organization = transaction.get("organization", "Unknown")
    print(f"Processing transaction for organization: {organization}")
    
    # Prepare analytics data for sending to Kafka
    analytics_data = {
        "country": country_name,
        "total_transactions": transaction_counts_by_country[country_name],
        "total_amount": amount_by_country[country_name],
        "unique_countries": list(unique_countries),  # Send the unique countries
        "organization": organization,
        "timestamp": transaction.get("timestamp"),
    }

    # Sending processed data to another topic
    producer.send(OUTPUT_TOPIC, analytics_data)

def print_analytics():
    """Print the current analytics."""
    print("\nCurrent Analytics:")
    print(f"Total transactions processed: {transaction_count}")
    print(f"Total amount processed: {total_amount:.2f}")
    print("Total amount by country:")
    for country, amount in amount_by_country.items():
        print(f"  {country}: {amount:.2f}")
    print("Unique countries involved in transactions:")
    for country in unique_countries:
        print(f"  {country}")

    # Monthly transaction counts
    print("\nMonthly Transaction Counts:")
    for month, count in monthly_transaction_counts.items():
        print(f"  {month}: {count}")

    # Monthly transaction amounts
    print("\nMonthly Transaction Amounts:")
    for month, total in monthly_transaction_amounts.items():
        print(f"  {month}: {total:.2f}")

    # Top organizations
    print("\nTop Organizations by Transaction Volume:")
    for org, count in top_organizations.items():
        print(f"  {org}: {count}")

    # Daily transaction counts
    print("\nDaily Transaction Counts:")
    for day, count in daily_transaction_counts.items():
        print(f"  {day}: {count}")

    # Average transaction amounts by country
    print("\nAverage Transaction Amounts by Country:")
    for country, amounts in average_transaction_amounts.items():
        if amounts:
            average_amount = sum(amounts) / len(amounts)
            print(f"  {country}: {average_amount:.2f}")

def consume_messages():
    """Consume messages from Kafka and process them."""
    print(f"Listening to topic {INPUT_TOPIC}...")
    for message in consumer:
        transaction = message.value
        print(f"Received message: {transaction}")
        process_transaction(transaction)

        # Insert the transaction into MongoDB
        if 'transaction_id' in transaction:
            collection.insert_one(transaction)
            print(f"Transaction {transaction['transaction_id']} inserted into MongoDB.")
        else:
            print("Transaction not inserted into MongoDB due to missing transaction_id.")
        
        # Print analytics periodically
        if transaction_count % 10 == 0:  # Print analytics every 10 transactions
            print_analytics()

if __name__ == "__main__":
    consume_messages()
