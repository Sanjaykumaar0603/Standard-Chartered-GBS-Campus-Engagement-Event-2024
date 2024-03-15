import os
import face_recognition
import capture


def main():
    # Capture the photo
    capture.main()

    # Load known image and compute its face encoding
    known_image = face_recognition.load_image_file("temp.jpg")
    stored_encoding = face_recognition.face_encodings(known_image)[0]

    # Directory containing employee images
    directory = "employees"

    # Iterate over each image in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Load unknown image
            unknown_image = face_recognition.load_image_file(os.path.join(directory, filename))
            
            # Find all face encodings in the unknown image
            unknown_encodings = face_recognition.face_encodings(unknown_image)
            
            # Iterate over each detected face encoding
            for unknown_encoding in unknown_encodings:
                # Compare face encodings
                results = face_recognition.compare_faces([stored_encoding], unknown_encoding)
                
                # If the face matches, print the filename
                if results[0]:
                    print("Match found for:", filename)
                    # break  # Assuming you want to stop iterating after finding the first match
                    return True
            else:
                print("No face found in:", filename)
        else:
            print("Skipping file:", filename)
    return False

if __name__ == "__main__":
    main()
