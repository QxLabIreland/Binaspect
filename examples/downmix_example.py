"""
Run the downmix example from binaspect in a standalone script.

Usage:
  python examples/downmix_example.py
"""

from matplotlib import pyplot as plot
import os, sys
from pathlib import Path
import librosa

# Ensure repo root is on sys.path so binaspect.py can be imported
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

try:
    import binaspect
except Exception as e:
    raise SystemExit(f"Failed to import binaspect: {e}")

ROOT = Path(binaspect.__file__).resolve().parent


def main():
    try:
        r51 = ROOT / "audio" / "downmix_example" / "2_source_5_1.wav"
        r71 = ROOT / "audio" / "downmix_example" / "2_source_7_1.wav"

        rendered_5_1, sr = librosa.load(str(r51), sr=44100, mono=False)
        rendered_7_1, sr = librosa.load(str(r71), sr=44100, mono=False)

        title = ""

        binaspect.ITD_spect_diff(rendered_7_1, rendered_5_1, sr, title=title, plots=True)
        binaspect.ILR_spect_diff(rendered_7_1, rendered_5_1, sr, title=title, plots=True)
    except FileNotFoundError as e:
        raise SystemExit(
            "Audio assets not found. Ensure files exist under 'audio/downmix_example/'.\n"
            f"Original error: {e}"
        )
    plot.show()


if __name__ == "__main__":
    main()
