from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import numpy as np
import wave
from hashlib import sha1

# Function to pad the data to be a multiple of 8 bytes
def pad(data):
    return data + b"\0" * (8 - len(data) % 8)

def generate_key(key):
    # make the key 8 bytes long using sha1
    key = sha1(key.encode()).digest()[:8]
    return key

# Function to encrypt audio samples
def encrypt_audio(input_audio_path, output_audio_path, key):
    des = DES.new(generate_key(key), DES.MODE_ECB)

    # Open the audio file
    input_wave = wave.open(input_audio_path, 'rb')

    # Get audio parameters
    sample_width = input_wave.getsampwidth()
    num_channels = input_wave.getnchannels()
    frame_rate = input_wave.getframerate()

    # Read audio samples
    audio_samples = input_wave.readframes(-1)
    input_wave.close()

    # Convert audio samples to NumPy array
    audio_array = np.frombuffer(audio_samples, dtype=np.int16)

    # Pad the data if needed
    audio_array_bytes = pad(audio_array.tobytes())

    # Encrypt the audio samples
    encrypted_data = des.encrypt(audio_array_bytes)

    # Create a new audio file from the encrypted samples
    output_wave = wave.open(output_audio_path, 'wb')
    output_wave.setsampwidth(sample_width)
    output_wave.setnchannels(num_channels)
    output_wave.setframerate(frame_rate)
    output_wave.writeframes(encrypted_data)
    output_wave.close()

# Function to decrypt audio samples
def decrypt_audio(encrypted_audio_path, output_audio_path, key):
    des = DES.new(generate_key(key), DES.MODE_ECB)

    # Open the encrypted audio file
    encrypted_wave = wave.open(encrypted_audio_path, 'rb')

    # Get audio parameters
    sample_width = encrypted_wave.getsampwidth()
    num_channels = encrypted_wave.getnchannels()
    frame_rate = encrypted_wave.getframerate()

    # Read encrypted audio samples
    encrypted_samples = encrypted_wave.readframes(-1)
    encrypted_wave.close()

    # Decrypt the audio samples
    decrypted_data = des.decrypt(encrypted_samples)

    # Convert decrypted audio samples to NumPy array
    decrypted_array = np.frombuffer(decrypted_data, dtype=np.int16)

    # Create a new audio file from the decrypted samples
    output_wave = wave.open(output_audio_path, 'wb')
    output_wave.setsampwidth(sample_width)
    output_wave.setnchannels(num_channels)
    output_wave.setframerate(frame_rate)
    output_wave.writeframes(decrypted_array.tobytes())
    output_wave.close()
    
encrypt_audio("audio.wav", "encrypted_audio.wav", "password")
decrypt_audio("encrypted_audio.wav", "decrypted_audio.wav", "password")