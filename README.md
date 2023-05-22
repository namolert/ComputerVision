# project-compvision
This is an application where you can use hand gestures with the slides. Also, the application is able to blur a background when users needed. <br/> <br/>
This is a final project in 2110433 Computer Vision (2022/2), Faculty of Engineering, Chulalongkorn University.
## Problem statement
A satisfying presentation requires the composition of proper content, equipment, and speech. However, controlling the presentation slides as desired can be hard to do due to the lack of equipment, for example, using a mouse to annotate the slide. Therefore, the objective of this project is to create an application that requires only 2 cameras as top-up equipment. This application uses real-time 3D depth estimation using the two cameras to let the presenter control the presentation slides naturally by performing hand gestures without using additional controllers.

## Technical challenge
The most challenging part of this project is to estimate depths in real-time from the two cameras which are needed for determining the pointing location on the slides. The cameras need to be calibrated so that both of them can measure depth values precisely. Also, being new to computer vision and even 3D vision also makes this project challenging.

## Related works
1. [Distant Pointing User Interfaces based on 3D Hand Pointing Recognition](https://dl.acm.org/doi/epdf/10.1145/3132272.3132292) <br/>
This paper shows a method of finger-pointing recognition based on machine learning which utilizes the appearance difference between two camera images. Moreover, they construct 3 types of user interfaces (tiles layout, pie menu, viewer) to consider the accuracy of distant pointing.
2. [Hand Gesture Recognition with multiple users for elevator control in covid pandemic situation](https://github.com/pewtpong/CV-Final-Project/tree/main) <br/>
This project introduces a hand gesture recognition application for controlling an elevator during the pandemic. The project consisted of 3 modules which are hand gesture recognition, face detection, and face recognition. The hand gesture recognition was implemented from Mediapipe, the face detection was implemented from Yolo v4 tiny, and the face recognition was implemented from [ageitgey's face recognition](https://github.com/ageitgey/face_recognition).
3. [Stereo Vision: Depth Estimation between object and camera](https://medium.com/analytics-vidhya/distance-estimation-cf2f2fd709d8) <br/>
This article shows a tutorial on how to estimate the depth of objects in the video using 2 stereo cameras. Both cameras are needed to be calibrated and then used to calculate disparities. After that, use the disparity to get a depth map/image.

## Method
The application consists of 2 major modules, hand gesture recognition and 3D vision. <br/> <br/>
The main library for the hand gesture recognition module is [Mediapipe](https://github.com/google/mediapipe) which provides a Hand module that is able to detect a hand and localize 21 hand landmarks in an input image in x, y, z where z is the depth of a landmark with the wrist depth as the origin. We also use [CVZone](https://github.com/cvzone/cvzone) Hand Tracking Module which implements additional functionalities on top of the Mediapipe Hand module including determining the fingers that are up. <br/> <br/>
For the 3D vision module, we use 2 Logitech C270 webcams to estimate the depth of the points using the stereo vision technique. <br/>

![Mediapipe hand landmarks](https://developers.google.com/static/mediapipe/images/solutions/hand-landmarks.png) <br/>

There are four hand gestures of which each performs the corresponding action on the presentation slides. The first one is index finger pointing which has two behaviors depending on the current mode. If the mode is "pointing" then a circle dot is drawn at the pointing location on the slide in the current video frame and is erased when the frame is changed, else if the mode is "annotating" then a circle dot and a line between the circle dot in the previous frame are drawn. The presenter can change the mode by raising up three fingers which are the index, the middle, and the ring. To change pages, raise the pinky finger to go to the next page, and raise the thumb to go to the previous page. <br/> <br/>
Notice that with Mediapipe's Hand module, we only have depths of landmarks with respect to the wrist not with the monitor plane, and thus we need to implement the 3D vision module to estimate the depths. Before we find depths of points of interest, we calibrate each camera to retrieve a set of parameters on the captured chessboard images at the same points in time. After that, we can undistort the input images using the obtained parameters. Now we can find the depth value by using the formula depth = baseline * f / disparity. Consequently, we use the depth value at the presenter's index finger MCP to calculate the 3D line that passes through the index finger MCP and TIP. The pointing location is then obtained by finding the intersection between the monitor plane and the line.

![3d line symmetric equation](https://i.ytimg.com/vi/OP19Db-WnLc/maxresdefault.jpg) <br/>

```
# parameter must be changed according to the cameras
a, b, c = tuple([indexTip[i] - indexMcp[i] for i in range(len(indexTip))])
x0, y0, z0 = indexMcp
z = zdepth * (10 / (2.8 ** 0.5))
x = (z - z0) / c * a + x0 if c != 0 else 0
y = (z - z0) / c * b + x0 if c != 0 else 0
```

The results show that In hand gesture recognition, the CVZone and Mediapipe are able to detect and identify any shape of the hand accurately. In the 3D vision module, the cameras are able to estimate the depth between the index finger MCP accurately. The locations pointed from that direction are also intuitive to understand and precise.

## Results
In hand gesture recognition, the CVZone and Mediapipe are able to detect and identify any shape of the hand accurately. <br/> <br/>
In 3D vision, the camera is able to detect the depth between an index finger tip and MCP accurately. The location from that direction is also easy to understand and precise.

## Discussion & Future improvements
The application seems to work very well. However, there are some limitations to our application. 
1. Slides are stored as a folder of pictures. This means that if the presentation has 100 slides we need to save them into 100 picture files.
2. The application is only available offline, which makes online presentation unavailable.
3. Since we use two separate cameras and not the stereo camera, the frames captured by them can not be synced at the same unit of time, so we have done the best approach which is using cv2.VideoCapture.grab() and cv2.VideoCapture.retrieve() instead of cv2.VideoCapture.read() to reduce the the delay between frame retrievals of the two cameras. Moreover, the alignment of the two cameras can be changed every time they are moved, so we need to calibrate them every time at the beginning of the application, unlike with stereo cameras of which the alignment is fixed.
4. The pointing and annotating parts are not jiggling due to the hand detection which is also jiggling and the results that are drawn in every frame. <br/>

With all the limitations mentioned above, future improvements can be made.
1. Replace the folder of pictures of presentation slides with a single file such as .pdf or .ppt. 
2. Make the application available online by developing an HTTP application. Lastly, improve the application to support different kinds of resolution, camera, and other parameters.
3. Try to smooth the coordinates between frames such as delaying the drawing on the locations. <br/>

Moreover, additional features such as detecting two hands simultaneously, adding empty pages for free drawing, and blurring a background can be implemented. <br/>

Conducting a camera calibration using OpenCV is one of the most challenging tasks, primarily when the chessboard cannot be detected easily. Despite the powerful capabilities of OpenCV, several factors can complicate the process such as varying lighting conditions and shadows. Moreover, errors in aligning the camera are also one of the problems in calibrating. Achieving accurate alignment between multiple cameras is crucial for stereo vision applications, where depth information is obtained by triangulating corresponding points in the two camera views. However, aligning the cameras precisely can be difficult due to various factors. This leads to problems after performing a camera calibration, it can be frustrating to discover that the quality of the obtained images is worse than before. Lastly, the frame size obtained from the camera is too small for the intended task, it can significantly impact the ability to perform the task perfectly. The small frame size can adversely affect the hand detection algorithms, as they heavily rely on robust feature detection and matching. Insufficient visual cues due to the small frame size can compromise the tracking accuracy and introduce tracking errors, leading to imprecise pointing or targeting.


## Credits
Big thanks to the references used in this project.
1. [Nicolai Nielsen](https://www.youtube.com/channel/UCpABUkWm8xMt5XmGcFb3EFg)
2. [Murtaza's Workshop - Robotics and AI](https://www.youtube.com/channel/UCYUjYU5FveRAscQ8V21w81A)
