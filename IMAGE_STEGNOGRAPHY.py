from PIL import Image

# Function to encode a message into an image using LSB
def encode_image(image_path, message, output_path):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size

    # Check if the message can fit within the image
    if len(message) * 8 > width * height:
        raise Exception("Message is too long to be encoded in this image.")

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Add a sentinel value to mark the end of the message
    binary_message += '1111111111111110'  # This is a sentinel value (16 bits)

    message_index = 0

    # Traverse the image pixel by pixel and encode the message
    for x in range(width):
        for y in range(height):
            pixel = list(img.getpixel((x, y)))

            # Modify the least significant bit of each color channel
            for color_channel in range(3):  # Red, Green, and Blue
                if message_index < len(binary_message):
                    pixel[color_channel] = pixel[color_channel] & 0xFE | int(binary_message[message_index])
                    message_index += 1

            img.putpixel((x, y), tuple(pixel))

    # Save the encoded image
    img.save(output_path)

# Function to decode a message from an image using LSB
def decode_image(image_path):
    img = Image.open(image_path)
    width, height = img.size

    binary_message = ""

    # Traverse the image pixel by pixel and decode the message
    for x in range(width):
        for y in range(height):
            pixel = list(img.getpixel((x, y)))

            # Extract the least significant bit from each color channel
            for color_channel in range(3):
                binary_message += bin(pixel[color_channel])[-1]

    # Find the sentinel value to mark the end of the message
    sentinel = '1111111111111110'
    sentinel_index = binary_message.find(sentinel)

    if sentinel_index == -1:
        raise Exception("No sentinel value found in the image. Message may be incomplete or missing.")

    # Convert the binary message back to text
    decoded_message = ""
    binary_message = binary_message[:sentinel_index]  # Exclude the sentinel value
    for i in range(0, len(binary_message), 8):
        decoded_message += chr(int(binary_message[i:i + 8], 2))

    return decoded_message

# Example usage
if __name__ == '__main__':
    image_path = 'steg.jpg'
    message = 'Information Security'
    encoded_image_path = 'encoded_image.png'

    # Encode the message into the image
    encode_image(image_path, message, encoded_image_path)
    print("Successfully Encoded the data into the image file!!")

    # Decode the message from the encoded image
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)
