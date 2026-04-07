# PatchCraft Server – Diff, patch og retteværktøj (Streamlit)

**PatchCraft Server** er en webbaseret app til at sammenligne to tekstfiler, generere unified diffs, rapporter med præcise linjenumre og et Python-script der kan omdannes til en selvstændig `.exe`-fil.

## 🚀 Live demo (hvis du hoster)
[https://patchcraft-server.streamlit.app](https://patchcraft-server.streamlit.app) *(eksempel – din egen URL)*

## ✨ Funktioner
- Upload to filer (alle tekstformater: `.py`, `.txt`, `.md`, `.nfo`, `.json`, `.c`, `.html`, `.sh`, m.fl.)
- Visuel farvet diff preview
- Download unified patch-fil (`.patch`)
- Download diff rapport med linjenumre (manuel rettelse)
- Download Python-script der anvender patchen – kan konverteres til `.exe` med PyInstaller

## 🛠️ Installation (lokal kørsel)
```bash
git clone https://github.com/dit-brugernavn/PatchCraft-Server.git
cd PatchCraft-Server
pip install streamlit
streamlit run app.py
