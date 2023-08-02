import cv2
# mediapipe is used to detect hand movements
import mediapipe as mp
# pyautogui is used to move the cursor
import pyautogui

# Step 1: To Open the Video Camera using a few lines of the code
# Step 2: Detect the hand
# Step 3: Separate the tip of the index finger in order to differentiate it from other fingers as it is used to operate the cursor
# Step 4: Move the cursor by using the index finger
# Step 5: Left click using the index finger and thumb

# Declaring a variable cap in order to capture the video from the video source
# The method VideoCapture() accepts either the device index or the name of a video file, in this case, it is the index
cap = cv2.VideoCapture(0)

hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    # To Capture the Frame of the Video
    _, frame = cap.read()

    # flip the video to make it laterally right by flipping on the y-axis
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Images are stored in the BGR format and to convert the colorspace from BGR to RGB, cvtColor() is used
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # To process the rgb frame
    output = hand_detector.process(rgb_frame)

    # multi_hand_landmarks is a collection of detected/tracked hands
    # where each hand is represented as a list of
    # 21 hand landmarks and each landmark is composed of x, y and z
    # a and y are normalized to [0.0, 1.0] by the image height and width respectively
    hands = output.multi_hand_landmarks

    # if hand movements are detected
    if hands:
        for hand in hands:
            # show the landmarks of the hand on the frame
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                # x and y are between 0 and 1
                # To get the actual coordinates, we multiply them by width and height respectively
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # The index of the tip of the index finger is 8
                if id == 8:
                    # circle the index point of the index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # To enable the cursor to move outside the frame
                    index_x = screen_width/frame_width * x
                    index_y = screen_height/frame_height * y

                    # move the cursor to the point having the coordinates (index_x, index_y)
                    pyautogui.moveTo(index_x, index_y)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # If the index finger and thumb get closer, left click is performed
                    if abs(index_y-thumb_y) < 20:
                        pyautogui.click()

    # The method imshow() is used to display an image in a window
    # The window automatically fits the image size
    cv2.imshow('Virtual Mouse', frame)

    # waitKey(1) shows the image for 1 millisecond before it automatically closes
    cv2.waitKey(1)