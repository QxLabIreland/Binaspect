"""
Run the ambisonics example from binaspect in a standalone script.

Usage:
  python examples/ambisonics_example.py

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

# Resolve repo root robustly based on the library location
ROOT = Path(binaspect.__file__).resolve().parent


def main():
    try:
        ref_path = ROOT / "audio" / "ambisonic_examples" / "castanetsRev_dynamic_A0_A360_E30_HOA_REF_rendered.wav"
        test_path = ROOT / "audio" / "ambisonic_examples" / "castanetsRev_dynamic_A0_A360_E30_FOA_REF_rendered.wav"

        ref_file, sr = librosa.load(str(ref_path), sr=44100, mono=False)
        test_file, sr = librosa.load(str(test_path), sr=44100, mono=False)

        title = "HOA (ref) vs FOA (test) Az 0-360 , El 30"

        # ITD_spect_diff Example
        binaspect.ITD_spect_diff(ref_file, test_file, sr, title=title + " | ITD", plots=True)

        # ILR_spect_diff Example
        binaspect.ILR_spect_diff(ref_file, test_file, sr, title=title + " | ILR", plots=True)
    except FileNotFoundError as e:
        raise SystemExit(
            "Audio assets not found. Ensure files exist under './audio/ambisonic_examples/'.\n"
            f"Original error: {e}"
        )
    # Show all figures created by the example
    plot.show()


if __name__ == "__main__":
    main()
