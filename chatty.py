import sys
import os
import pkgutil

# --- FIX CRITIC PENTRU DLL-URI (Executat IMEDIAT) ---
if getattr(sys, 'frozen', False):
    os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
# ---------------------------------------------------

from PyQt6.QtCore import QUrl, Qt, pyqtSignal, QObject
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Schimbăm modul de import pentru pynput ca să fim ultra-expliciți
try:
    from pynput.keyboard import GlobalHotkeys
except ImportError:
    # Fallback în caz că structura internă a pynput este recalcitrantă
    from pynput.keyboard._win32 import KeyCode
    from pynput.keyboard import GlobalHotkeys

class HotkeySignal(QObject):
    trigger = pyqtSignal()

class ChattyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatty - WhatsApp Portable Edition")
        self.resize(1100, 800)

        # 1. LOGICA DE PORTABILITATE
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.data_path = os.path.join(self.base_path, "chatty_data")
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # 2. CONFIGURARE BROWSER
        self.browser = QWebEngineView()
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        
        profile = self.browser.page().profile()
        profile.setPersistentStoragePath(self.data_path)
        profile.setHttpUserAgent(ua)
        
        self.browser.setUrl(QUrl("https://web.whatsapp.com"))
        self.setCentralWidget(self.browser)

        # 3. INITIALIZARE TRAY ȘI HOTKEYS
        self.setup_tray()
        self.setup_hotkeys()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = os.path.join(self.base_path, "icon.ico")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
        
        menu = QMenu()
        show_action = QAction("Afișează Chatty (Ctrl+Alt+W)", self)
        quit_action = QAction("Închide de tot (Exit)", self)
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
        
        # Folosim direct clasa importată mai sus
        self.kp_listener = GlobalHotkeys({
            '<ctrl>+<alt>+w': self.hotkey_sig.trigger.emit
        })
        self.kp_listener.start()

    def toggle_window(self):
        if self.isVisible() and self.windowState() != Qt.WindowState.WindowMinimized:
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()
            self.raise_()

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