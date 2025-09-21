import React, { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [serviceName, setServiceName] = useState('openai');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (!serviceName || !username || !password) {
      setMessage('All fields are required.');
      return;
    }

    if (window.electronAPI) {
      const result = await window.electronAPI.saveCredential(serviceName, username, password);
      if (result.success) {
        setMessage(`Successfully saved credentials for ${username} on ${serviceName}!`);
        setUsername(''); // Clear fields after saving
        setPassword('');
      } else {
        setMessage(`Error: ${result.error}`);
      }
    } else {
      setMessage('Error: Not running in Electron environment.');
    }
  };

  return (
    <div>
      <h1>Settings</h1>

      <div className="settings-section">
        <h2>AI Service Credential Management</h2>
        <div className="warning-box">
          <strong>Security Warning:</strong> You are about to enter sensitive credentials. These will be stored securely in your operating system's native keychain or credential vault and will only be used for logging into AI services via browser automation on your local machine.
        </div>
        <form onSubmit={handleSubmit} className="credential-form">
          <div className="form-group">
            <label htmlFor="service">Service</label>
            <select id="service" value={serviceName} onChange={(e) => setServiceName(e.target.value)}>
              <option value="openai">OpenAI (ChatGPT)</option>
              <option value="google">Google (Gemini)</option>
              <option value="anthropic">Anthropic (Claude)</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="username">Username / Email</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your login username or email"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit">Save Credential</button>
        </form>
        {message && <p className="message">{message}</p>}
      </div>

    </div>
  );
};

export default Settings;
