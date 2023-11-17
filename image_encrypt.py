from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import numpy as np
from PIL import Image

# Function to pad the data to be a multiple of 8 bytes
def pad(data):
    return data + b"\0" * (8 - len(data) % 8)

# Function to encrypt pixel values in an image
def encrypt_image(input_image_path, output_image_path, key):
    des = DES.new(key, DES.MODE_ECB)

    # Open the image and convert it to a NumPy array
    image = Image.open(input_image_path)
    image_array = np.array(image)

    # Record the shape of the original image
    original_shape = image_array.shape

    # Flatten the array and convert it to bytes
    flattened_array = image_array.flatten().tobytes()

    # Pad the data if needed
    flattened_array = pad(flattened_array)

    # Encrypt the pixel values
    encrypted_data = des.encrypt(flattened_array)

    # Create a new image from the encrypted pixel values
    encrypted_image_array = np.frombuffer(encrypted_data, dtype=np.uint8)

    # Reshape the encrypted data to match the size of the original image
    encrypted_image_array = encrypted_image_array[:image_array.size]
    encrypted_image_array = encrypted_image_array.reshape(original_shape)

    encrypted_image = Image.fromarray(encrypted_image_array)

    # Save the encrypted image in a common format like PNG
    encrypted_image.save(output_image_path, "PNG")

# Function to decrypt pixel values in an image
def decrypt_image(encrypted_image_path, output_image_path, key):
    des = DES.new(key, DES.MODE_ECB)

    # Open the encrypted image
    encrypted_image = Image.open(encrypted_image_path)
    encrypted_image_array = np.array(encrypted_image)

    # Flatten the array and convert it to bytes
    flattened_array = encrypted_image_array.flatten().tobytes()

    # Decrypt the pixel values
    decrypted_data = des.decrypt(flattened_array)

    # Create a new image from the decrypted pixel values
    decrypted_image_array = np.frombuffer(decrypted_data, dtype=np.uint8)

    # Reshape the decrypted data to match the size of the original image
    decrypted_image_array = decrypted_image_array[:encrypted_image_array.size]
    decrypted_image_array = decrypted_image_array.reshape(encrypted_image_array.shape)

    decrypted_image = Image.fromarray(decrypted_image_array)

    # Save the decrypted image in the original format (you might need to specify the format)
    decrypted_image.save(output_image_path)

# Example usage:
input_image_path = "pxfuel.jpg"
output_encrypted_image_path = "encrypted_image.png"
output_decrypted_image_path = "decrypted_image.png"

# Generate a random 8-byte key (DES key size)
key = get_random_bytes(8)
print(key)

encrypt_image(input_image_path, output_encrypted_image_path, key)
decrypt_image(output_encrypted_image_path, output_decrypted_image_path, key)
