import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import cv2
import easyocr

# Load the pre-trained OCR reader
reader = easyocr.Reader(['en'])

# Load the input image
image = cv2.imread("copped/Cheque309158/6_0.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to enhance the digits
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Perform text detection
result = reader.readtext(thresh, detail=0, paragraph=False)

# Extract and print the detected digits
detected_digits = []
for text in result:
    if text.isdigit():  # Check if the detected text is a digit
        detected_digits.append(text)
        print("Detected digit:", text)

# Display the output image
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
