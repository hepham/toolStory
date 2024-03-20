import os
from PIL import Image
import imagehash

def calculate_hash(image_path):
    with Image.open(image_path) as img:
        # Resize the image to a fixed size for consistency
        # Convert the image to grayscale
        grayscale_img = img.convert('L')
        # Calculate the perceptual hash
        return imagehash.average_hash(grayscale_img)

def find_and_remove_duplicates(folder_path):
    hash_dict = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, filename)
            image_hash = calculate_hash(file_path)

            # Check if the hash already exists (duplicate)
            if image_hash in hash_dict:
                print(f"Removing duplicate: {filename}")
                os.remove(file_path)
            else:
                # Store the hash in the dictionary
                hash_dict[image_hash] = file_path

if __name__ == "__main__":
    folder_path = "canvas"
    find_and_remove_duplicates(folder_path)
