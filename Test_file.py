#Author: Nafis Ahmed
#This script is used to convert a video file into a dataset of images. 
#The script will display each frame of the video and wait for the user to click on the frame. 
#When the user clicks on the frame, the script will save the frame as an image file in the output directory. 
#The filename of the image file will be the x and y coordinates of the clicked point in the frame. 
#The script will also generate a unique ID for the frame and append it to the filename. 
#This is done to ensure that the filename is unique and does not clash with any existing files in the output directory.
#if a frame does not contain any object of interest, the user can simply press and hold the spacebar to skip the frame/frames.
#choose the video file from the videos folder and put it in the video_path variable.
import cv2
import uuid

# Define the video file path
#example: video_path = 'videos/clip_1.mp4'
video_path = 'D:\Mechatronic System Engineering\clip_1.mp4'

# Define the output directory where frames will be saved
output_directory = 'D:\Mechatronic System Engineering\output'

# Open the video file
video_capture = cv2.VideoCapture(video_path)


# Variables to store clicked coordinates
x_coordinate = None
y_coordinate = None

# Flag to indicate if a click event has occurred
click_event_occurred = False

from pynput.keyboard import Controller

# Create a keyboard controller
keyboard = Controller()

# Function to handle mouse clicks on the video frame
def save_frame(event, x, y, flags, param):
    global x_coordinate, y_coordinate, click_event_occurred
    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the clicked coordinates
        x_coordinate = x
        y_coordinate = y
        click_event_occurred = True
        # Generate a spacebar key event
        keyboard.press(' ')  # Press the spacebar
        keyboard.release(' ')  # Release the spacebar

# Create a window to display the video frame
cv2.namedWindow('Video Frame')
cv2.setMouseCallback('Video Frame', save_frame)

while True:
    # Read the next frame from the video
    ret, frame = video_capture.read()

    if not ret:
        # Video has ended
        break

    # Display the frame in the window
    cv2.imshow('Video Frame', frame)

    if click_event_occurred:
        # Generate a unique ID for the frame
        unique_id = str(uuid.uuid4())

        # Construct the frame filename using the clicked coordinates and the unique ID
        frame_filename = f"{x_coordinate}_{y_coordinate}_{unique_id}.jpg"

        # Save the frame to the output directory
        cv2.imwrite(output_directory + '/' + frame_filename, frame)
        print(f"Frame saved: {frame_filename}")

        # Reset the flag and clicked coordinates
        click_event_occurred = False
        x_coordinate = None
        y_coordinate = None

        # Wait for the user to press any key before proceeding to the next frame
        # cv2.waitKey(0)

    # Check for 'q' key press to exit
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
video_capture.release()
cv2.destroyAllWindows()