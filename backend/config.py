import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'your-password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'real_time_data')
    KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'localhost:9092')
