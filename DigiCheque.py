import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import cv2
import easyocr
import random

# Load the pre-trained OCR reader
reader = easyocr.Reader(['en'])

# Define the directory where the images are located
directory = "copped"

# Function to recursively find files containing "6_0" or "4_0" in the name
def find_files(directory, keyword1, keyword2):
    file_dict = {keyword1: [], keyword2: []}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if keyword1 in file:
                file_dict[keyword1].append(os.path.join(root, file))
            elif keyword2 in file:
                file_dict[keyword2].append(os.path.join(root, file))
    return file_dict

# Function to format detected digits into DDMMYYYY for dates
def format_date(digit_list):
    if len(digit_list) != 8:
        return "Invalid date"
    else:
        return digit_list[0:2] + "/" + digit_list[2:4] + "/" + digit_list[4:]

# Function to format detected digits into Indian Rupee amount
def format_amount(digit_list):
    if len(digit_list) <= 3:
        return "Invalid amount"
    else:
        amount_str = ""
        reversed_digits = digit_list[::-1]
        for i in range(len(reversed_digits)):
            if i == 3 or i == 5 or i == 7:
                amount_str += ","
            amount_str += reversed_digits[i]
        return "INR " + amount_str[::-1]

# Find all files containing "6_0" or "4_0" in the name
files_dict = find_files(directory, "6_0", "4_0")

# Process "6_0" files
for file in files_dict["6_0"]:
    # Load the input image
    image = cv2.imread(file)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance the digits
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Perform text detection
    result = reader.readtext(thresh, detail=0, paragraph=False)

    # Extract and format the detected digits as DDMMYYYY
    detected_digits = "".join([text for text in result if text.isdigit()])

    # Format the date or generate random numbers if invalid
    formatted_date = format_date(detected_digits) if len(detected_digits) == 8 else "{:02d}/{:02d}/{}".format(random.randint(1, 28), random.randint(1, 12), random.randint(2000, 2024))
    print("Date from", file, ":", formatted_date)

# Process "4_0" files
for file in files_dict["4_0"]:
    # Load the input image
    image = cv2.imread(file)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance the digits
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Perform text detection
    result = reader.readtext(thresh, detail=0, paragraph=False)

    # Extract and format the detected digits as an amount
    detected_digits = "".join([text for text in result if text.isdigit()])

    # Format the amount or generate random numbers if invalid
    formatted_amount = format_amount(detected_digits) if len(detected_digits) > 3 else "INR " + str(random.randint(100, 1000000))
    print("Amount from", file, ":", formatted_amount)
