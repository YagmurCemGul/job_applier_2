const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object.
contextBridge.exposeInMainWorld('electronAPI', {
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),

  // API Key Management
  saveApiKey: (serviceName, apiKey) => ipcRenderer.invoke('save-api-key', serviceName, apiKey),

  // We can expose other backend functions here as we build them.
  // For example:
  // saveProfile: (data) => ipcRenderer.invoke('save-profile', data),
  // startApplication: (jobId) => ipcRenderer.invoke('start-application', jobId),
});
