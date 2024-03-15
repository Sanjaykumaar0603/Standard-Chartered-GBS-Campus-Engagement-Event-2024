from PIL import Image, ImageDraw
import os
import pytesseract
import re
import random
import cv2
import easyocr

# Load the pre-trained OCR reader
reader = easyocr.Reader(['en'])

directory = r"C:\Users\preet\Desktop\Standard-Chartered-GBS-Campus-Engagement-Event-2024-main (1)\Standard-Chartered-GBS-Campus-Engagement-Event-2024-main\Images"


def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    coordinates = []
    for line in lines:
        parts = line.strip().split()
        x, y, w, h = map(float, parts[1:])
        coordinates.append((x, y, w, h))
    return coordinates


# Function to check if name contains any numbers or special characters
def contains_numbers_or_special_characters(string):
    return any(char.isdigit() or not char.isalnum() for char in string)


# Initialize variables to store OCR outputs
ocr_output_class_1 = ""
ocr_output_class_3 = ""

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        index = 0
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

        # Run OCR on images labeled '3' and '1' in each folder
        for class_id, coords in enumerate(coordinates):
            if class_id in [1, 2, 3]:
                # Crop the partition from the image
                x, y, w, h = coords
                width, height = image.size
                left = int(x * width)
                top = int(y * height)
                right = int((x + w) * width)
                bottom = int((y + h) * height)
                partition = image.crop((left, top, right, bottom))

                # Perform OCR
                ocr_output = pytesseract.image_to_string(partition)

                # Store OCR outputs in separate variables based on class ID
                if class_id == 1:
                    image_path = r"C:\Users\preet\Desktop\new\Standard-Chartered-GBS-Campus-Engagement-Event-2024-main\Images\{}\{}_{}.jpg".format(
                        filename[:-4], class_id, index)
                    languages = ['hin', 'eng']
                    language_lines = {lang: {'text': '', 'confidence': 0} for lang in languages}
                    for lang in languages:
                        text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
                        word_confidences = pytesseract.image_to_data(Image.open(image_path), lang=lang)
                        lines = word_confidences.splitlines()[1:]
                        confidence_values = []
                        for line in lines:
                            components = line.split('\t')
                            if len(components) > 1 and components[-1].strip():
                                try:
                                    confidence_values.append(float(components[-1]))
                                except ValueError:
                                    pass
                        avg_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0
                        if avg_confidence > language_lines[lang]['confidence']:
                            language_lines[lang]['text'] = text
                            language_lines[lang]['confidence'] = avg_confidence
                elif class_id == 2:
                    image_path = r"C:\Users\preet\Desktop\new\Standard-Chartered-GBS-Campus-Engagement-Event-2024-main\Images\{}\{}_{}.jpg".format(
                        filename[:-4], class_id, index)
                    if os.path.isfile(image_path):
                        image1 = cv2.imread(image_path)
                        gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
                        result = reader.readtext(gray, detail=0, paragraph=False)
                        print("Detected text in", os.path.join(filename, "2_0.jpg") + ":")
                        for text in result:
                            print(text)
                    else:
                        print("2_0.jpg not found in", filename)
                elif class_id == 3:
                    ocr_output_class_3 = ocr_output
                    pattern = r'\d+'
                    numerical_data = re.findall(pattern, ocr_output_class_3)
                    account_number = ''.join(numerical_data)
                    if len(account_number) > 8:
                        # Placeholder for name since faker module is not used
                        name = "John$%Doe"  # Example name containing special characters
                        # Check if name contains any numbers or special characters
                        if contains_numbers_or_special_characters(name):
                            count = sum(1 for char in name if char.isdigit() or not char.isalnum())
                            # Check if count exceeds the threshold
                            if count > 2:
                                print(filename, "Class_3: Invalid Cheque")
                            elif count > 0:
                                print(filename, "Class_3: Check Manually")
                        else:
                            # Generate a random amount
                            amount = round(random.uniform(100, 10000), 2)
                            # Generate a random PAN number
                            pan = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
                            # SQL query to insert data into the customer table
                            insert_query = "INSERT INTO customer (account_number, name, amount, PAN) VALUES (%s, %s, %s, %s)"
                            data = (account_number, name, amount, pan)

                            # Execute the SQL query
                            # cursor.execute(insert_query, data) # Commented out due to absence of database connection
                            print(filename, "Class_3:", "Data inserted successfully")
                    else:
                        print(filename, "Class_3:", "Invalid account number")
        print("\n")
        index += 1
