# 📱 Chatty - WhatsApp Portable Edition

![Chatty Screenshot](WhatsApp%20Portable%20Edition.png)

---

### **Versiune Stabilă:** v1.1.5 | **Status:** Producție stabile 🚀

**Chatty** este un client WhatsApp Web ultra-ușor, conceput pentru portabilitate și productivitate. Spre deosebire de aplicația oficială, Chatty nu necesită instalare și oferă control total printr-o scurtătură globală (Hotkey).

---

## ✨ Caracteristici Principale

* 🚀 **Portabilitate Reală:** Toate datele sesiunii (cookies, cache) sunt salvate în folderul local `chatty_data`. Poți lua folderul pe un stick USB și vei rămâne logat pe orice alt PC.

* ⌨️ **Hotkey Global (`Ctrl + Alt + W`):** Ascunde sau afișează fereastra instantaneu, indiferent de aplicația în care te afli.

* 🥷 **Mod Stealth (System Tray):** Aplicația rulează discret lângă ceas. Închiderea ferestrei doar o ascunde în Tray, păstrând conexiunea activă.

* 📉 **Consum Redus de Resurse:** Optimizat pentru a ocupa mai puțină memorie RAM decât un tab de browser obișnuit.

---

## 🚀 Cum se utilizează

1.  **Mergi la secțiunea Releases:** Descarcă ultima variantă de `Chatty.exe`.

2.  **Lansare:** Rulează aplicația (nu necesită drepturi de Administrator).

3.  **Logare:** Scanează codul QR cu telefonul o singură dată.

4.  **Utilizare:** Folosește **`Ctrl + Alt + W`** pentru a apela rapid chat-ul.

---

## 🛠️ Detalii Tehnice (Pentru Developeri)

Dacă dorești să modifici sau să rulezi proiectul din surse, ai nevoie de **Python 3.10+**.

### 📂 Structura Proiectului
```plaintext
📂 Chatty/
├── 📂 .github/workflows/   # Automatizarea Build-ului (GitHub Actions)
├── 📄 chatty.py            # Codul sursă principal (PyQt6 + keyboard)
├── 📄 requirements.txt     # Dependențele proiectului
├── 🖼️ icon.ico             # Iconița aplicației
└── 📄 README.md            # Documentația curentă
```

⌨️ Instalare Dependențe

PowerShell
pip install -r requirements.txt

🔨 Compilare Manuală (Local):

PowerShell
pyinstaller --onefile --noconsole --name "Chatty" --icon="icon.ico" chatty.py

📝 Jurnal de Modificări (Changelog)
v1.1.5 (Cea mai recentă)
Migrare bibliotecă: S-a trecut de la pynput la keyboard pentru o stabilitate sporită în modul portabil.

Fix DLL Hell: S-a implementat logica de forțare a path-ului pentru DLL-urile Qt6.

Optimizare UI: S-a adăugat funcția raise_() pentru a asigura aducerea ferestrei în prim-plan la apăsarea Hotkey-ului.

v1.0.0
Lansare inițială cu PyQt6 WebEngine.

Implementare folder local de date chatty_data.

## 🛡️ Securitate și Confidențialitate
* **Fără Cloud:** Chatty nu stochează datele tale pe niciun server propriu. Totul rămâne în folderul tău local.
* **Open Source:** Poți audita codul sursă oricând.
* **Notă Sysadmin:** Asigură-te că ai `chatty_data` în `.gitignore` pentru a proteja intimitatea sesiunilor tale!

---

## 👤 Autor
**George Popa**
* [GitHub Profile](https://github.com/georgevpopa)

## 📄 Licență
Acest proiect este oferit sub licența **MIT**. Poți să-l modifici și să-l distribui gratuit.