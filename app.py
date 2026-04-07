import streamlit as st
import difflib
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="PatchCraft Server", page_icon="📄", layout="wide")

# Custom CSS for farvet diff
st.markdown("""
<style>
.diff-add {
    background-color: #14532d;
    color: #bbf7d0;
    display: block;
    font-family: monospace;
    padding: 2px 0;
}
.diff-remove {
    background-color: #7f1a1a;
    color: #fecaca;
    display: block;
    font-family: monospace;
    padding: 2px 0;
}
.diff-header {
    color: #7dd3fc;
    font-weight: bold;
}
.diff-context {
    color: #cbd5e1;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 PatchCraft Server – Diff, patch og automatisk rettelse")
st.markdown("Sammenlign to tekstfiler – generér patch, linjenumre og download færdig rette-fil (batch + prækompileret EXE).")

col1, col2 = st.columns(2)

with col1:
    incorrect_file = st.file_uploader("📁 **Forkert fil** (skal rettes)", type=None, key="incorrect")
    if incorrect_file:
        st.success(f"Valgt: {incorrect_file.name} ({incorrect_file.size/1024:.1f} KB)")

with col2:
    correct_file = st.file_uploader("✅ **Korrekt fil** (reference)", type=None, key="correct")
    if correct_file:
        st.success(f"Valgt: {correct_file.name} ({correct_file.size/1024:.1f} KB)")

if st.button("🔍 Sammenlign og generér patch", type="primary"):
    if not incorrect_file or not correct_file:
        st.error("Vælg begge filer!")
        st.stop()
    
    # Læs filer som tekst
    try:
        incorrect_text = incorrect_file.getvalue().decode("utf-8")
        correct_text = correct_file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"Kunne ikke læse filer som UTF-8 tekst: {e}")
        st.stop()
    
    incorrect_lines = incorrect_text.splitlines()
    correct_lines = correct_text.splitlines()
    
    if incorrect_text == correct_text:
        st.success("✅ Filerne er allerede identiske – ingen patch nødvendig.")
        st.stop()
    
    # Generér unified diff
    diff = difflib.unified_diff(
        incorrect_lines, correct_lines,
        fromfile=incorrect_file.name, tofile=correct_file.name,
        lineterm=""
    )
    patch_content = "\n".join(diff)
    
    # Vis diff med farver
    st.subheader("📜 Unified diff preview")
    diff_lines = patch_content.splitlines()
    html_diff = []
    for line in diff_lines:
        if line.startswith('+'):
            html_diff.append(f'<span class="diff-add">{line}</span>')
        elif line.startswith('-'):
            html_diff.append(f'<span class="diff-remove">{line}</span>')
        elif line.startswith('@@'):
            html_diff.append(f'<span class="diff-header">{line}</span>')
        else:
            html_diff.append(f'<span class="diff-context">{line}</span>')
    st.markdown(f'<div style="background:#0f172a; padding:1rem; border-radius:1rem; font-family:monospace; overflow-x:auto;">{"<br>".join(html_diff)}</div>', unsafe_allow_html=True)
    
    # Generér diff rapport med linjenumre
    st.subheader("📄 Diff rapport med præcise linjenumre")
    d = difflib.SequenceMatcher(None, incorrect_lines, correct_lines)
    report_lines = []
    report_lines.append(f"DIFF RAPPORT – PRÆCISE LINJENUMMER")
    report_lines.append(f"Forkert fil: {incorrect_file.name}")
    report_lines.append(f"Korrekt fil: {correct_file.name}\n")
    
    old_line = 1
    for tag, i1, i2, j1, j2 in d.get_opcodes():
        if tag == 'replace':
            report_lines.append(f"[ERSTAT I FORKERT FIL] Linje {old_line+i1} → {old_line+i2-1} (erstattes med korrekte linjer {j1+1}-{j2}):")
            for line in incorrect_lines[i1:i2]:
                report_lines.append(f"  - {line}")
            for line in correct_lines[j1:j2]:
                report_lines.append(f"  + {line}")
        elif tag == 'delete':
            report_lines.append(f"[SLET FRA FORKERT FIL] Linje {old_line+i1} → {old_line+i2-1}:")
            for line in incorrect_lines[i1:i2]:
                report_lines.append(f"  - {line}")
        elif tag == 'insert':
            report_lines.append(f"[INDSÆT I FORKERT FIL] Ved linje {old_line+i1} (før nuværende linje {old_line+i1}):")
            for line in correct_lines[j1:j2]:
                report_lines.append(f"  + {line}")
        # 'equal' springes over
    report_lines.append("\n📌 Brug rapporten til manuelt at rette filen.")
    report_text = "\n".join(report_lines)
    st.text_area("Forhåndsvisning af diff rapport", report_text, height=200)
    
    # Generér batch-fil, der bruger en prækompileret patch_applier.exe
    batch_content = f"""@echo off
echo Anvender patch på "{incorrect_file.name}"...
if not exist "{incorrect_file.name}" (
    echo Fejl: Filen "{incorrect_file.name}" findes ikke i denne mappe.
    pause
    exit /b 1
)
if not exist "patch_applier.exe" (
    echo Fejl: patch_applier.exe mangler.
    echo Download den fra https://github.com/dit-brugernavn/PatchCraft-Server/releases
    pause
    exit /b 1
)
patch_applier.exe "patch_to_apply.patch" "{incorrect_file.name}"
echo.
echo Tryk en tast for at lukke...
pause > nul
"""
    
    # Generér Python-script (til dem der selv vil kompilere til EXE)
    script_content = f'''#!/usr/bin/env python3
# Auto-genereret patch-applier fra PatchCraft Server
import sys, os, subprocess, tempfile

PATCH = r"""{patch_content}"""

def main():
    target = r"""{incorrect_file.name}"""
    if len(sys.argv) > 1:
        target = sys.argv[1]
    if not os.path.exists(target):
        print(f"Fejl: '{target}' findes ikke")
        sys.exit(1)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as f:
        f.write(PATCH)
        patch_file = f.name
    
    try:
        cmd = ['patch', '-p0', '-i', patch_file, target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Patch anvendt!")
        else:
            print("❌ Fejl ved anvendelse af patch:")
            print(result.stderr)
    finally:
        os.unlink(patch_file)

if __name__ == '__main__':
    main()
'''
    
    # Download sektion
    st.subheader("📥 Download retteværktøjer")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.download_button(
            label="📄 .patch-fil",
            data=patch_content,
            file_name=f"patch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.patch",
            mime="text/x-patch"
        )
    with col_b:
        st.download_button(
            label="📑 Diff rapport (linjenumre)",
            data=report_text,
            file_name=f"diff_rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    with col_c:
        st.download_button(
            label="⚙️ Batch-fil (brug med patch_applier.exe)",
            data=batch_content,
            file_name=f"apply_patch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bat",
            mime="text/plain"
        )
    with col_d:
        st.download_button(
            label="🐍 Python-script (kan gøres til .exe)",
            data=script_content,
            file_name=f"apply_patch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
            mime="text/x-python"
        )
    
    st.info("💡 **For at få automatisk .exe:** Download batch-filen ovenfor **og** hent `patch_applier.exe` (prækompileret) fra [Releases](https://github.com/dit-brugernavn/PatchCraft-Server/releases). Læg begge i samme mappe som den forkerte fil, og dobbeltklik på batch-filen. **Alternativt:** Konverter Python-scriptet til .exe med `pyinstaller --onefile --noconsole filnavn.py`.")

st.markdown("---")
st.markdown("""
**Sådan får du `patch_applier.exe` (prækompileret):**
1. Gå til [Releases](https://github.com/dit-brugernavn/PatchCraft-Server/releases) på dit repository.
2. Download `patch_applier.exe` (eller byg den selv med C# – se README).
3. Placer den i samme mappe som batch-filen.
""")
