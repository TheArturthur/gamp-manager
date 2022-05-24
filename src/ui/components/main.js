const {app, BrowserWindow} = require("electron")
require('electron-reload')(__dirname)

function createWindow(file) {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600
    })

    mainWindow.loadFile(file)
}

app.whenReady().then(() => {
    createWindow()
})
