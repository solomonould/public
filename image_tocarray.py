import requests
from PIL import Image
import io

# Function to download and resize the image
def download_and_resize_image(url, width, height):
    response = requests.get(url)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content))
    image = image.resize((width, height))
    return image

# Function to convert the image to 16bpp format (RGB565)
def image_to_16bpp(image):
    image_data = list(image.getdata())
    pixels_16bpp = [(r >> 3) << 11 | (g >> 2) << 5 | (b >> 3) for r, g, b in image_data]
    return pixels_16bpp

# Function to generate the C array string
def generate_array_string(array, bytes_per_element):
    array_string = "const unsigned char rasp[{}] = {{\n".format(len(array) * bytes_per_element)
    for value in array:
        for i in range(bytes_per_element):
            array_string += "0x{:02X}, ".format((value >> (8 * i)) & 0xFF)
    array_string = array_string[:-2]  # Remove the trailing comma and space
    array_string += "\n};"
    return array_string

def main():
    # URL of the image you want to download and display
    image_url = "https://www.amgc.org.au/wp-content/uploads/gravity_forms/3-728f303a3a9e62dcc8edcf5b26e0f9b2/2020/05/Packserv-Logo-002.jpg"

    # Target resolution for the image (800x480)
    target_width = 800
    target_height = 480

    try:
        # Download and resize the image
        image = download_and_resize_image(image_url, target_width, target_height)

        # Convert the image to 16bpp format (RGB565)
        pixels_16bpp = image_to_16bpp(image)

        # Generate the C array string for 768,000 elements (16-bit values)
        array_string = generate_array_string(pixels_16bpp, bytes_per_element=2)

        # Save the C array to a file
        with open("1.h", "w") as file:
            file.write(array_string)

        print("Image converted and saved as '1.h'")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
