import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def preprocess_signature(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh

def extract_features(image):
    # For simplicity, let's use the image histogram as feature
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist.flatten()

def compare_signatures(sig1_features, sig2_features):
    # Calculate correlation coefficient as a similarity measure
    similarity = cv2.compareHist(sig1_features, sig2_features, cv2.HISTCMP_CORREL)
    return similarity

def extract_signature(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Preprocess the signature
    preprocessed_signature = preprocess_signature(image)
    
    return preprocessed_signature

def load_database():
    # In a real scenario, you would load signatures from a database
    # For simplicity, let's just load example signatures here
    database = {}
    #database["John Doe"] = extract_features(preprocess_signature(cv2.imread("john_doe_signature.jpg")))
    database["Jane Smith"] = extract_features(preprocess_signature(cv2.imread("sign1.jpeg")))
    return database

def authenticate_signature(input_signature, database):
    input_signature_features = extract_features(input_signature)
    max_similarity = 0
    matched_person = None
    for person, signature_features in database.items():
        similarity = compare_signatures(input_signature_features, signature_features)
        if similarity > max_similarity:
            max_similarity = similarity
            matched_person = person
    return matched_person, max_similarity

def main():
    # Load signature database
    signature_database = load_database()

    # Path to the bank cheque image
    image_path = "ch.jpeg"
    
    # Extract the signature from the bank cheque
    extracted_signature = extract_signature(image_path)

    # Authenticate the extracted signature
    matched_person, similarity = authenticate_signature(extracted_signature, signature_database)

    # Print the result
    if matched_person:
        print(f"Authenticated as {matched_person} with similarity score: {similarity}")
    else:
        print("Signature not authenticated.")

if __name__ == "__main__":
    main()
