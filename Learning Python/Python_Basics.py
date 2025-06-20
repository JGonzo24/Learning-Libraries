import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import butter, lfilter
from scipy.fft import fft, fftfreq

def plot_fft(signal, fs, label):
    N = len(signal)
    freqs = fftfreq(N, 1/fs)[:N//2]
    spectrum = np.abs(fft(signal)) [:N//2]
    plt.plot(freqs, spectrum, label=label)
def section1():
    t = np.linspace(0, 1, 1000)
    signal = 0.5 * np.sin(2 * np.pi * 50 * t)
    
    # 1a. Create a 2D array of sinuoids at different frequencies (50Hz, 150Hz, 300 Hz) using broadcasting
    freqs = np.array([100, 150, 300, 400])
    col_vec = freqs.reshape(-1,1)
    broadcast = col_vec * t 
    sinusoids = np.sin(2*np.pi*broadcast)
    
    # 1b. Slice every other column and plot them
    slices = sinusoids[:, ::2]
    plt.figure(figsize= (10,6))
    for i, f in enumerate(freqs):
        plt.plot(t[::2], slices[i], label=f"{f} Hz")
        
    # 2a. Multiply each row in a 2D array by a 1D Hamming Winow using broadcasting
    window = np.hamming(1000)
    windowed_function = window * sinusoids
    
    # 3a Slice a subarray, modify it, and check if the original changed (to test view vs. copy)
    subarray = sinusoids[0]
    subarray_copy = sinusoids[0].copy()
    
    subarray[0:10] = 999 
    subarray_copy[0:10] = -999
    
    print("Original sinusoids[0][0:10]:", sinusoids[0][0:10])
    print("Copy modified [0:10]: ", subarray_copy[0:10])
       
    plt.title("Sinusiods with every other column sampled")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()
        
    

def section2():
    # Record a sound clip and compute the FFT using
    fs = 1000 # 1kHz sampling rate
    t = np.linspace(0, 1, fs, endpoint=False)
    signal = np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2*np.pi * 250 * t)
    window = np.hamming(len(signal))
    windowed = window * signal
    fft = np.fft.rfft(windowed)
    freqs = np.fft.rfftfreq(len(signal), 1/fs)

    magnitude = np.abs(fft) / (np.sum(window)/2)
    plt.plot(freqs,magnitude)
    
    plt.title("FFT of synthetic 100 Hz + 250 Hz signal")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()
     
def section3():
    fs = 1000
    t = np.linspace(0, 1, fs, endpoint=False)
    signal = 0.5 * np.sin(2 * np.pi * 250 * t) + np.sin(2 * np.pi * 50 * t)
    
    # Design the butter worth lowpass filter with a cutoff of 150 hz
    cutoff = 150
    N = 4 # Order of the filter
    Wn = cutoff / (fs / 2) # Cutoff frequency normalized to the nyquist 
    b_low,a_low = butter(N, Wn, btype='low') # low pass
    b_high,a_high= butter(N, Wn, btype='high') # High pass
    b_band,a_band = butter(N, Wn = [0.2, 0.5], btype='band') # Band pass
    
    # Apply the filter to the signal
    filtered_low = lfilter(b_low, a_low, signal)
    
    
    # plot the fft to see that it is working as well
    plt.figure(figsize=(10,4))
    plt.plot(t,signal,label='Original')
    plt.plot(t, filtered_low, label='Low-pass Filtered', linewidth = 2)
    plt.legend()
    plt.gcf().canvas.mpl_connect('pick_event', lambda event: event.artist.set_visible(not event.artist.get_visible()))

    plt.xlabel('Time[s]')
    plt.title('Time Domain: Original vs Filtered')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(10,4))
    plot_fft(signal, fs, label='Original')
    plot_fft(filtered_low, fs, label='Filtered (low-pass)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Frequency Domain (FFT)')
    plt.legend()
    plt.gcf().canvas.mpl_connect('pick_event', lambda event: event.artist.set_visible(not event.artist.get_visible()))

    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
   
    
def main():
    # section1() 
    # section2()
    section3()

if __name__ == "__main__":
    main()
    