# PatchCraft – File Diff & Unified Patch Generator

**PatchCraft** er en 100% client-side webapp, der lader dig sammenligne to tekstfiler og skabe et **UNIX patch**, som kan transformere den forkerte fil til en præcis kopi af den korrekte fil – linje for linje, tegn for tegn.

![Screenshot](https://via.placeholder.com/800x400?text=Diff+Preview+and+Patch+Download)  
*(Indsæt gerne et skærmbillede af appen)*

## ✨ Funktioner
- Sammenlign to filer af enhver tekstbaseret type (`.py`, `.txt`, `.md`, `.nfo`, `.json`, `.js`, `.html`, `.css`, `.c`, `.cpp`, `.sh`, `.bat`, `.ps1`, `.rs`, `.go`, `.rb`, `.php`, `.java`, `.kt`, `.swift`, `.sql`, `.lua`, `.vue`, `.tex`, `.csv`, `.xml`, `.yaml`, `.ini` …)
- Generér **unified diff** (standard `patch`-format) med farvelagt preview
- Download patch-fil (`.patch`) som kan anvendes direkte i terminalen
- Visuel fremhævning af tilføjede (+) og fjernede (-) linjer
- Ingen filer sendes til nogen server – alt foregår i din browser

## 🛠️ Sådan bruger du appen

1. Åbn `index.html` i en moderne webbrowser (Chrome, Edge, Firefox, Safari).
2. Vælg **Forkert fil** – den fil, der indeholder fejl og skal rettes.
3. Vælg **Korrekt fil** – referencefilen (den perfekte version).
4. Klik på **🔍 Sammenlign & Generér patch**.
5. Hvis der er forskelle, vises et farvet diff-preview.
6. Klik på **📥 Download patch-fil** for at gemme `.patch`-filen.
7. Anvend patchen i din terminal:

```bash
# Gå til mappen, hvor den forkerte fil ligger
patch -p0 < downloadet_fil.patch
