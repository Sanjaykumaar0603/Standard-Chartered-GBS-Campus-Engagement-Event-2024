import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import cv2
import easyocr
tc=0#total count words
tt=0#total text
cc=0#correct count (True Positive)
wc=0#wrong count (True Negative)
# Load the pre-trained OCR reader
reader = easyocr.Reader(['en'])

# Define the directory where the images are located
directory = "copped"

# Function to recursively find folders containing "2_0" files
def find_folders(directory, keyword):
    folder_list = []
    for root, dirs, files in os.walk(directory):
        if any(keyword in file for file in files):
            folder_list.append(root)
    return folder_list

# Find all folders containing "2_0" files
folders = find_folders(directory, "2_0")

# Process each folder
for folder in folders:
    print("Processing folder:", folder)
    # Iterate through files in the folder
    for file in os.listdir(folder):
        if "2_0" in file:
            # Load the input image
            image = cv2.imread(os.path.join(folder, file))
            
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Perform text detection
            result = reader.readtext(gray, detail=0, paragraph=False)
            tc=tc+1
            # Extract and print the detected text (considering only handwritten text)
            for text in result:
                tt=tt+1
                if(text.isalpha()):
                    print("Detected text in", os.path.join(folder, file), ":", text)
                    cc=cc+1
                else:
                    wc=wc+1
print("Total COUNT Images : ",tc)
print("Total COUNT words : ",tt)
print("Correct COUNT : ",cc)
print("Wrong COUNT : ",wc)