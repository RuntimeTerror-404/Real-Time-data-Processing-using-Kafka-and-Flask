// src/components/TopCompaniesCard.jsx

import React, { useEffect, useState } from 'react';
import './TopCompaniesCard.css'; // Import the CSS file
import Amex from "../avatars/amex.jpg";
import Visa from "../avatars/visa.jpg";
import Mastercard from "../avatars/mastercard.png";
import FIS from "../avatars/fis_2.png";
import Broadridge from "../avatars/broadridge.jpg";
import Finastra from "../avatars/finastra.png";
import Western from "../avatars/western.png";

const TopCompaniesCard = () => {
    const [transactions, setTransactions] = useState([]);
    const organizations = [
        { name: 'American Express', avatar: Amex }, 
        { name: 'VISA', avatar: Visa }, 
        { name: 'Mastercard', avatar: Mastercard }, 
        { name: 'FIS', avatar: FIS }, 
        { name: 'Broadridge', avatar: Broadridge }, 
        { name: 'Finastra', avatar: Finastra }, 
        { name: 'Western Union', avatar: Western }
    ];

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

    // Prepare data for the table
    const aggregateAmountsByOrganization = (transactions) => {
        const organizationTotals = {};

        transactions.forEach(item => {
            const organizationName = item.organization; // Use the 'organization' field from the response
            if (organizations.some(org => org.name === organizationName)) {
                if (!organizationTotals[organizationName]) {
                    organizationTotals[organizationName] = 0; // Initialize if not present
                }
                organizationTotals[organizationName] += item.amount; // Sum up the amounts for the organization
            }
        });

        return organizationTotals;
    };

    const organizationTotals = aggregateAmountsByOrganization(transactions);

    return (
        <div className="top-companies-card">
            <h2>Top Financial Transaction Processing Organizations</h2>
            <table>
                <thead>
                    <tr>
                        <th>Organization Name</th>
                        <th>Total Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {organizations.map(({ name, avatar }) => (
                        <tr key={name}>
                            <td>
                                <img src={avatar} alt={`${name} logo`} className="avatar" />
                                {name}
                            </td>
                            <td>${organizationTotals[name]?.toFixed(2) || 0}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TopCompaniesCard;
