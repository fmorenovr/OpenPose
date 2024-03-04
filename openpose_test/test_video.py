# test_heatmap.py
import os
import unittest
from py.pose_estimation import PoseEstimation
from pu.utils import verifyDir
import cv2
import copy
from datetime import datetime
from pathlib import Path
from time import time
from pathlib import Path
import glob
from tqdm import tqdm

here_path = Path().resolve()
repo_path = here_path.parents[0]
test_dir = f"{repo_path}/app/"
OUTPUT_PATH = f"{test_dir}/outputs/"

verifyDir(OUTPUT_PATH)

class TestPoseEstimator(unittest.TestCase):

    def test_videos(self):
        pose_estimator = PoseEstimation()
        video_list = glob.glob(f"{test_dir}/inputs/*/*.mp4")
        for video_src in tqdm(video_list):
            video_source_mkv = video_src.replace("//", "/")
            
            cap = cv2.VideoCapture(video_source_mkv)
            _, frame = cap.read()
            
            out_name = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            video_name = ( video_src.split("/")[-1] ).split(".")[0]
            dir_name = video_src.split("/")[-2]
            verifyDir(f"{OUTPUT_PATH}{dir_name}/")
            video_out_path = f"{OUTPUT_PATH}{dir_name}/{video_name}_pose_estimation.mp4".replace("//", "/")
            print(video_out_path)
            
            out_video = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (1280, 720))
            
            start_time = time()
        
            count = 0
            
            while cap.isOpened():
                
                ok, frame = cap.read()
                
                if not ok:
                    break
                    
                if frame is None:
                    break
            
                frame_resized = cv2.resize(frame, (640,640), interpolation=cv2.INTER_CUBIC)
                
                posedict_keypoints, frame_keypoints = pose_estimator.estimate(copy.deepcopy(frame_resized))
            
                out_video.write( cv2.resize(frame_keypoints, (1280, 720)) )
                
                count += 1

            cap.release()
            print(f"Elapsed time: {str(time() - start_time)} seconds." )
        
        self.assertTrue(count>1)
        

    def test_image(self):
        pose_estimator = PoseEstimation()
        
        input_name = f"{test_dir}/inputs/videos/c01_test.avi"
        
        file_name = input_name.split("/")[-1].replace(".avi", "")
        
        cap = cv2.VideoCapture(input_name)
        _, frame = cap.read()
        
        out_name = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        out_path = f"{test_dir}/outputs/videos/"
        video_out_path = Path(out_path).joinpath(f"{out_name}_{file_name}_pose_estimation.mp4").as_posix()
        
        out_video = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (1280, 720))
        
        start_time = time()
        
        count = 0
        
        while cap.isOpened():
            
            ok, frame = cap.read()
            
            if not ok:
                break
                
            if frame is None:
                break
        
            frame_resized = cv2.resize(frame, (640,640), interpolation=cv2.INTER_CUBIC)
            
            posedict_keypoints, frame_keypoints = pose_estimator.estimate(copy.deepcopy(frame_resized))
        
            out_video.write( cv2.resize(frame_keypoints, (1280, 720)) )
            
            count += 1

        cap.release()
        print(f"Elapsed time: {str(time() - start_time)} seconds." )

        self.assertTrue(count>=1)
