import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_signature(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize the image (if necessary)
    resized = cv2.resize(gray, (300, 150))
    return resized

def extract_features(image):
    # Initialize HOG descriptor
    hog = cv2.HOGDescriptor()
    # Compute HOG features
    features = hog.compute(image)
    return features.flatten()

def compare_signatures(sig1_features, sig2_features):
    # Calculate cosine similarity
    similarity = cosine_similarity(sig1_features.reshape(1, -1), sig2_features.reshape(1, -1))[0, 0]
    return similarity

def main():
    # Load signature database
    signature_database = {}
    # Load example signatures from the same image
    image_path = "sign1.jpeg"
    image = cv2.imread(image_path)
    #signature_database["John Doe"] = extract_features(preprocess_signature(image))
    signature_database["Jane Smith"] = extract_features(preprocess_signature(image))

    # Path to the input signature to authenticate
    input_signature_path = "ch.jpeg"
    input_signature = cv2.imread(input_signature_path)

    # Extract features from the input signature
    input_signature_features = extract_features(preprocess_signature(input_signature))

    # Compare input signature with signatures in the database
    max_similarity = 0
    matched_person = None
    for person, signature_features in signature_database.items():
        similarity = compare_signatures(input_signature_features, signature_features)
        if similarity > max_similarity:
            max_similarity = similarity
            matched_person = person

    # Print authentication result
    if matched_person:
        print(f"Authenticated as {matched_person} with similarity score: {max_similarity}")
    else:
        print("Signature not authenticated.")

if __name__ == "__main__":
    main()
