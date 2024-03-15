import cv2
from tkinter import *
from PIL import Image, ImageTk

class ImageCapture:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Capture")
        
        self.video_capture = cv2.VideoCapture(0)
        
        self.btn_capture = Button(self.root, text="Capture Image", command=self.capture_image)
        self.btn_capture.pack(pady=10)
        
        self.label = Label(self.root)
        self.label.pack()
        
        self.update()
        
    def update(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.label.config(image=self.photo)
            self.label.image = self.photo
        self.root.after(10, self.update)
        
    def capture_image(self):
        ret, frame = self.video_capture.read()
        if ret:
            cv2.imwrite("temp.jpg", frame)
            print("Image captured successfully!")

def main():
    root = Tk()
    app = ImageCapture(root)
    root.mainloop()

if __name__ == "__main__":
    main()
