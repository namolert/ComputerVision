# project-compvision
This is an application where you can use hand gestures with the slides. Also, the application is able to blur a background when users needed. <br/> <br/>
This is a final project in 2110433 Computer Vision (2022/2), Faculty of Engineering, Chulalongkorn University.
## Problem statement
A satisfying presentation requires the composition of proper content, equipment, and speech. However, some users cannot have a good presentation due to the lack of equipment. Therefore, the objective of this project is to create an application that requires only 2 cameras as top-up equipment to let the presenter conduct a decent presentation. This application uses real-time 3D depth estimation using the two cameras to let the presenter control the presentation slides naturally by performing hand gestures without using additional controllers. The presenter can also blur their backgrounds by doing a specified hand gesture.

## Technical challenge

## Related works
1. [Distant Pointing User Interfaces based on 3D Hand Pointing Recognition](https://dl.acm.org/doi/epdf/10.1145/3132272.3132292) <br/>
This paper shows a method of finger-pointing recognition based on machine learning which utilizes the appearance difference between two camera images. Moreover, they construct 3 types of user interfaces (tiles layout, pie menu, viewer) to consider the accuracy of distant pointing.
2. [Hand Gesture Recognition with multiple users for elevator control in covid pandemic situation](https://github.com/pewtpong/CV-Final-Project/tree/main) <br/>
This project introduces a hand gesture recognition application for controlling an elevator during the pandemic. The project consisted of 3 modules which are hand gesture recognition, face detection, and face recognition. The hand gesture recognition was implemented from Mediapipe, the face detection was implemented from Yolo v4 tiny, and the face recognition was implemented from [ageitgey's face recognition](https://github.com/ageitgey/face_recognition)

## Method
The application consisted of 2 major modules, hand gesture recognition and 3D vision. <br/> <br/>
The hand gesture recognition module uses the [cvzone](https://github.com/cvzone/cvzone) library which is a computer vision package that makes processing images and AI functions easier to implement. Also, the package [Mediapipe](https://github.com/google/mediapipe) provides a hand gesture detection module that is able to identify which fingers are raised and which hand it is (left or right). <br/> <br/>
For the 3D vision module, we use 2 Logitech C270 webcams to create depth maps using the stereo vision technique. First, we calibrate each camera to retrieve a set of parameters on the captured chessboard images at the same points in time. After that, we combine both cameras with the obtained parameters to estimate the depth of the video frames. The depth images will be used to determine the direction of a finger that points to the screen and blur the background apart from the user's body.

## Results

## Discussion
The application seems to work very well. However, there are some limitations to our application.
1. Slides are stored as a folder of pictures. This means that if the presentation has 100 slides we need to save them into 100 picture files.
2. The application is only available offline, which makes online presentation unavailable.
3. The result may vary when used with other camera models and other resolutions.

## Future improvements
With all limitations mentioned above, future improvements can be made.
1. Replace the folder of pictures of presentation slides with a single file such as .pdf or .ppt.
2. Make the application available online by developing an HTTP application.
3. Improve the application to support different kinds of resolution, camera, and other parameters. <br/>
Moreover, additional features such as detecting two hands simultaneously or adding empty pages for free drawing can be implemented.

## Credits
Big thanks to the creators.
1. [Nicolai Nielsen](https://www.youtube.com/channel/UCpABUkWm8xMt5XmGcFb3EFg)
2. [Murtaza's Workshop - Robotics and AI](https://www.youtube.com/channel/UCYUjYU5FveRAscQ8V21w81A)
