// src/components/StatisticalGraph.jsx

import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js'; // Import Chart.js components

Chart.register(...registerables); // Register all necessary components

const StatisticalGraph = () => {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        const fetchTransactionData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/transactions'); // Update with your API endpoint
                const result = await response.json();
                setTransactions(result); // Store the fetched transaction data
            } catch (error) {
                console.error("Error fetching transaction data:", error);
            }
        };

        fetchTransactionData();
    }, []);

    // Prepare data for the chart
    const aggregateDataByYear = (transactions) => {
        const yearlyData = {};

        // Aggregate transaction amounts by year
        transactions.forEach(item => {
            const year = new Date(item.timestamp).getFullYear();
            if (year >= 2011) { // Only consider years from 2011 onward
                if (!yearlyData[year]) {
                    yearlyData[year] = 0; // Initialize if not present
                }
                yearlyData[year] += item.amount; // Sum up the amounts for the year
            }
        });

        return yearlyData;
    };

    // Get the aggregated data
    const yearlyData = aggregateDataByYear(transactions);

    // Prepare chart data
    const chartData = {
        labels: [], // Years from 2011 to present
        datasets: [
            {
                label: 'Total Amount Spent per Year',
                data: [], // Total amounts for each year
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            },
        ],
    };

    // Populate labels and data arrays
    for (let year = 2011; year <= new Date().getFullYear(); year++) {
        chartData.labels.push(year); // Add year to labels
        chartData.datasets[0].data.push(yearlyData[year] || 0); // Add total amount or 0 if no transactions for that year
    }

    return (
        <div style={{ padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 0 10px rgba(0,0,0,0.1)' }}>
            <h2>Total Amount Spent per Year</h2>
            <Bar data={chartData} />
        </div>
    );
};

export default StatisticalGraph;
