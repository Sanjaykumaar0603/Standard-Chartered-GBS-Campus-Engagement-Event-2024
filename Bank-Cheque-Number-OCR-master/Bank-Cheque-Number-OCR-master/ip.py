from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from skimage.segmentation import clear_border
from imutils import contours
import imutils
import os

app = Flask(__name__)

charNames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0","T", "U", "A", "D"]

def extractChNo(image, charCnts, minW=5, minH=15):
    charIter = charCnts.__iter__()
    rois = []
    locs = []
    
    while True:
        try:
            c = next(charIter)
            (cX, cY, cW, cH) = cv2.boundingRect(c)
            roi = None
            
            if cW >= minW and cH >= minH:
                roi = image[cY:cY + cH, cX:cX + cW]
                rois.append(roi)
                locs.append((cX, cY, cX + cW, cY + cH))
            else:
                parts = [c,next(charIter), next(charIter)]
                (sXA, sYA, sXB, sYB) = (np.inf, np.inf, -np.inf,-np.inf)
                
                for p in range(0,3):
                    (pX, pY, pW, pH) = cv2.boundingRect(parts[p])
                    sXA = min(sXA, pX)
                    sYA = min(sYA, pY)
                    sXB = max(sXB, pX + pW)
                    sYB = max(sYB, pY + pH)
                
                roi = image[sYA:sYB, sXA:sXB]
                rois.append(roi)
                locs.append((sXA, sYA, sXB, sYB))
        except StopIteration:
            break
    return (rois, locs)

def ocr_check(image_path):
    ref = cv2.imread("refr.png")
    ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    ref = imutils.resize(ref, width=500)
    ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    refCnts = imutils.grab_contours(refCnts)
    refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]

    refROIs = extractChNo(ref, refCnts,minW=10, minH=20)[0]
    chars = {}
    for (name, roi) in zip(charNames, refROIs):
        roi = cv2.resize(roi, (36, 36)) 
        chars[name] = roi

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 7))
    output = []

    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    delta = int(h - (h * 0.2))
    bottom = image[delta:h, 0:w]

    gray = cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)

    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0,ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
    gradX = gradX.astype("uint8")

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)

    groupCnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    groupCnts = imutils.grab_contours(groupCnts)
    groupLocs = []

    for (i, c) in enumerate(groupCnts):
        (x, y, w, h) = cv2.boundingRect(c+1)
        if w > 20 and h > 15:
            groupLocs.append((x, y, w, h))

    groupLocs = sorted(groupLocs, key=lambda x:x[0])

    for (gX, gY, gW, gH) in groupLocs:
        groupOutput = []

        group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
        group = cv2.threshold(group, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        charCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        charCnts = imutils.grab_contours(charCnts)
        charCnts = contours.sort_contours(charCnts,method="left-to-right")[0]

        (rois, locs) = extractChNo(group, charCnts)

        for roi in rois:
            scores = []
            roi = cv2.resize(roi, (36, 36))
            for charName in charNames:
                result = cv2.matchTemplate(roi, chars[charName],cv2.TM_CCOEFF)
                (_, score, _, _) = cv2.minMaxLoc(result)
                scores.append(score)

            groupOutput.append(charNames[np.argmax(scores)])

        output.append("".join(groupOutput))

    return {
        "cn": output[0][1:7],
        "mc": output[1][0:9],
        "ai": output[2][0:6],
        "tc": output[3]
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        filename = file.filename
        file.save(filename)
        result = ocr_check(filename)
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
