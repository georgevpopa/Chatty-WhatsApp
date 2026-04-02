import sys
import os
from PyQt6.QtCore import QUrl, Qt, pyqtSignal, QObject
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView
from pynput import keyboard

class HotkeySignal(QObject):
    trigger = pyqtSignal()

class ChattyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatty - WhatsApp Portable Edition")
        self.resize(1100, 800)

        # Configurare folder portabil pentru date
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Redenumit în chatty_data pentru consistență
        self.data_path = os.path.join(self.base_path, "chatty_data")
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # Configurare Browser Engine
        self.browser = QWebEngineView()
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        self.browser.page().profile().setPersistentStoragePath(self.data_path)
        self.browser.page().profile().setHttpUserAgent(ua)
        self.browser.setUrl(QUrl("https://web.whatsapp.com"))
        self.setCentralWidget(self.browser)

        # System Tray & Hotkeys
        self.setup_tray()
        self.setup_hotkeys()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        # Folosește iconița de sistem dacă icon.ico lipsește
        self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_DialogNoButton))
        
        menu = QMenu()
        show_action = QAction("Open Chatty (Ctrl+Alt+W)", self)
        quit_action = QAction("Exit", self)
        
        show_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(QApplication.instance().quit)
        
        menu.addAction(show_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_click)

    def setup_hotkeys(self):
        self.hotkey_sig = HotkeySignal()
        self.hotkey_sig.trigger.connect(self.toggle_window)
        self.kp_listener = keyboard.GlobalHotkeys({'<ctrl>+<alt>+w': self.hotkey_sig.trigger.emit})
        self.kp_listener.start()

    def toggle_window(self):
        if self.isVisible() and self.windowState() != Qt.WindowState.WindowMinimized:
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_window()

    def changeEvent(self, event):
        if event.type() == event.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMinimized:
                self.hide()
                event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    chatty = ChattyApp()
    chatty.show()
    sys.exit(app.exec())