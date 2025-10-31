import React from 'react';
import './Notification.css';

function Notification({ message, type = 'info', onClose }) {
  if (!message) return null;

  return (
    <div className={`notification notification-${type}`}>
      <div className="notification-content">
        <span>{message}</span>
        {onClose && (
          <button className="notification-close" onClick={onClose}>×</button>
        )}
      </div>
    </div>
  );
}

export default Notification;
