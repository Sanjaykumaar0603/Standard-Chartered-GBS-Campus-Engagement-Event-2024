#Cropping the images according to ROI

from PIL import Image, ImageDraw
import os

def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    coordinates = []
    for line in lines:
        parts = line.strip().split()
        x, y, w, h = map(float, parts[1:])
        coordinates.append((x, y, w, h))
    return coordinates

def crop_and_save_partition(image, coordinates, class_id, output_directory):
    for idx, coord in enumerate(coordinates):
        x, y, w, h = coord
        width, height = image.size
        left = int(x * width)
        top = int(y * height)
        right = int((x + w) * width)
        bottom = int((y + h) * height)

        # Crop the partition
        partition = image.crop((left, top, right, bottom))

        # Save the partition in the output directory
        partition.save(os.path.join(output_directory, f"{class_id}_{idx}.jpg"))

# Path to the directory containing images and text files
directory = "Images/"

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        image_path = os.path.join(directory, filename)
        txt_path = os.path.join(directory, filename[:-4] + ".txt")
        
        # Check if the corresponding txt file exists
        if not os.path.exists(txt_path):
            print(f"Corresponding txt file not found for {filename}")
            continue
        
        # Load the image
        image = Image.open(image_path)

        # Read coordinates from the txt file
        coordinates = read_coordinates(txt_path)

        # Create a new directory for the current image
        output_directory = os.path.join(directory, filename[:-4])
        os.makedirs(output_directory, exist_ok=True)

        # Crop partitions and save them in the new directory
        for class_id, coords in enumerate(coordinates):
            crop_and_save_partition(image.copy(), [coords], class_id, output_directory)
