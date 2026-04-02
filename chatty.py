import sys
import os
import pkgutil

# --- FIX CRITIC PENTRU DLL-URI (Se execută înainte de orice import PyQt6) ---
# Rezolvă eroarea "QtCore: The specified procedure could not be found" 
# forțând aplicația să caute bibliotecile Qt în folderul temporar de dezarhivare.
if getattr(sys, 'frozen', False):
    os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
# --------------------------------------------------------------------------

from PyQt6.QtCore import QUrl, Qt, pyqtSignal, QObject
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView
from pynput import keyboard

# Clasă pentru comunicarea între firul de execuție al tastaturii și interfața grafică
class HotkeySignal(QObject):
    trigger = pyqtSignal()

class ChattyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatty - WhatsApp Portable Edition")
        self.resize(1100, 800)

        # 1. LOGICA DE PORTABILITATE
        # Identificăm locația executabilului pentru a salva datele lângă el
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Folder dedicat pentru cache și sesiune (nu va fi urcat pe GitHub)
        self.data_path = os.path.join(self.base_path, "chatty_data")
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # 2. CONFIGURARE ENGINE BROWSER
        self.browser = QWebEngineView()
        
        # User-Agent modern pentru a preveni blocarea de către WhatsApp Web
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        
        # Setăm profilul de stocare persistentă
        profile = self.browser.page().profile()
        profile.setPersistentStoragePath(self.data_path)
        profile.setHttpUserAgent(ua)
        
        self.browser.setUrl(QUrl("https://web.whatsapp.com"))
        self.setCentralWidget(self.browser)

        # 3. COMPONENTE DE UI (Tray & Hotkeys)
        self.setup_tray()
        self.setup_hotkeys()

    def setup_tray(self):
        """Configurează System Tray (iconița de lângă ceas)"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Încercăm să încărcăm iconița proprie, altfel punem una de sistem
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
        """Configurează scurtătura globală Ctrl+Alt+W"""
        self.hotkey_sig = HotkeySignal()
        self.hotkey_sig.trigger.connect(self.toggle_window)
        
        # Pornim ascultătorul de taste global
        self.kp_listener = keyboard.GlobalHotkeys({
            '<ctrl>+<alt>+w': self.hotkey_sig.trigger.emit
        })
        self.kp_listener.start()

    def toggle_window(self):
        """Funcție pentru a arăta/ascunde fereastra rapid"""
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
        """Minimizează fereastra direct în System Tray"""
        if event.type() == event.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMinimized:
                self.hide()
                event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Menține aplicația pornită chiar dacă fereastra principală este ascunsă
    app.setQuitOnLastWindowClosed(False)
    
    chatty = ChattyApp()
    chatty.show()
    
    sys.exit(app.exec())