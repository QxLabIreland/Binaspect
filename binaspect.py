# %matplotlib ipympl
import librosa
import numpy as np
import matplotlib.pyplot as plot
import colormap


# Features and Functions
# 1 - ITD Histogram
# 2 - ILR Histogram
# 9 - ILD Histogram
# 3 - ITD Spectrogram (and masks if applicable)
# 8 - IPD Spectrogram (and masks if applicable)
# 4 - ILR Spectrogram (and masks if applicable)
# 7 - ILD Spectrogram (and masks if applicable)
# 5 - ITD Difference Dynamic
# 6 - ILR Difference Dynamic


# change spect diff to just diff?
# 10 - ITD Difference Spectrogram 
# 11 - ILD Difference Spectrogram
# 12 - IPD Difference Spectrogram


def ITD_spect(input_file, sr, start_freq=50, stop_freq=620, plots=False):
    # Calculate the ITD spectragram of a stereo or binaural audio file
    
    # Setup the parameters
    window_size = 4096                         # Window size for STFT
    hop_size = round(window_size/4)             # Analysis hop size
    window_type = np.hanning(window_size)       # Window function
    bin_width = sr/window_size                   # Width of the frequency bins

    # check if the frequency range is valid
    if start_freq < 0 or stop_freq > sr/2:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))
    if start_freq >= stop_freq:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))
    
    # # * Can only measure accurately up to 620 Hz because of modulo 2pi wrap around
    # start_freq = 50                              # frequency in Hz to start processing
    # stop_freq = 620                           # frequency in Hz to stop processing
    
    # ITD Histogram Setup
    ITDstartbin = int(np.round(start_freq/bin_width))
    ITDstopbin = int(np.round(stop_freq/bin_width))        # freq bin number to start processing

    # Split Channels
    left_td = input_file[0, :]
    right_td = input_file[1, :]

    # Cpmplex STFT
    left = librosa.stft(left_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)
    right = librosa.stft(right_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)

    # Calculate Magnitude and Phase
    left_mag, left_phase = librosa.magphase(left)
    right_mag, right_phase = librosa.magphase(right)

    intensity = left_mag + right_mag

    left_phase = np.angle(left_phase)
    right_phase = np.angle(right_phase)

    # Get the number of bins and frames
    [numbins, numframes] = np.shape(left_mag)

    # ITD_spectrogram Setup

    ITD_spectra = np.zeros((ITDstopbin, numframes))

    # Calculate the Phase Differences
    phasediffs = left_phase - right_phase
   

    # Calculate ITD
    for frame in range(numframes):
       
        for bin in range(ITDstartbin, ITDstopbin):
            
            phasediff = phasediffs[bin, frame]
            
            # calculate the wrapped phase difference
            wrapped_phase_diff = np.mod(phasediff + np.pi, 2*np.pi) - np.pi

            # convert the wrapped phase difference to a delay in seconds
            bindelay = wrapped_phase_diff / (2 * np.pi * bin_width * bin)
             
            if intensity[bin, frame] >= 0.00:
            
                ITD_spectra[bin, frame] = bindelay
  
    # Remove bins before ITDstartbin
    ITD_spectra = ITD_spectra[ITDstartbin:ITDstopbin, :]

    # show the ITD spectra
    if plots:
        plot.figure()
        plot.imshow(ITD_spectra, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        plot.colorbar()
        plot.ylabel('Frequency (Hz)')
        plot.xlabel('Time (frames)')
        plot.title('Interaural Time Difference (μs)')
        plot.yticks(np.linspace(0, ITDstopbin - ITDstartbin, 5), np.round(np.linspace(start_freq, stop_freq, 5)).astype(int))
        

    return ITD_spectra

def IPD_spect(input_file, sr, start_freq=50, stop_freq=620, wrapped=False, plots=False):
    # Calculate the IPD spectragram of a stereo or binaural audio file
    
    # Setup the parameters
    window_size = 4096                         # Window size for STFT
    hop_size = round(window_size/4)             # Analysis hop size
    window_type = np.hanning(window_size)       # Window function
    bin_width = sr/window_size                   # Width of the frequency bins

    # check if the frequency range is valid
    if start_freq < 0 or stop_freq > sr/2:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))
    if start_freq >= stop_freq:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))

    # Notes
    # *Realistically we can only measure accurately up to 620 Hz because of modulo 2pi wrap around
    # start_freq = 50                              # frequency in Hz to start processing
    # stop_freq = 620                           # frequency in Hz to stop processing
    
    # IPD Histogram Setup
    IPDstartbin = int(np.round(start_freq/bin_width))        # freq bin number to start processing
    IPDstopbin = int(np.round(stop_freq/bin_width))        # freq bin number to start processing

    # Split Channels
    left_td = input_file[0, :]
    right_td = input_file[1, :]

    # Cpmplex STFT
    left = librosa.stft(left_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)
    right = librosa.stft(right_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)

    # Calculate Magnitude and Phase
    left_mag, left_phase = librosa.magphase(left)
    right_mag, right_phase = librosa.magphase(right)

    intensity = left_mag + right_mag

    left_phase = np.angle(left_phase)
    right_phase = np.angle(right_phase)

    # Get the number of bins and frames
    [numbins, numframes] = np.shape(left_mag)

    # IPD_spectrogram Setup

    IPD_spectra = np.zeros((IPDstopbin, numframes))

    # Calculate the Phase Differences
    phasediffs = left_phase - right_phase

    if wrapped == True:
        # Wrap phase differences to be between -pi and pi
        phasediffs = np.mod(phasediffs + np.pi, 2*np.pi) - np.pi

    # Remove bins before IPDstartbin
    IPD_spectra = phasediffs[IPDstartbin:IPDstopbin, :]

    
    # show the IPD spectra
    if plots:
        plot.figure()
        plot.imshow(IPD_spectra, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        plot.colorbar()
        plot.ylabel('Frequency (Hz)')
        plot.xlabel('Time (frames)')
        plot.title('Interaural Phase Difference (radians)')
        plot.yticks(np.linspace(0, IPDstopbin - IPDstartbin, 5), np.round(np.linspace(start_freq, stop_freq, 5)).astype(int))
        

    return IPD_spectra



def ILR_spect(input_file, sr, start_freq=1700, stop_freq=4600, plots=False):
    # Calculate the ILR spectra of a stereo audio file
    
    # Setup the parameters

    window_size = 4096                          # Window size for STFT
    hop_size = round(window_size/4)             # Analysis hop size
    window_type = np.hanning(window_size)       # Window function
    bin_width = sr/window_size                   # Width of the frequency bins

    # check if the frequency range is valid
    if start_freq < 0 or stop_freq > sr/2:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))
    if start_freq >= stop_freq:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))

    # Notes
    # 500 - 2000 => for spec diff mean plots
    # 1700 - 4600 => for ILR hists
    # Full Band (all bins) => for ML features in conjunction with binary mask if necessary
    # start_freq = 500                          # frequency in Hz to start processing
    # stop_freq = 2500                       # frequency in Hz to stop processing

    ILRstartbin = int(np.round(start_freq/bin_width))        # freq bin number to start processing
    ILRstopbin = int(np.round(stop_freq/bin_width))        # freq bin number to stop processing
  
    # Split Channels
    left_td = input_file[0, :]
    right_td = input_file[1, :]

    # Cpmplex STFT
    left = librosa.stft(left_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)
    right = librosa.stft(right_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)

    # Calculate Magnitude and Phase
    left_mag, left_phase = librosa.magphase(left)
    right_mag, right_phase = librosa.magphase(right)

    intensity = left_mag + right_mag

    # mask out low intensity values
    mask = intensity < 0.0
    left_mag[mask] = np.nan
    right_mag[mask] = np.nan

    # Getting intensity ratios
    ILR_spectra = right_mag / left_mag

    # Handle divide by zero
    ILR_spectra[np.isinf(ILR_spectra)] = np.nan  # Replace inf with nan
    
    # TLDR - everything greater than 1 gets inverted amd a negative value
    ILR_spectra[ILR_spectra < 1] = (1 - ILR_spectra[ILR_spectra < 1])
    ILR_spectra[ILR_spectra >= 1] = -(1 - (1 / ILR_spectra[ILR_spectra >= 1]))
   
    # Remove bins before ITDstartbin
    ILR_spectra = ILR_spectra[ILRstartbin:ILRstopbin, :]
    
    # show the ILR spectra
    if plots:
        plot.figure()
        plot.imshow(ILR_spectra, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        plot.colorbar()
        plot.ylabel('Frequency (Hz)')
        plot.xlabel('Time (frames)')
        plot.title('Interaural Level Ratio (-1 to 1)')
        plot.yticks(np.linspace(0, ILRstopbin - ILRstartbin, 5), np.round(np.linspace(start_freq, stop_freq, 5)).astype(int))
        

    return ILR_spectra

def ILD_spect(input_file, sr, start_freq=1700, stop_freq=4600, plots=False):
    # Calculate the ILD spectra of a stereo audio file

    # Setup the parameters

    window_size = 4096                          # Window size for STFT
    hop_size = round(window_size/4)             # Analysis hop size
    window_type = np.hanning(window_size)       # Window function
    bin_width = sr/window_size                   # Width of the frequency bins

    # check if the frequency range is valid
    if start_freq < 0 or stop_freq > sr/2:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))
    if start_freq >= stop_freq:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))

    # Notes
    # 500 - 2000 => for spec diff mean plots
    # 1700 - 4600 => for ILD hists
    # Full Band (all bins) => for ML features in conjunction with binary mask if necessary
    # start_freq = 500                          # frequency in Hz to start processing
    # stop_freq = 2500                       # frequency in Hz to stop processing

    ILDstartbin = int(np.round(start_freq/bin_width))        # freq bin number to start processing
    ILDstopbin = int(np.round(stop_freq/bin_width))        # freq bin number to stop processing
  
    # Split Channels
    left_td = input_file[0, :]
    right_td = input_file[1, :]

    # Cpmplex STFT
    left = librosa.stft(left_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)
    right = librosa.stft(right_td, hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)

    # Calculate Magnitude and Phase
    left_mag, left_phase = librosa.magphase(left)
    right_mag, right_phase = librosa.magphase(right)

    intensity = left_mag + right_mag

    # mask out low intensity values
    mask = intensity < 0.0
    left_mag[mask] = np.nan
    right_mag[mask] = np.nan

    # Getting level differences in dB
    ILD_spectra = 20 * np.log10(right_mag / left_mag)

    # Handle divide by zero
    ILD_spectra[np.isinf(ILD_spectra)] = np.nan  # Replace inf with nan
   
    # Remove bins before ITDstartbin
    ILD_spectra = -ILD_spectra[ILDstartbin:ILDstopbin, :]
    
    # show the ILD spectra
    if plots:
        plot.figure()
        plot.imshow(ILD_spectra, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        plot.colorbar()
        plot.ylabel('Frequency (Hz)')
        plot.xlabel('Time (frames)')
        plot.title('Interaural Level Difference (dB)')        
        plot.yticks(np.linspace(0, ILDstopbin - ILDstartbin, 5), np.round(np.linspace(start_freq, stop_freq, 5)).astype(int))
        

    return ILD_spectra

# Function to compare ILR Spectra
def ILR_spect_diff(ref, test, sr, title="", plots=False): 

    ILR_spect_ref = ILR_spect(ref,sr)
    ILR_spect_test = ILR_spect(test,sr)

    absdiff = (np.abs(ILR_spect_test) - np.abs(ILR_spect_ref))
    diff = (ILR_spect_test - ILR_spect_ref)

    mean_ILR_diff = np.nanmean(np.abs(np.mean(diff, axis=0)))
    max_ILR_diff = np.nanmax(np.abs(np.mean(diff, axis=0)))

    ILR_time_diff = (np.nanmedian(diff, axis=0))

    if plots:

        # plot.figure()
        # plot.imshow((diff), aspect='auto', origin='lower', interpolation='nearest')
        # # plot.imshow((absdiff), aspect='auto', origin='lower', interpolation='nearest')
        # plot.ylabel('Frequency Bin')
        # plot.xlabel('Time Frame')
        # plot.title('ILR Spectrogram Difference')
        # plot.colorbar()  
      
        hist_size = 400

        ILR_histogram_ref = ILR_hist(ref,sr,hist_size=hist_size)
        ILR_histogram_test = ILR_hist(test,sr,hist_size=hist_size)

        xlimit = (0, ILR_histogram_ref.shape[1])

        plot.rcParams.update({'font.size': 14})
        fig, axs = plot.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(title)
        fig.subplots_adjust(top=0.82)  # Add more space above the subplots for the suptitle
        
        axs[0].imshow(ILR_histogram_ref, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[0].set_title('ILR Histogram (ref)')
        axs[0].set_ylabel('ILR Estimate')
        axs[0].set_xlabel('Time (frames)')
        axs[0].set_yticks([0, 100, 200, 300, 400])
        axs[0].set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
        axs[0].set_xlim(0, hist_size)

        axs[1].imshow(ILR_histogram_test, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[1].set_title('ILR Histogram (test)')
        axs[1].set_xlabel('Time (frames)')
        axs[1].set_yticks([0, 100, 200, 300, 400])
        axs[1].set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
        axs[1].set_xlim(0, xlimit[1])

        axs[2].plot(ILR_time_diff)
        axs[2].axhline(0, color='lightgray', linestyle='--')
        axs[2].set_title('ILR Difference')
        axs[2].text(
            0.95, 0.95,
            f"mean = {mean_ILR_diff:.1f}\nmax = {max_ILR_diff:.1f}",
            ha='right', va='top', transform=axs[2].transAxes,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
        )
        axs[2].set_ylim(-1, 1)
        axs[2].set_yticks([-1, -0.5, 0, 0.5, 1])
        axs[2].set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
        axs[2].set_xlim(0, xlimit[1])
        axs[2].set_xlabel('Time (frames)')
        # axs[3].imshow(diff, aspect='auto', origin='lower', interpolation='nearest')
        # axs[3].set_title('ILR Difference Spectrogram')
        # axs[3].set_ylabel('Frequency')
        # axs[3].set_yticks([0, 100, 200, 300, 400])
        # axs[3].set_yticklabels(['-90°', '-45°', '0°', '45°', '90°'])
        
        # save figure as PDF
        # fig.savefig("ILR_analysis.pdf", bbox_inches='tight')

        

    return mean_ILR_diff, max_ILR_diff


def ITD_spect_diff(ref, test, sr, title="", plots=False): 
    
    ITD_spect_ref = ITD_spect(ref,sr)
    ITD_spect_test = ITD_spect(test,sr)

    # If the 0 degree IR is not accurate, this compensates for asymmetry 
    absdiff = np.abs(ITD_spect_test) - np.abs(ITD_spect_ref)
    
    diff = (ITD_spect_test) - (ITD_spect_ref)

    mean_diff_degrees = np.mean(np.abs((np.mean(diff, axis=0)))) * 1/0.00086 * 90
    max_diff_degrees = np.max(np.abs((np.mean(diff, axis=0)))) * 1/0.00086 * 90
    mean_diff_ITD = np.median(((np.mean(diff, axis=0))))

    ITD_time_diff = (np.mean(diff, axis=0))
  
    if plots:

        ITD_histogram_ref = ITD_hist(ref,sr)
        ITD_histogram_test = ITD_hist(test,sr)

        xlimit = (0, ITD_histogram_ref.shape[1])

        plot.rcParams.update({'font.size': 14})
        fig, axs = plot.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(title)
        fig.subplots_adjust(top=0.82)  # Add more space above the subplots for the suptitle
        axs[0].imshow(ITD_histogram_ref, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[0].set_title('ITD Histogram (ref)')
        axs[0].set_ylabel('ITD Estimate (μs)')
        axs[0].set_xlabel('Time (frames)')
        axs[0].set_yticks([0, 100, 200, 300, 400])
        # axs[0].set_yticklabels(['-90°', '-45°', '0°', '45°', '90°'])
        axs[0].set_yticklabels(['-800', '-400', '0', '400', '800'])
        axs[0].set_xlim(0, xlimit[1])

        axs[1].imshow(ITD_histogram_test, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[1].set_title('ITD Histogram (test)')
        axs[1].set_xlabel('Time (frames)')
        axs[1].set_yticks([0, 100, 200, 300, 400])
        # axs[1].set_yticklabels(['-90°', '-45°', '0°', '45°', '90°'])
        axs[1].set_yticklabels(['-800', '-400', '0', '400', '800'])
        axs[1].set_xlim(0, xlimit[1])

        axs[2].plot(ITD_time_diff)
        axs[2].axhline(0, color='lightgray', linestyle='--')
        # Place mean and max inside the graph as text
        axs[2].set_title('ITD Difference')
        axs[2].text(
            0.95, 0.95,
            f"mean = {mean_diff_degrees:.1f}°\nmax = {max_diff_degrees:.0f}°",
            ha='right', va='top', transform=axs[2].transAxes,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
        )
        axs[2].set_ylim(-0.00086, 0.00086)
        axs[2].set_xlabel('Time (frames)')
        axs[2].set_yticks([-0.00086, -0.00043, 0, 0.00043, 0.00086])
        axs[2].set_yticklabels(['-90°', '-45°', '0°', '45°', '90°'])
        axs[2].set_xlim(0, xlimit[1])
        # axs[3].imshow(diff, aspect='auto', origin='lower', interpolation='nearest')
        # axs[3].set_title('ITD Difference Spectrogram')
        # axs[3].set_ylabel('Frequency')
        # axs[3].set_yticks([0, 100, 200, 300, 400])
        # axs[3].set_yticklabels(['-90°', '-45°', '0°', '45°', '90°'])
        
        # save figure as PDF
        # fig.savefig("ITD_analysis.pdf", bbox_inches='tight')

    return mean_diff_degrees, mean_diff_ITD

def ITD_hist(input_file, sr, hist_size=400, start_freq=50, stop_freq=620, normalize=True, energyweighting=True, plots=False):
    # Calculate the ITD histogram of a stereo or binaural audio file

    # check if the frequency range is valid
    if start_freq < 0 or stop_freq > sr/2:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))
    if start_freq >= stop_freq:
        raise ValueError("Invalid frequency range. Valid range is [0, {}]".format(sr/2))

    # Get the ITD spectrogram
    ITD_spectra = ITD_spect(input_file, sr, start_freq=start_freq, stop_freq=stop_freq, plots=False)
  
    # Setup the parameters
    window_size = 4096                         # Window size for STFT
    hop_size = round(window_size/4)             # Analysis hop size
    window_type = np.hanning(window_size)       # Window function
    bin_width = sr/window_size                   # Width of the frequency bins
     
    # Note - Can only measure accurately up to 620 Hz because of modulo 2pi wrap around
    # Idea - Try modify to use ILR as estimate of first arriving ear
    # start_freq = 50                             # frequency in Hz to start processing
    # stop_freq = 620                           # frequency in Hz to stop processing
    
    # ITD Histogram Setup
    ITDstartbin = int(np.round(start_freq/bin_width))        # freq bin number to start processing
    ITDstopbin = int(np.round(stop_freq/bin_width))        # freq bin number to start processing
    
    ITDhist_size = hist_size   # Size of the histogram
    delaybinedges = np.linspace(-0.00088, 0.00088, ITDhist_size + 1) 
    delaybinwidth = delaybinedges[1] - delaybinedges[0]
    delayhist = np.zeros(ITDhist_size)

    # Complex STFT
    left = librosa.stft(input_file[0, :], hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)
    right = librosa.stft(input_file[1, :], hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)

    # Calculate Magnitude and trim according to start/stop bins
    left_mag = np.abs(left)[ITDstartbin:ITDstopbin, :]
    right_mag = np.abs(right)[ITDstartbin:ITDstopbin, :]

    # Get the number of bins and frames of the band-limited ITD spectrogram
    [numbins, numframes] = np.shape(ITD_spectra)

    # ITD_histogram Setup
    ITD_histogram = np.zeros((ITDhist_size, numframes))
    
    # Calculate Histogram
    for frame in range(numframes):

        bindelays = ITD_spectra[:, frame]
        mag_weights = left_mag[:, frame] + right_mag[:, frame]

        if energyweighting == True:
            # weighted histogram
            delayhist, bin_edges = np.histogram(bindelays, bins=delaybinedges-(delaybinwidth/2), weights=mag_weights)
        else:
            delayhist, bin_edges = np.histogram(bindelays, bins=delaybinedges-(delaybinwidth/2))

        if normalize == True:
            # Normalize the histogram to max value of 1
            delayhist = delayhist / np.max(delayhist) 

        ITD_histogram[:, frame] = delayhist         # Add frame to the ITD_histogram

        delayhist = np.zeros(ITDhist_size)          # Zero the histograms for next iteration
    
    if plots:

        xlimit = (0, ITD_histogram.shape[1])

        plot.rcParams.update({'font.size': 14})
        fig, axs = plot.subplots(1, 1, figsize=(8, 6))
        axs.imshow(ITD_histogram, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs.set_title('ITD Histogram')
        axs.set_ylabel('ITD Estimate (μs)')
        axs.set_xlabel('Time (frames)')
        axs.set_yticks([0, 100, 200, 300, 400])
        axs.set_yticklabels(['-800', '-400', '0', '400', '800'])
        axs.set_xlim(0, xlimit[1])
        axs.axhline(hist_size/2, color='white', linestyle='--', linewidth=0.7)
        
    
    return ITD_histogram 

def ILR_hist(input_file, sr, hist_size=400, start_freq=1700, stop_freq=4600, normalize=True, energyweighting=True, plots=False):
    # Calculate the ILR histogram of a stereo or binaural audio file

    # Get the ILR spectrogram
    ILR_spectra = ILR_spect(input_file, sr, start_freq=start_freq, stop_freq=stop_freq, plots=False)

    # Setup the parameters
    exponent = 3 
    window_size = 4096                         # Window size for STFT
    hop_size = round(window_size/4)             # Analysis hop size
    window_type = np.hanning(window_size)       # Window function
    bin_width = sr/window_size                   # Width of the frequency bins

    # ILR Histogram Setup
    # (1700 - 4600) normally or (1800 - 5600 when dealing with Virtual rendering)
    # start_freq = 1700                        # frequency in Hz to start processing (1700 - 4600) or (500 - 2500)
    # stop_freq = 4600                         # frequency in Hz to stop processing

    # ILR Histogram Setup
    ILRstartbin = int(np.round(start_freq/bin_width))        # freq bin number to start processing
    ILRstopbin = int(np.round(stop_freq/bin_width))        # freq bin number to start processing

    ILRhist_size = hist_size   # Size of the histogram
    levelbinedges = np.linspace(-1, 1, ILRhist_size + 1)
    levelbinwidth = levelbinedges[1] - levelbinedges[0]
    levelhist = np.zeros(ILRhist_size)

    # Complex STFT
    left = librosa.stft(input_file[0, :], hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)
    right = librosa.stft(input_file[1, :], hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)

    # Calculate Magnitude and trim according to start/stop bins
    left_mag = np.abs(left)[ILRstartbin:ILRstopbin, :]
    right_mag = np.abs(right)[ILRstartbin:ILRstopbin, :]

    # Get the number of bins and frames of the band-limited ILR spectrogram
    [numbins, numframes] = np.shape(ILR_spectra)

    # ILR_histogram Setup
    ILR_histogram = np.zeros((ILRhist_size, numframes))

    # Calculate Histogram
    for frame in range(numframes):

        ratios = ILR_spectra[:, frame]
        mag_weights = left_mag[:, frame] + right_mag[:, frame]

        if energyweighting == True:
            # weighted histogram
            levelhist, bin_edges = np.histogram(ratios, bins=levelbinedges-(levelbinwidth/2*0), weights=mag_weights)
        else:
            levelhist, bin_edges = np.histogram(ratios, bins=levelbinedges-(levelbinwidth/2))

        levelhist = levelhist**exponent          # Exponent to enhance peaks 

        if normalize == True:
            # Normalize the histogram to max value of 1
            levelhist = levelhist / np.max(levelhist)  

        ILR_histogram[:, frame] = levelhist         # Add frame to the ILR_histogram

        levelhist = np.zeros(ILRhist_size)          # Zero the histograms for next iteration

    if plots:
        xlimit = (0, ILR_histogram.shape[1])

        plot.rcParams.update({'font.size': 14})
        fig, axs = plot.subplots(1, 1, figsize=(8, 6))
        axs.imshow(ILR_histogram, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs.set_title('ILR Histogram')
        axs.set_ylabel('ILR Estimate')
        axs.set_xlabel('Time (frames)')
        axs.set_yticks([0, 100, 200, 300, 400])
        axs.set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
        axs.set_xlim(0, xlimit[1])
        axs.axhline(hist_size/2, color='white', linestyle='--', linewidth=0.7)
        

    return ILR_histogram

def ILD_hist(input_file, sr, hist_size=400, start_freq=1700, stop_freq=4600, dB_range=24, normalize=True, energyweighting=True , plots=False):
    # Calculate the ILD histogram of a stereo or binaural audio file

    # Get the ILD spectrogram
    ILD_spectra = ILD_spect(input_file, sr, start_freq=start_freq, stop_freq=stop_freq, plots=False)

    # Setup the parameters
    exponent = 3
    window_size = 4096                         # Window size for STFT
    hop_size = round(window_size/4)             # Analysis hop size
    window_type = np.hanning(window_size)       # Window function
    bin_width = sr/window_size                   # Width of the frequency bins

    # Notes
    # (1700 - 4600) normally or (1800 - 5600 when dealing with Virtual rendering)
    # start_freq = 1700                        # frequency in Hz to start processing (1700 - 4600) or (500 - 2500)
    # stop_freq = 4600                         # frequency in Hz to stop processing

    # ILD Histogram Setup
    ILDstartbin = int(np.round(start_freq/bin_width))        # freq bin number to start processing
    ILDstopbin = int(np.round(stop_freq/bin_width))        # freq bin number to start processing

    ILDhist_size = hist_size   # Size of the histogram
    levelbinedges = np.linspace(-dB_range, dB_range, ILDhist_size + 1)
    levelbinwidth = levelbinedges[1] - levelbinedges[0]
    levelhist = np.zeros(ILDhist_size)

    # Complex STFT
    left = librosa.stft(input_file[0, :], hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)
    right = librosa.stft(input_file[1, :], hop_length=hop_size, n_fft=window_size, win_length=window_size, window=window_type)

    # Calculate Magnitude and trim according to start/stop bins
    left_mag = np.abs(left)[ILDstartbin:ILDstopbin, :]
    right_mag = np.abs(right)[ILDstartbin:ILDstopbin, :]

    # Get the number of bins and frames of the band-limited ILD spectrogram
    [numbins, numframes] = np.shape(ILD_spectra)

    # ILD_histogram Setup
    ILD_histogram = np.zeros((ILDhist_size, numframes))

    # Calculate Histogram
    for frame in range(numframes):

        ratios = ILD_spectra[:, frame]
        mag_weights = left_mag[:, frame] + right_mag[:, frame]

        if energyweighting == True:
            # weighted histogram
            levelhist, bin_edges = np.histogram(ratios, bins=levelbinedges-(levelbinwidth/2*0), weights=mag_weights)
        else:
            levelhist, bin_edges = np.histogram(ratios, bins=levelbinedges-(levelbinwidth/2))

        levelhist = levelhist**exponent          # Exponent to enhance peaks 

        if normalize == True:
            # Normalize the histogram to max value of 1
            levelhist = levelhist / np.max(levelhist)  

        ILD_histogram[:, frame] = levelhist         # Add frame to the ILD_histogram

        levelhist = np.zeros(ILDhist_size)          # Zero the histograms for next iteration

    if plots:
        xlimit = (0, ILD_histogram.shape[1])

        plot.rcParams.update({'font.size': 14})
        fig, axs = plot.subplots(1, 1, figsize=(8, 6))
        axs.imshow(ILD_histogram, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs.set_title('ILD Histogram')
        axs.set_ylabel('ILD Estimate (dB)')
        axs.set_xlabel('Time (frames)')
        axs.set_yticks([0, 100, 200, 300, 400])
        axs.set_yticklabels([f'{-dB_range}', f'{-dB_range/2}', '0', f'{dB_range/2}', f'{dB_range}'])
        axs.set_xlim(0, xlimit[1])
        axs.axhline(hist_size/2, color='white', linestyle='--', linewidth=0.7)
        

    return ILD_histogram

# Function to compare ITD Spectra
def ITD_sim(ref, test, sr, mode='signed', plots=False): 

    itd_spect_ref = ITD_spect(ref,sr)
    itd_spect_test = ITD_spect(test,sr)

    # If the 0 degree IR is not accurate, this compensates for asymetry 
    absdiff = np.abs(itd_spect_test) - np.abs(itd_spect_ref)
    absdiff = np.nan_to_num(absdiff, nan=0.0)

    diff = itd_spect_test - itd_spect_ref
    diff = np.nan_to_num(diff, nan=0.0)

    if mode == 'signed':
        dynamic_similarity = 1 - (np.abs((np.median(diff, axis=0)) * 1/0.00086))
    elif mode == 'unsigned':
        # If ref and test are more than 90 degrees apart, this doubles the range
        dynamic_similarity = 1 - (np.abs((np.median(diff, axis=0)) * 1/0.00086))
        dynamic_similarity = (dynamic_similarity +1)/2

    avg_similarity = np.median(dynamic_similarity)
    min_similarity = np.min(dynamic_similarity)

    if plots: 

        hist_size = 400

        itd_histogram_ref = ITD_hist(ref,sr)
        itd_histogram_test = ITD_hist(test,sr)

        fig, axs = plot.subplots(1, 3, figsize=(20, 5))
        axs[0].imshow(itd_histogram_ref, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[0].set_title('ITD Histogram Reference')
        axs[0].set_ylabel('Angle Estimate')
        axs[0].set_yticks([0, 100, 200, 300, 400])
        axs[0].set_yticklabels(['-90°', '-45°', '0°', '45°', '90°'])
        axs[0].set_xlim(0, hist_size)
        axs[1].imshow(itd_histogram_test, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[1].set_title('ITD Histogram Test')
        axs[1].set_yticks([0, 100, 200, 300, 400])
        axs[1].set_yticklabels(['-90°', '-45°', '0°', '45°', '90°'])
        axs[1].set_xlim(0, hist_size)
        axs[2].plot(dynamic_similarity)
        axs[2].set_title('Similarity (Mean = {:.2f}, Min = {:.2f})'.format(avg_similarity, min_similarity))
        axs[2].set_ylim(0, 1.05)
        axs[2].set_yticks([0, 0.25, 0.50, 0.75, 1])
        axs[2].set_yticklabels([0, 0.25, 0.50, 0.75, 1])
        axs[2].set_xlim(0, hist_size)
        

    return avg_similarity


# Function to compare ITD Spectra
def ILR_sim(ref, test, sr, mode='signed', plots=False): 

    ILR_spect_ref = ILR_spect(ref,sr, start_freq=1700, stop_freq=4600)
    ILR_spect_test = ILR_spect(test,sr, start_freq=1700, stop_freq=4600)

    #TODO add mag weighting

    # If the 0 degree IR is not accurate, this compensates for asymetry
    absdiff = np.abs(ILR_spect_test) - np.abs(ILR_spect_ref)
    absdiff = np.nan_to_num(absdiff, nan=0.0)

    diff = (ILR_spect_test - ILR_spect_ref)
    diff = np.nan_to_num(diff, nan=0.0)
    
    if mode == 'signed':
        dynamic_similarity = 1 - (np.abs((np.mean(diff, axis=0))))
    elif mode == 'unsigned':
        # If ref and test are more than 90 degrees apart, this doubles the range
        dynamic_similarity = 1 - (np.abs((np.mean(diff, axis=0))))
        dynamic_similarity = (dynamic_similarity +1)/2
    
    avg_similarity = (np.mean(dynamic_similarity))
    min_similarity = np.min(dynamic_similarity)

    if plots: 

        hist_size = 400
        ILR_histogram_ref = ILR_hist(ref,sr)
        ILR_histogram_test = ILR_hist(test,sr)

        fig, axs = plot.subplots(1, 3, figsize=(20, 5))
        axs[0].imshow(ILR_histogram_ref, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[0].set_title('ILR Histogram Reference')
        axs[0].set_ylabel('Angle Estimate')
        axs[0].set_yticks([0, 100, 200, 300, 400])
        axs[0].set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
        axs[0].set_xlim(0, hist_size)
        axs[1].imshow(ILR_histogram_test, cmap='danlab2', aspect='auto', origin='lower', interpolation='nearest')
        axs[1].set_title('ILR Histogram Test')
        axs[1].set_yticks([0, 100, 200, 300, 400])
        axs[1].set_xlim(0, hist_size)
        axs[1].set_yticklabels(['-1', '-0.5', '0', '0.5', '1'])
        axs[2].plot(dynamic_similarity)
        axs[2].set_title('Similarity (Mean = {:.2f}, Min = {:.2f})'.format(avg_similarity, min_similarity))
        axs[2].set_ylim(0, 1.05)
        axs[2].set_yticks([0, 0.25, 0.50, 0.75, 1])
        axs[2].set_yticklabels([0, 0.25, 0.50, 0.75, 1])
        axs[2].set_xlim(0, hist_size)
        
   

    return avg_similarity
