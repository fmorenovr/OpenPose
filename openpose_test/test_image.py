# test_heatmap.py
import os
import unittest
from py.pose_estimation import PoseEstimation
from py.utils import verifyDir
import cv2
from time import time
from pathlib import Path

here_path = Path().resolve()
repo_path = here_path.parents[0]
test_dir = f"{repo_path}/app/"

verifyDir(f"{test_dir}/outputs/")

class TestPoseEstimator(unittest.TestCase):

    def test_frame(self):
        pose_estimator = PoseEstimation()
        image = cv2.imread(f"{test_dir}/inputs/image_test.png")
        
        start_time = time()
        pose_keypoints, result_frame = pose_estimator.estimate(image)
        print(f"Elapsed time: {str(time() - start_time)} seconds." )

        print("keypoints", pose_keypoints)
        cv2.imwrite(f"{test_dir}/outputs/image_test_result.png", result_frame)
        
        self.assertTrue(result_frame is not None)
