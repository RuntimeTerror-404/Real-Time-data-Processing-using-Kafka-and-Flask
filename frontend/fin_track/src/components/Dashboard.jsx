// src/components/Dashboard.jsx

import React from 'react';
import StatisticalGraph from './StatisticalGraph';
import TopCompaniesCard from './TopCompaniesCard';
import TopTransactionsTable from './TopTransactionsTable';
import './Dashboard.css'; // Import the CSS file for styling
import { Colors } from 'chart.js';

const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <h1>Welcome to the <span style={{color: "red"}}>Dashboard!</span></h1>

      {/* Container for the first two sub-components */}
      <div className="top-section">
        <div className="graph-section">
          <StatisticalGraph />
        </div>
        <div className="companies-card-section">
          <TopCompaniesCard />
        </div>
      </div>

      {/* Third sub-component (placed at the bottom) */}
      <div className="transactions-table-section">
        <TopTransactionsTable />
      </div>
    </div>
  );
};

export default Dashboard;
