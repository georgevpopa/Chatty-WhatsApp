# 📱 Chatty - WhatsApp Portable Edition

![Chatty Screenshot](WhatsApp%20Portable%20Edition.png)

---

### **Stable Version:** v1.1.5 | **Status:** Production Stable 🚀

**Chatty** is an ultra-lightweight WhatsApp Web client designed for portability and productivity. Unlike the official app, Chatty requires no installation and offers full control through a global hotkey.

---

## ✨ Key Features

* 🚀 **True Portability:** All session data (cookies, cache) is stored in the local `chatty_data` folder. You can take the folder on a USB stick and stay logged in on any other PC.

* ⌨️ **Global Hotkey (`Ctrl + Alt + W`):** Show or hide the window instantly, regardless of which application you're in.

* 🥷 **Stealth Mode (System Tray):** The app runs discreetly next to the clock. Closing the window only hides it to the Tray, keeping the connection active.

* 📉 **Low Resource Usage:** Optimized to use less RAM than a regular browser tab.

---

## 🚀 How to Use

1. **Go to Releases:** Download the latest `Chatty.exe`.

2. **Launch:** Run the application (no Administrator rights required).

3. **Login:** Scan the QR code with your phone once.

4. **Use:** Press **`Ctrl + Alt + W`** to quickly bring up the chat.

---

## 🛠️ Technical Details (For Developers)

If you want to modify or run the project from source, you need **Python 3.10+**.

### 📂 Project Structure
```plaintext
📂 Chatty/
├── 📂 .github/workflows/   # Build Automation (GitHub Actions)
├── 📄 chatty.py            # Main source code (PyQt6 + keyboard)
├── 📄 requirements.txt     # Project dependencies
├── 🖼️ icon.ico             # Application icon
└── 📄 README.md            # This documentation
```

### ⌨️ Install Dependencies

```powershell
pip install -r requirements.txt
```

### 🔨 Manual Build (Local):

```powershell
pyinstaller --onefile --noconsole --name "Chatty" --icon="icon.ico" chatty.py
```

---

## 📝 Changelog

### v1.1.5 (Latest)
- Library migration: Switched from pynput to keyboard for improved stability in portable mode.
- DLL Hell fix: Implemented path forcing logic for Qt6 DLLs.
- UI optimization: Added `raise_()` function to ensure window comes to foreground on Hotkey press.

### v1.0.0
- Initial release with PyQt6 WebEngine.
- Implemented local `chatty_data` session folder.

---

## 🛡️ Security & Privacy

* **No Cloud:** Chatty does not store your data on any proprietary server. Everything stays in your local folder.
* **Open Source:** You can audit the source code at any time.
* **Sysadmin Note:** Make sure you have `chatty_data` in `.gitignore` to protect your session privacy!

---

## 👤 Author

**George Popa**
* [GitHub Profile](https://github.com/georgevpopa)

## 📄 License

This project is offered under the **MIT** license. You can modify and distribute it freely.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=georgevpopa/Chatty-WhatsApp&type=Date)](https://star-history.com/#georgevpopa/Chatty-WhatsApp&Date)
