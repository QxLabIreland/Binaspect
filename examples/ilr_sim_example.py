from matplotlib import pyplot as plot
import os, sys
from pathlib import Path
import librosa

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import binaspect
ROOT = Path(binaspect.__file__).resolve().parent


def main():
    ref = ROOT / "audio" / "opus_examples" / "castanets360_opus512k.wav"
    test = ROOT / "audio" / "opus_examples" / "castanets360_opus32k.wav"
    ref_data, sr = librosa.load(str(ref), sr=44100, mono=False)
    test_data, sr = librosa.load(str(test), sr=44100, mono=False)
    sim = binaspect.ILR_sim(ref_data, test_data, sr, plots=True)
    print("ILR Similarity:", sim)
    plot.show()


if __name__ == "__main__":
    main()
