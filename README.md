# Standard-Chartered-GBS-Campus-Engagement-Event-2024

## OBJECTIVE:

1. Reading Cheque Information (OCR)
2. Verifying Signatures
3. Checking Technical Details
4. Handling Different Languages
5. Automating the Process
6. Detecting Fraud
7. Testing and Improvement

## Program Structure
1) According to CTS-10 standard we are clipping the region of interest from the cheques to reduce the noise and to improve the processing speed
2) We are using tesseract OCR for recognizing printed text(such as Bank Name, Account number, Bank Details etc.) in the cheque image.
3) we are utilizing Histogram of Oriented Gradients (HOG) descriptors and cosine similarity for feature extraction and comparison, respectively, to detect and authenticate signatures in bank cheque images.
4) We are using easyocr for recognizing handwriting and digits to get the Reciever's name, amount, date.
5) For Fraudulent detection, we validate the Signature, Date, "Stop Cheque" and Cheque Number.
6) The cheque Number is retrieved from MICR code
7) MICR code is retrieved using image processing and segmentation
8) If the cheque is valid, then the information is printed else it is rejected if it meets any one of the fraudulent criteria,.
9) All the details are stored in the database and are continuously updated.
10) For auditing, we provide feature of generating QR code for the generated text OCR, to prevent tampering.

