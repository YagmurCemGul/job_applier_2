const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const axios = require('axios');

// Define the base URL for the backend API
const BACKEND_URL = 'http://127.0.0.1:8000';

function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.loadURL(
    isDev
      ? 'http://localhost:3000'
      : `file://${path.join(__dirname, '../build/index.html')}`
  );

  if (isDev) {
    win.webContents.openDevTools();
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// --- IPC Handlers for Frontend-Backend Communication ---

ipcMain.handle('get-app-version', () => {
    return app.getVersion();
});

ipcMain.handle('save-credential', async (event, serviceName, username, password) => {
  console.log(`Received save-credential event for service: ${serviceName}`);
  try {
    const response = await axios.post(`${BACKEND_URL}/api/settings/credential`, {
      service_name: serviceName,
      username: username,
      password: password,
    });
    console.log('Backend response:', response.data);
    return { success: true, data: response.data };
  } catch (error) {
    const errorMessage = error.response ? error.response.data.detail : 'Network error or backend is not running.';
    console.error('Failed to save credential via backend:', errorMessage);
    return { success: false, error: errorMessage };
  }
});
