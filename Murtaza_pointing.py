from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import mediapipe as mp

# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = os.path.join('images', 'presentation')

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)
fingerIndex = mp.solutions.hands.HandLandmark

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath))
print(pathImages)


def getImageXYFromZ(indexTip, indexMcp):

    a, b, c = tuple([indexTip[i] - indexMcp[i] for i in range(len(indexTip))])
    x0, y0, z0 = indexMcp
    z = 1280  # don't have depth map yet
    # TODO: recheck these formulas
    x = (z - z0) / c * a + x0 if c != 0 else 0
    y = (z - z0) / c * b + y0 if c != 0 else 0

    # set overflows to boundaries
    if x < 0:
        x = 0
    elif x > width - 1:
        x = width - 1
    if y < 0:
        y = 0
    elif y > height - 1:
        y = height - 1

    x = width - 1 - int(x)  # flip coordinates
    y = height - 1 - int(y)  # flip coordinates
    return int(x), int(y)


while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold),
             (width, gestureThreshold), (0, 255, 0), 5)

    if hands and not buttonPressed:  # If hand is detected

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        # indexTipX = int(np.interp(lmList[fingerIndex.INDEX_FINGER_TIP][0], [width // 2, width], [0, width]))
        # indexTipY = int(np.interp(lmList[fingerIndex.INDEX_FINGER_TIP][1], [150, height-150], [0, height]))
        indexTipX = lmList[fingerIndex.INDEX_FINGER_TIP][0]
        indexTipY = lmList[fingerIndex.INDEX_FINGER_TIP][1]
        indexTipZ = lmList[fingerIndex.INDEX_FINGER_TIP][2]
        indexMcpX = lmList[fingerIndex.INDEX_FINGER_MCP][0]
        indexMcpY = lmList[fingerIndex.INDEX_FINGER_MCP][1]
        indexMcpZ = lmList[fingerIndex.INDEX_FINGER_MCP][2]
        indexFinger = getImageXYFromZ(
            (indexTipX, indexTipY, indexTipZ), (indexMcpX, indexMcpY, indexMcpZ))
        print(indexFinger)

        pointerColor = cv2.cvtColor(
            np.array([[[abs(indexTipZ), 255, 255]]]).astype(np.uint8), cv2.COLOR_HSV2BGR)
        pointerColor = pointerColor.reshape(3)
        pointerColor = tuple([int(x) for x in pointerColor])

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            # print(annotationNumber)
            # print(pointerColor)
            annotations[annotationNumber].append((indexFinger, pointerColor))
            cv2.circle(imgCurrent, indexFinger, 12, pointerColor, cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                print(annotation[j - 1][0], annotation[j][0])
                cv2.line(
                    imgCurrent, annotation[j - 1][0], annotation[j][0], annotation[j][1], 12)

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
