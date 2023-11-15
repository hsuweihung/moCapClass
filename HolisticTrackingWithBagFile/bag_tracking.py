# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path
import mediapipe as mp
import time
import math

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", default='001.bag',
                    type=str, help="./mocap_video.bag")
# Parse the command line arguments to an object
args = parser.parse_args(args=['--input', 'mocap_video.bag'])

mpDraw = mp.solutions.drawing_utils  # Call the drawing tool
mp_holistic = mp.solutions.holistic  # Call the hand tracking tool
mp_drawing_styles = mp.solutions.drawing_styles

# Create pipeline
pipeline = rs.pipeline()

# Create a config object
config = rs.config()

# Tell config that we will use a recorded device from file to be used by the pipeline through playback.
rs.config.enable_device_from_file(config, args.input)

# Configure the pipeline to stream the depth stream
# Change this parameters according to the recorded bag file resolution
# config.enable_stream(rs.stream.depth, rs.format.z16, 30)


if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()

try:
    # 從檔案開始串流
    pipeline.start(config)

    while True:
        frames = pipeline.wait_for_frames()

        # 將 RealSense 畫面轉換為 NumPy 陣列
        depth_frame = np.asanyarray(frames.get_depth_frame().get_data())

        # 讀取彩色畫面
        color_frame = np.asanyarray(frames.get_color_frame().get_data())

        # 對彩色畫面進行 holistic 處理
        with mp_holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as holistic:

            # 處理畫面
            results = holistic.process(color_frame)

            # 在彩色畫面上繪製標誌
            mpDraw.draw_landmarks(
                color_frame,
                results.face_landmarks,
                mp_holistic.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style())

            mpDraw.draw_landmarks(
                color_frame,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_pose_landmarks_style())

            # 顯示畫面
            cv2.imshow('Holistic Detection', color_frame)

            # 當按下 'Esc' 鍵時跳出迴圈
            if cv2.waitKey(1) == 27:
                break

finally:
    # 停止串流
    pipeline.stop()
    cv2.destroyAllWindows()
