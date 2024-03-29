# Standard-Chartered-GBS-Campus-Engagement-Event-2024


## Demonstation Video
The demo video is uploaded as ChequeVissionApp.mp4 in the Video & PPT folder. Click on "View Raw" to download and view the video.
For details refer ReadMe EOF 


## Introduction
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

<p align="center"><img src ="https://repository-images.githubusercontent.com/273438480/c3235400-c851-11ea-9011-4c77828502cf" height="340" alt="Sublime's custom image" /></p>

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
NameInCheque.py - Change the "main_directory" to the path of your file.
sigext.py - Run as the code is. Nothing to be changed.
Bank_AcctNo_OCR.py - Change the "directory" and "image_path" to the path of you file.
databasecheck.py - Provide the cheque number and account number as parameters. Requires databases of all the accepted and stoped cheques.


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
<a href = "https://www.kaggle.com/datasets/74caca03d8d6a1e3ec07f412cc6f5594ab2961fddcdc210d0215aee5589e985b/data?select=object-detection.pbtxt"> Kaggle Dataset </a>

We have implemented the ROI detection using ML models like pytorch, but due to the lack of datasets, the AI might sometimes crop inaccurately.


## Accuracy
The system is able to process 70-80% of the cheques including the rejected cheques.
False positives for names handwriting detection is 250 words out of 750 words.

## Video Download Instruction
https://drive.google.com/file/d/1IxnnyZvSqfBM9sG0KiVXO3qergcFoH1n/view?usp=sharing
![Screenshot 2024-03-15 155518](https://github.com/Sanjaykumaar0603/Standard-Chartered-GBS-Campus-Engagement-Event-2024/assets/96214556/5a42e3d8-2718-448c-86c5-e569259edefd)
![Screenshot 2024-03-15 155529](https://github.com/Sanjaykumaar0603/Standard-Chartered-GBS-Campus-Engagement-Event-2024/assets/96214556/4cb1a5ff-0296-45b6-8cd1-0b79de11e3ef)
![Screenshot 2024-03-15 155538](https://github.com/Sanjaykumaar0603/Standard-Chartered-GBS-Campus-Engagement-Event-2024/assets/96214556/37d77774-f9e7-4ba5-95e4-5a9c5a7c63ef)
