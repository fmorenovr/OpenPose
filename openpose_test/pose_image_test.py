import argparse
import copy
import cv2
from datetime import datetime
from pathlib import Path
from time import time
from console_logging.console import Console
from open_pose.pose_estimation import PoseEstimation

# run video
# python pose_test.py --input_video 00195.flv --img_show

# run realtime
# python pose_test.py

parser = argparse.ArgumentParser(description='Pose-Estimator image processing:')

parser.add_argument('--input_image', required=True, help='Input video.')
parser.add_argument('--data_path', default='inputs/', required=False, help='Input data.')
parser.add_argument('--out_path', default='outputs/', required=False, help='Output data.')
parser.add_argument('--out_name', default=None, required=False, help='Output video name.')
parser.add_argument('--batch_frames', default=None, required=False, help='Number of frames to process.')

parser.add_argument('--save_video', dest='save_video', action='store_true', help='Save output video.')
parser.add_argument('--no-save_video', dest='save_video', action='store_false', help='Save output video.')
parser.set_defaults(save_video=True)

parser.add_argument('--track_employees', dest='track_employees', action='store_true', help='Follow and track employees.')
parser.set_defaults(track_employees=False)

parser.add_argument('--draw_bboxes', dest='draw_bboxes', action='store_true', help='Draw bboxes.')
parser.set_defaults(draw_bboxes=False)

parser.add_argument('--img_show', dest='img_show', action='store_true', help='Show frame.')
parser.set_defaults(img_show=False)

opt = parser.parse_args()
print(opt)

def verifyDir(dir_path):
    if not Path(dir_path).exists():
        Path(dir_path).mkdir(parents=True, mode=0o770, exist_ok=True)

if __name__ == "__main__":

    print("Processing frame batch pose-estimation...")
    
    pose_estimator = PoseEstimation(max_people=10)

    VIDEO_SRC = opt.data_path + opt.input_image
    image = cv2.imread(f"{VIDEO_SRC}")

    verifyDir(opt.out_path)
    
    if opt.out_name is None:
        opt.out_name = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
    
    console = Console()
    
    console.info("[ POSE CONSUMER ]  ....STARTED.... ")
    
    start_time = time()
    pose_keypoints, result_frame = pose_estimator.estimate(image)
    print(f"Elapsed time: {str(time() - start_time)} seconds." )
    
    print("keypoints", pose_keypoints)
    cv2.imwrite(f"{opt.out_path}/image_test_result.png", result_frame)
