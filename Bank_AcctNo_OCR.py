from PIL import Image, ImageDraw
import os
import pytesseract
import re
import random
import faker
import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='sch'
)

fake = faker.Faker()
cursor = connection.cursor()
directory = "Images/"

def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    coordinates = []
    for line in lines:
        parts = line.strip().split()
        x, y, w, h = map(float, parts[1:])
        coordinates.append((x, y, w, h))
    return coordinates

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
            if class_id in [1, 3]:
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
                
                # Print OCR output
                # print(f"OCR Output for {filename}_{class_id}.jpg:")
                # print(ocr_output)

                # Store OCR outputs in separate variables based on class ID
                if class_id == 1:
                    image_path = r"C:\Users\S Karun Vikhash\Downloads\SCHack\self\Images\{}\{}_{}.jpg".format(filename[:-4], class_id, index)
                    # ocr_output_class_1 = ocr_output
                    # print(filename, "Class_1: ", ocr_output_class_1)
                    # Define languages
                    languages = ['hin', 'eng']

                    # Initialize confidence scores for each language
                    language_lines = {lang: {'text': '', 'confidence': 0} for lang in languages}

                    # Iterate over languages
                    for lang in languages:
                        # Perform OCR for each language
                        text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
                        # Calculate confidence score (average confidence of all words)
                        word_confidences = pytesseract.image_to_data(Image.open(image_path), lang=lang)
                        # Split the output into lines and skip the header
                        lines = word_confidences.splitlines()[1:]
                        # Extract the confidence scores and convert them to floats
                        confidence_values = []
                        for line in lines:
                            components = line.split('\t')
                            if len(components) > 1 and components[-1].strip():
                                try:
                                    confidence_values.append(float(components[-1]))
                                except ValueError:
                                    pass
                        # Calculate the average confidence score
                        avg_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0
                        # Update the language lines if the confidence score is higher
                        if avg_confidence > language_lines[lang]['confidence']:
                            language_lines[lang]['text'] = text
                            language_lines[lang]['confidence'] = avg_confidence

                    # Check if Hindi has the highest confidence score
                    if language_lines['hin']['confidence'] > language_lines['eng']['confidence']:
                        print("Hindi Text:")
                        print(language_lines['hin']['text'].split("\n")[0])
                        print(language_lines['eng']['text'].split("\n")[1])
                    else:
                        print("English Text:")
                        print(language_lines['eng']['text'])

                elif class_id == 3:
                    ocr_output_class_3 = ocr_output
                    # # Define a regex pattern to match numerical data
                    pattern = r'\d+'
                    # Find all numerical matches in the OCR output
                    numerical_data = re.findall(pattern, ocr_output_class_3)

                    # Remove whitespace and join the numerical data
                    account_number = ''.join(numerical_data)
                    if len(account_number)>8:
                        print(filename, "Class_3:", account_number)
                        # Generate a random name
                        name = fake.name()
                        # Generate a random amount
                        amount = round(random.uniform(100, 10000), 2)
                        # Generate a random PAN number
                        pan = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
                        # SQL query to insert data into the customer table
                        insert_query = "INSERT INTO customer (account_number, name, amount, PAN) VALUES (%s, %s, %s, %s)"
                        data = (account_number, name, amount, pan)

                        # Execute the SQL query
                        cursor.execute(insert_query, data)

                        
                    else:
                        print(filename, "Class_3:", "Invalid account number")
        print("\n")
        index+=1
                    
