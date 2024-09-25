const { app, BrowserWindow, ipcMain } = require('electron');
const zmq = require('zeromq');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 400,
    height: 400,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });
  mainWindow.loadFile('index.html');
}

app.whenReady().then(createWindow);

ipcMain.on('send-data', async (event, data) => {
  const sock = new zmq.Request();
  await sock.connect("tcp://localhost:5555");

  console.log("Sending:", data);
  await sock.send(JSON.stringify(data));

  const [result] = await sock.receive();
  console.log("Received:", result.toString());
});

