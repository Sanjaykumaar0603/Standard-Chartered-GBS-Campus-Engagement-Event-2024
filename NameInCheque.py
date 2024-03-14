import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import cv2
import easyocr

# Load the pre-trained OCR reader
reader = easyocr.Reader(['en'])

# Load the input image
image = cv2.imread("copped/Cheque309158/2_0.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Perform text detection
result = reader.readtext(gray, detail=0, paragraph=False)

# Extract and print the detected text (considering only handwritten text)
for text in result:
    print("Detected text:", text)

# Display the output image
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
