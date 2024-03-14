import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_signature(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize the image (if necessary)
    resized = cv2.resize(gray, (300, 150))
    # Apply histogram equalization for better contrast
    equalized = cv2.equalizeHist(resized)
    return equalized


def extract_features(image):
    # Initialize HOG descriptor
    hog = cv2.HOGDescriptor()
    # Compute HOG features
    features = hog.compute(image)
    return features.flatten()


def normalize_features(features):
    # Normalize feature vector
    norm_features = features / np.linalg.norm(features)
    return norm_features


def compare_signatures(sig1_features, sig2_features):
    # Normalize feature vectors
    sig1_features = normalize_features(sig1_features)
    sig2_features = normalize_features(sig2_features)
    # Calculate cosine similarity
    similarity = cosine_similarity(sig1_features.reshape(1, -1), sig2_features.reshape(1, -1))[0, 0]
    return similarity


def main():
    # Load signature database
    signature_database = {}
    # Load example signatures from the same image
    image_path = "sign3.jpg"
    image = cv2.imread(image_path)
    # Preprocess and extract features for the reference signature
    reference_signature = preprocess_signature(image)
    reference_features = extract_features(reference_signature)
    signature_database["Jane Smith"] = reference_features

    # Path to the input signature to authenticate
    input_signature_path = "ch1.jpg"
    input_signature = cv2.imread(input_signature_path)
    # Preprocess and extract features for the input signature
    input_signature_processed = preprocess_signature(input_signature)

    # Introduce aggressive distortion to the input signature
    input_signature_processed = cv2.GaussianBlur(input_signature_processed, (15, 15), 0)
    input_signature_features = extract_features(input_signature_processed)

    # Compare input signature with signatures in the database
    max_similarity = 0
    matched_person = None
    for person, signature_features in signature_database.items():
        similarity = compare_signatures(input_signature_features, signature_features)
        # Set a threshold for similarity score
        threshold = 0.5  # Below 5%
        if similarity > max_similarity:
            max_similarity = similarity
            matched_person = person

    # Print authentication result
    if matched_person and max_similarity > threshold:
        print(f"Authenticated as {matched_person} with similarity score: {max_similarity}")
    else:
        print("Signature not authenticated.")


if __name__ == "__main__":
    main()
