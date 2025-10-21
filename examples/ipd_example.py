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
    wav = ROOT / "audio" / "opus_examples" / "castanets360_opus512k.wav"
    data, sr = librosa.load(str(wav), sr=44100, mono=False)
    binaspect.IPD_spect(data, sr, start_freq=50, stop_freq=620, wrapped=True, plots=True)
    plot.show()


if __name__ == "__main__":
    main()
