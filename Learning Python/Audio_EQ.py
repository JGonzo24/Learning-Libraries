import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
from scipy.io.wavfile import write
import sounddevice as sd
from scipy.fft import fft, fftfreq
def butter_filter(cutoff, fs, btype='low', order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return b, a

def apply_filter(data, cutoff, fs, btype='low', order=4):
    b, a = butter_filter(cutoff, fs, btype=btype, order=order)
    return lfilter(b, a, data)

def plot_fft(signal, fs, label):
    N = len(signal)
    freqs = fftfreq(N, 1/fs)[:N//2]           # Frequencies (only positive half)
    spectrum = np.abs(fft(signal))[:N//2]     # Magnitude of FFT (positive half only)
    
    plt.plot(freqs, spectrum, label=label)


fs = 44100
t = np.linspace(0, 2.0, int(fs*2), endpoint=False)
signal = np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 300 * t) + 0.2 * np.sin(2 * np.pi * 600 * t)

bass = apply_filter(signal, 150, fs, btype='low')
mid = apply_filter(apply_filter(signal, 490, fs, 'low'), 150, fs, 'high')
treble = apply_filter(signal, 490, fs, 'high')

# Combine with different gains
equalized=  1.0 * bass + 0.5 * mid + 5.0 * treble # Boost treble 
# Normalize to -1 to 1
equalized_norm = equalized / np.max(np.abs(equalized))

# Convert to 16-bit PCM format
equalized_int16 = (equalized_norm * 32767).astype(np.int16)
sd.play(equalized_norm, fs)
sd.wait()
# Save to WAV
write("equalized_output.wav", fs, equalized_int16)

plt.figure(figsize=(10, 6))
plot_fft(signal, fs, "Original")
plot_fft(bass, fs, "Bass")
plot_fft(mid, fs, "Mid")
plot_fft(treble, fs, "Treble")
plt.title("Frequency Spectrum of Signals (FFT)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

