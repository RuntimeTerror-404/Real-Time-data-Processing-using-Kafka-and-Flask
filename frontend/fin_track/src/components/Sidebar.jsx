import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css'; // Assuming you have a separate Sidebar.css for styling

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>Fin-Track</h2>
      <ul>
        <li><Link to="/dashboard">Dashboard</Link></li>
        {/* Add more navigation links */}
      </ul>
    </div>
  );
}

export default Sidebar;
