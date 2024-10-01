// src/components/TopTransactionsTable.jsx

import React, { useEffect, useState } from 'react';
import './TopTransactionsTable.css';

const TopTransactionsTable = () => {
    const [transactions, setTransactions] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [filteredTransactions, setFilteredTransactions] = useState([]);

    useEffect(() => {
        const fetchTransactionData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/transactions');
                const result = await response.json();
                setTransactions(result);
                setFilteredTransactions(result); // Initially show all data
            } catch (error) {
                console.error("Error fetching transaction data:", error);
            }
        };

        fetchTransactionData();
    }, []);

    // Handle search input change
    const handleSearch = (event) => {
        const value = event.target.value.toLowerCase();
        setSearchTerm(value);
        const filtered = transactions.filter((transaction) =>
            transaction.user_id.toLowerCase().includes(value) || 
            new Date(transaction.timestamp).toLocaleDateString().toLowerCase().includes(value) ||
            transaction.transaction_type.toLowerCase().includes(value) ||
            transaction.amount.toString().includes(value) ||
            transaction.status.toLowerCase().includes(value)
        );
        setFilteredTransactions(filtered);
    };

    return (
        <div className="top-transactions-table">
            <div className="table-header">
                <h2>Top Transactions Details</h2>
                <input 
                    type="text" 
                    placeholder="Search..." 
                    value={searchTerm}
                    onChange={handleSearch}
                    className="search-input"
                />
            </div>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Date</th>
                            <th>Method</th>
                            <th>Amount</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredTransactions.map((transaction, index) => (
                            <tr key={index}>
                                <td>{transaction.user_id}</td>
                                <td>{new Date(transaction.timestamp).toLocaleDateString()}</td>
                                <td>{transaction.transaction_type}</td>
                                <td>${transaction.amount.toFixed(2)}</td>
                                <td>{transaction.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TopTransactionsTable;
