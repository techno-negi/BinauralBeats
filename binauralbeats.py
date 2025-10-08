import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import os

class BinauralBeatGenerator:
    def __init__(self, duration=10, sample_rate=44100, output_dir="binaural_beats"):
        self.duration = duration  # seconds
        self.sample_rate = sample_rate  # samples per second
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_tone(self, freq_left, freq_right):
        """
        Generate stereo binaural beat tone: base freq in left ear, base+beat freq in right ear.
        """
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        left = np.sin(2 * np.pi * freq_left * t)
        right = np.sin(2 * np.pi * freq_right * t)
        stereo = np.vstack((left, right)).T
        # Normalize to int16 range
        stereo *= 32767 / np.max(np.abs(stereo))
        return stereo.astype(np.int16)

    def play(self, base_freq, beat_freq):
        """
        Play binaural beat with given base frequency and beat frequency.
        """
        freq_left = base_freq
        freq_right = base_freq + beat_freq
        tone = self.generate_tone(freq_left, freq_right)
        sd.play(tone, self.sample_rate)
        sd.wait()

    def save(self, base_freq, beat_freq, filename):
        """
        Save binaural beat to WAV file.
        """
        freq_left = base_freq
        freq_right = base_freq + beat_freq
        tone = self.generate_tone(freq_left, freq_right)
        filepath = os.path.join(self.output_dir, filename)
        write(filepath, self.sample_rate, tone)
        print(f"Saved binaural beat to {filepath}")

if __name__ == "__main__":
    generator = BinauralBeatGenerator(duration=15)  # 15 seconds each

    brainwave_bands = {
        "Delta": 1.5,   # Hz
        "Theta": 5,
        "Alpha": 10,
        "Beta": 20,
        "Gamma": 40
    }
    base_frequency = 200  # Hz

    for band, beat in brainwave_bands.items():
        print(f"Playing {band} binaural beat at {beat} Hz...")
        generator.play(base_frequency, beat)
        filename = f"{band}_binaural_{beat}Hz.wav"
        generator.save(base_frequency, beat, filename)
        print(f"Finished {band}.")
