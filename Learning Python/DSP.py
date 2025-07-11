import sounddevice as sd  
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
def main():
    duration = 5
    fs = 44100
    device_index = 1
    my_recording = record_audio(duration, fs, device_index)  
    play_audio(my_recording, fs)
    sf.write('output.wav', my_recording, fs)
    plot_waveform_and_fft(my_recording, fs)
    
def record_audio(duration, fs, device_index):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2,dtype='float32', device=device_index)
    sd.wait()
    print("Done Recording.")
    return recording

def play_audio(myrecording, fs):
    sd.play(myrecording, fs)
    sd.wait()
    sd.stop()
   
def plot_waveform_and_fft(audio, fs):
    # Mono channel
    if audio.ndim > 1:
        audio = audio[:, 0]

    num_samples = len(audio)
    t = np.linspace(0, num_samples / fs, num=num_samples)

    # --- Create subplots ---
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))  # 2 rows, 1 column

    # --- Waveform plot ---
    axs[0].plot(t, audio)
    axs[0].set_title("Audio Waveform")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Amplitude")
    axs[0].grid(True)

    # --- FFT plot ---
    windowed = audio * np.hamming(len(audio))
    fft = np.fft.rfft(windowed)
    freqs = np.fft.rfftfreq(len(windowed), d=1/fs)
    magnitude = np.abs(fft)

    axs[1].plot(freqs, magnitude)
    axs[1].set_title("Frequency Spectrum (FFT)")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel("Magnitude")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()    

if __name__ == '__main__':
    main()
    