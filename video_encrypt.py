import moviepy.editor as mp
import numpy as np
from io import BytesIO
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import numpy as np
import wave
from image_encrypt import pad, encrypt_image, decrypt_image

def encrypt_audio(input_audio_path, key):
    des = DES.new(key, DES.MODE_ECB)

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
    
    return encrypted_data

# Function to decrypt audio samples
def decrypt_audio(encrypted_audio_path, key):
    des = DES.new(key, DES.MODE_ECB)

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

    return decrypted_array

# Step 1: Extract audio and images
video_path = 'input_video.mp4'

video_clip = mp.VideoFileClip(video_path)
audio_clip = video_clip.audio
audio_bytes = BytesIO()
audio_clip.write_audiofile(audio_bytes, fps=44100, nbytes=2)

# Save images from video frames to a list
frame_images = []

for frame in video_clip.iter_frames(fps=30, dtype='uint8'):
    frame_images.append(frame)

# Perform operations on images and audio
# For example, let's add a watermark to each frame and apply an audio effect.
def process_image(image,key):
    # Add a watermark to the image
    result = encrypt_image(image, key)
    return result

# Process each image
processed_images = [process_image(mp.ImageClip(image, duration=1 / 30)) for image in frame_images]

# Apply audio effects
def process_audio(audio):
    new_audio = encrypt_audio(audio)
    return audio.volumex(2.0)  # Adjust the volume level as needed

processed_audio = process_audio(mp.AudioFileClip(audio_bytes))

# Step 2: Reassemble processed audio and images into a video
new_video_path = 'output_video.mp4'

video_clip = mp.concatenate_videoclips(processed_images, method="compose")
video_clip = video_clip.set_audio(processed_audio)
video_clip.write_videofile(new_video_path, fps=30)

# Clean up
audio_clip.close()
video_clip.close()
