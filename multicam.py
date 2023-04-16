import numpy as np
import cv2
import pickle


def ShowDisparity(bSize, nDisparities, imgLeft, imgRight):
    # Initialize the stereo block matching object
    stereo = cv2.StereoBM_create(numDisparities=nDisparities, blockSize=bSize)

    grayLeft = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)

    # Convert the image to 8 bits per pixel
    grayLeft = cv2.convertScaleAbs(grayLeft)
    grayRight = cv2.convertScaleAbs(grayRight)

    # Compute the disparity image
    disparity = stereo.compute(grayLeft, grayRight)

    # Normalize the image for representation
    min = disparity.min()
    max = disparity.max()
    disparity = np.uint8(255 * (disparity - min) / (max - min))

    # Plot the result
    return disparity


def CropImage(image, scale):
    # get the webcam size
    height, width, channels = image.shape

    # prepare the crop
    centerX, centerY = int(height/2), int(width/2)
    radiusX, radiusY = int(scale*height/100), int(scale*width/100)

    minX, maxX = centerX-radiusX, centerX+radiusX
    minY, maxY = centerY-radiusY, centerY+radiusY

    cropped = image[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))

    if cv2.waitKey(1) & 0xFF == ord("o"):
        scale += 1  # zoom out 1
        print(scale)

    if cv2.waitKey(1) & 0xFF == ord("i"):
        scale -= 1  # zoom in 1
        print(scale)

    return resized_cropped, scale


# declare all variable
video_capture_0 = cv2.VideoCapture(1)
video_capture_1 = cv2.VideoCapture(0)
bsize = 5
nDisparities = 16
scale = 40
num = 0

while True:
    ret0, frame0 = video_capture_0.read()
    ret1, frame1 = video_capture_1.read()
    frame0 = cv2.flip(frame0, 1)
    frame1 = cv2.flip(frame1, 1)

    # setting camera
    if (ret0):
        cv2.imshow("Cam 0", frame0)
    if (ret1):
        frame1_new, scale = CropImage(frame1, scale)
        cv2.imshow("Cam 1", frame1_new)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        cv2.imwrite('images/stereoRight/imageR' + str(num) + '.png', frame0)
        cv2.imwrite('images/stereoLeft/imageL' + str(num) + '.png', frame1_new)
        print("Images save!!!")
        num += 1

    # find object with depth
    scale = 37
    frame1_new, scale = CropImage(frame1, scale)
    result = ShowDisparity(bsize, nDisparities, frame0, frame1_new)
    cv2.imshow("Cam 2", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture_0.release()
video_capture_1.release()
cv2.destroyAllWindows()
