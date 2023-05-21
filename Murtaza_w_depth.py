from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import mediapipe as mp
import calibrate_func
import triangulation as tri

# Parameters
width, height = 640, 480
# width, height = 1280, 720
gestureThreshold = 300
folderPath = os.path.join('images', 'presentation2')

# Camera Setup
cap_right = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap_left = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap_right.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_right.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap_left.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_left.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Hand Detector
detectorHandL = HandDetector(detectionCon=0.8, maxHands=1)
detectorHandR = HandDetector(detectionCon=0.8, maxHands=1)
fingerIndex = mp.solutions.hands.HandLandmark

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
pointMode = True

# annotationsR, annotationsL = [[]], [[]]
# annotationNumberR, annotationNumberL = -1, -1
# annotationStartR, annotationStartL = False, False

annotations = [[]]
annotationNumber = -1
annotationStart = False

hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

frame_rate = 120  # Camera frame rate (maximum at 120 fps)
B = 14  # Distance between the cameras [cm]
f = 4  # Camera lense's focal length [mm]
alpha = 55  # Camera field of view in the horisontal plane [degrees]

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath))
print(pathImages)


def getImageXYFromZ(indexTip, indexMcp, zdepth):

    a, b, c = tuple([indexTip[i] - indexMcp[i] for i in range(len(indexTip))])
    x0, y0, z0 = indexMcp
    z = zdepth * (10 / (2.8 ** (0.5)))
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
    succes_right, frame_right = cap_right.read()
    succes_left, frame_left = cap_left.read()

    # Calibration
    frame_right, frame_left = calibrate_func.undistortRectify(
        frame_right, frame_left)

    frame_right = cv2.flip(frame_right, 1)
    frame_left = cv2.flip(frame_left, 1)

    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Find the hand and its landmarks
    handsR, frame_right = detectorHandR.findHands(frame_right)
    handsL, frame_left = detectorHandL.findHands(frame_left)

    # Display mode
    if pointMode:
        cv2.putText(frame_left, "mode: pointing", (50, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
    else:
        cv2.putText(frame_left, "mode: annotating", (50, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)

    # Draw Gesture Threshold line
    cv2.line(frame_right, (0, gestureThreshold),
             (width, gestureThreshold), (0, 255, 0), 5)
    cv2.line(frame_left, (0, gestureThreshold),
             (width, gestureThreshold), (0, 255, 0), 5)

    # If hand is detected
    if (handsR and handsL) and not buttonPressed:

        handL = handsL[0]
        handR = handsR[0]
        cxR, cyR = handR["center"]
        cxL, cyL = handL["center"]

        # List of 21 Landmark points
        lmListR = handR["lmList"]
        lmListL = handL["lmList"]

        # List of which fingers are up
        fingersR = detectorHandR.fingersUp(handR)
        fingersL = detectorHandL.fingersUp(handL)

        # Constrain values for easier drawing
        indexTipXR = int(np.interp(lmListR[fingerIndex.INDEX_FINGER_TIP][0], [
            width // 2, width], [0, width]))
        indexTipYR = int(np.interp(lmListR[fingerIndex.INDEX_FINGER_TIP][1], [
            150, height-150], [0, height]))
        indexTipXL = int(np.interp(lmListL[fingerIndex.INDEX_FINGER_TIP][0], [
            width // 2, width], [0, width]))
        indexTipYL = int(np.interp(lmListL[fingerIndex.INDEX_FINGER_TIP][1], [
            150, height-150], [0, height]))

        indexMcpXR = int(np.interp(lmListR[fingerIndex.INDEX_FINGER_MCP][0], [
            width // 2, width], [0, width]))
        indexMcpYR = int(np.interp(lmListR[fingerIndex.INDEX_FINGER_MCP][1], [
            150, height-150], [0, height]))
        indexMcpXL = int(np.interp(lmListL[fingerIndex.INDEX_FINGER_MCP][0], [
            width // 2, width], [0, width]))
        indexMcpYL = int(np.interp(lmListL[fingerIndex.INDEX_FINGER_MCP][1], [
            150, height-150], [0, height]))

        wristXR = int(np.interp(lmListR[fingerIndex.WRIST][0], [
            width // 2, width], [0, width]))
        wristYR = int(np.interp(lmListR[fingerIndex.WRIST][1], [
            150, height-150], [0, height]))
        wristXL = int(np.interp(lmListL[fingerIndex.WRIST][0], [
            width // 2, width], [0, width]))
        wristYL = int(np.interp(lmListL[fingerIndex.WRIST][1], [
            150, height-150], [0, height]))

        indexTipZR = lmListR[8][2]
        indexFingerR = indexTipXR, indexTipYR
        indexTipZL = lmListL[8][2]
        indexFingerL = indexTipXL, indexTipYL
        wristZR = lmListR[0][2]
        wristXYR = wristXR, wristYR
        wristZL = lmListL[0][2]
        wristXYL = wristXL, wristYL
        indexMcpZR = lmListR[5][2]
        indexFingerMcpR = indexMcpXR, indexMcpYR
        indexMcpZL = lmListL[5][2]
        indexFingerMcpL = indexMcpXL, indexMcpYL

        pointerColor = cv2.cvtColor(
            np.array([[[abs(indexTipZR), 255, 255]]]).astype(np.uint8), cv2.COLOR_HSV2BGR)
        pointerColor = pointerColor.reshape(3)
        pointerColor = tuple([int(x) for x in pointerColor])

        # Change Page
        if fingersL == [1, 0, 0, 0, 0] or fingersR == [1, 0, 0, 0, 0]:
            print("Left")
            buttonPressed = True
            if imgNumber > 0:
                imgNumber -= 1
                annotations = [[]]
                annotationNumber = -1
                annotationStart = False
        if fingersL == [0, 0, 0, 0, 1] or fingersR == [0, 0, 0, 0, 1]:
            print("Right")
            buttonPressed = True
            if imgNumber < len(pathImages) - 1:
                imgNumber += 1
                annotations = [[]]
                annotationNumber = -1
                annotationStart = False

        # Map index finger to the screen
        depth = tri.find_depth(
            indexFingerMcpR, indexFingerMcpL, frame_right, frame_left, B, f, alpha)
        # cv2.putText(frame_right, "Distance: " + str(round(depth, 1)),
        #             (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        # cv2.putText(frame_left, "Distance: " + str(round(depth, 1)),
        #             (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        indexFinger = getImageXYFromZ(
            (indexTipXL, indexTipYL, indexTipZL), (indexMcpXL, indexMcpYL, indexMcpZL), depth)

        # Change pointMode
        if fingersL == [0, 1, 1, 1, 0] or fingersR == [0, 1, 1, 1, 0]:
            buttonPressed = True
            pointMode = not pointMode

        # Choose between point mode and draw mode
        if pointMode:
            annotationStart = False
            cv2.circle(imgCurrent, indexFinger, 12, (0, 255, 0), cv2.FILLED)
        else:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            annotations[annotationNumber].append((indexFinger, pointerColor))
            cv2.circle(imgCurrent, indexFinger, 12, pointerColor, cv2.FILLED)

        # I LOVE YOU
        if fingersL == [1, 1, 0, 0, 1] or fingersR == [1, 1, 0, 0, 1]:
            cv2.putText(frame_right, "I LOVE YOU", (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.putText(frame_left, "I LOVE YOU", (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.putText(imgCurrent, "I LOVE YOU", (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
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
                cv2.line(
                    imgCurrent, annotation[j - 1][0], annotation[j][0], annotation[j][1], 12)

    imgSmall = cv2.resize(frame_right, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Frame Right", frame_right)
    cv2.imshow("Frame Left", frame_left)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
