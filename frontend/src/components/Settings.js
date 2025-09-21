import React, { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [serviceName, setServiceName] = useState('openai');
  const [apiKey, setApiKey] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (!serviceName || !apiKey) {
      setMessage('Service name and API key are required.');
      return;
    }

    if (window.electronAPI) {
      const result = await window.electronAPI.saveApiKey(serviceName, apiKey);
      if (result.success) {
        setMessage(`Successfully saved API key for ${serviceName}!`);
        setApiKey(''); // Clear the key after saving
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
        <h2>LLM API Key Management</h2>
        <p>Your API keys are stored securely in your operating system's keychain.</p>
        <form onSubmit={handleSubmit} className="api-key-form">
          <div className="form-group">
            <label htmlFor="service">Service</label>
            <select id="service" value={serviceName} onChange={(e) => setServiceName(e.target.value)}>
              <option value="openai">OpenAI</option>
              <option value="google">Google</option>
              <option value="anthropic">Anthropic</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="api-key">API Key</label>
            <input
              id="api-key"
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your API key"
              required
            />
          </div>
          <button type="submit">Save API Key</button>
        </form>
        {message && <p className="message">{message}</p>}
      </div>

    </div>
  );
};

export default Settings;
