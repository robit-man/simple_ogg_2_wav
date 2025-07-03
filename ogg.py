#!/usr/bin/env python3
import sys
import os
import subprocess
import venv

# ─── Configuration ────────────────────────────────────────────────────────────
VENV_DIR = os.path.join(os.path.dirname(__file__), 'venv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'wav')

# ─── Step 1: Ensure we're running inside our venv ──────────────────────────────
def ensure_venv():
    # If sys.prefix == base_prefix, we are NOT in a venv
    if getattr(sys, 'base_prefix', sys.prefix) == sys.prefix:
        # 1a) Create venv if needed
        if not os.path.isdir(VENV_DIR):
            print(f"Creating virtualenv in {VENV_DIR}...")
            venv.EnvBuilder(with_pip=True).create(VENV_DIR)
        # 1b) Install dependencies
        py_exe = os.path.join(VENV_DIR, 'Scripts' if os.name == 'nt' else 'bin', 'python')
        print("Installing dependencies into venv...")
        subprocess.check_call([py_exe, '-m', 'pip', 'install', 'imageio-ffmpeg'])
        # 1c) Re-execute this script inside the venv Python
        os.execv(py_exe, [py_exe] + sys.argv)

# ─── Step 2: Conversion logic ───────────────────────────────────────────────────
def convert_all_oggs_to_mono_wav():
    # import after ensure_venv so that imageio_ffmpeg is available
    import imageio_ffmpeg
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

    # make output folder
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # find all .ogg files in CWD
    oggs = [f for f in os.listdir('.') if f.lower().endswith('.ogg')]
    if not oggs:
        print("No .ogg files found in this directory.")
        return

    for ogg in oggs:
        base = os.path.splitext(os.path.basename(ogg))[0]
        out_wav = os.path.join(OUTPUT_DIR, f"{base}.wav")
        print(f"Converting {ogg} → {out_wav} (mono)...")
        subprocess.check_call([
            ffmpeg_bin,
            '-y',          # overwrite without asking
            '-i', ogg,     # input file
            '-ac', '1',    # downmix to mono
            out_wav
        ])
    print("All done! Your WAVs are in the ‘wav/’ folder.")

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    ensure_venv()
    convert_all_oggs_to_mono_wav()
