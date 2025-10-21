"""
Run the codec comparison example from binaspect in a standalone script.

Usage:
  python examples/codec_example.py


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
        opus512 = ROOT / "audio" / "opus_examples" / "castanets360_opus512k.wav"
        opus128 = ROOT / "audio" / "opus_examples" / "castanets360_opus128k.wav"
        opus32 = ROOT / "audio" / "opus_examples" / "castanets360_opus32k.wav"

        opus512_file, sr = librosa.load(str(opus512), sr=44100, mono=False)
        opus128_file, sr = librosa.load(str(opus128), sr=44100, mono=False)
        opus32_file, sr = librosa.load(str(opus32), sr=44100, mono=False)

        ITD_histogram_512 = binaspect.ITD_hist(opus512_file, sr)
        ITD_histogram_128 = binaspect.ITD_hist(opus128_file, sr)
        ITD_histogram_32 = binaspect.ITD_hist(opus32_file, sr)

        ILR_histogram_512 = binaspect.ILR_hist(opus512_file, sr)
        ILR_histogram_128 = binaspect.ILR_hist(opus128_file, sr)
        ILR_histogram_32 = binaspect.ILR_hist(opus32_file, sr)

        xlimit = (0, ITD_histogram_512.shape[1])
        fig, axs = plot.subplots(2, 3, figsize=(16, 12))

        plot.rcParams.update({'font.size': 15})
        axs[0,0].imshow(ITD_histogram_512, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[0,0].set_title('ITD Hist. (Opus 512k)')
        axs[0,0].set_ylabel('ITD Estimate (μs)')
        axs[0,0].set_xlabel('Time (frames)')
        axs[0,0].set_yticks([0, 100, 200, 300, 400])
        axs[0,0].set_yticklabels(['-800', '-400', '0', '400', '800'])
        axs[0,0].set_xlim(0, xlimit[1])

        axs[0,1].imshow(ITD_histogram_128, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[0,1].set_title('ITD Hist. (Opus 128k)')
        axs[0,1].set_xlabel('Time (frames)')
        axs[0,1].set_yticks([])
        axs[0,1].set_yticklabels([])
        axs[0,1].set_xlim(0, xlimit[1])

        axs[0,2].imshow(ITD_histogram_32, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[0,2].set_title('ITD Hist. (Opus 32k)')
        axs[0,2].set_xlabel('Time (frames)')
        axs[0,2].set_yticks([])
        axs[0,2].set_yticklabels([])
        axs[0,2].set_xlim(0, xlimit[1])

        plot.subplots_adjust(hspace=0.3)

        axs[1,0].imshow(ILR_histogram_512, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[1,0].set_title('ILR Hist. (Opus 512k)')
        axs[1,0].set_ylabel('ILR Estimate')
        axs[1,0].set_xlabel('Time (frames)')
        axs[1,0].set_yticks([0, 100, 200, 300, 400])
        axs[1,0].set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
        axs[1,0].set_xlim(0, xlimit[1])

        axs[1,1].imshow(ILR_histogram_128, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[1,1].set_title('ILR Hist. (Opus 128k)')
        axs[1,1].set_xlabel('Time (frames)')
        axs[1,1].set_yticks([])
        axs[1,1].set_yticklabels([])
        axs[1,1].set_xlim(0, xlimit[1])

        axs[1,2].imshow(ILR_histogram_32, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[1,2].set_title('ILR Hist. (Opus 32k)')
        axs[1,2].set_xlabel('Time (frames)')
        axs[1,2].set_yticks([])
        axs[1,2].set_yticklabels([])
        axs[1,2].set_xlim(0, xlimit[1])
    except FileNotFoundError as e:
        raise SystemExit(
            "Audio assets not found. Ensure files exist under './audio/opus_examples/'.\n"
            f"Original error: {e}"
        )
    plot.show()


if __name__ == "__main__":
    main()
