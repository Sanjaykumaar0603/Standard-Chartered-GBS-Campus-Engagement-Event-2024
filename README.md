# Standard-Chartered-GBS-Campus-Engagement-Event-2024

##Introduction
We are able to process multi lingual languages like hindi, english, tamil, etc using tesseract OCR
<a href>Link for Tesseract OCR</a>

## OBJECTIVE:

1. Reading Cheque Information (OCR)
2. Verifying Signatures
3. Checking Technical Details
4. Handling Different Languages
5. Automating the Process
6. Detecting Fraud
7. Testing and Improvement

<p align="center"><img src ="doc/imgs/cheuqedum.jpeg?raw=true" height="340" alt="Sublime's custom image" /></p>

## Program Structure
1) According to <a href = "https://rbidocs.rbi.org.in/rdocs/content/PDFs/SCFR220210.pdf">CTS-10 standard </a> we are clipping the region of interest from the cheques to reduce the noise and to improve the processing speed
2) We are using tesseract OCR for recognizing printed text(such as Bank Name, Account number, Bank Details etc.) in the cheque image.
3) we are utilizing Histogram of Oriented Gradients (HOG) descriptors and cosine similarity for feature extraction and comparison, respectively, to detect and authenticate signatures in bank cheque images.
4) We are using easyocr for recognizing handwriting and digits to get the Reciever's name, amount, date.
5) For Fraudulent detection, we validate the Signature, Date, "Stop Cheque" and Cheque Number.
6) The cheque Number is retrieved from MICR code
7) MICR code is retrieved using image processing and segmentation
8) If the cheque is valid, then the information is printed else it is rejected if it meets any one of the fraudulent criteria,.
9) All the details are stored in the database and are continuously updated.
10) For auditing, we provide feature of generating QR code for the generated text OCR, to prevent tampering.

## How to run

## Dependencies 
pip install the following modules:
1. os
2. pytesseract
3. re
4. random
5. cv2
6. easyocr
7. ssl
8. mysql.connector
9. numpy
10. cosine_similarity
11. face_recognition
12. sklearn

## Dataset
Retrieved dataset from kaggle.

## Accuracy
The system is able to process 70-80% of the cheques including the rejected cheques.
