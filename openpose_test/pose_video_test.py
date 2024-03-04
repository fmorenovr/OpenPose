import argparse
import copy
import cv2
from datetime import datetime
from pathlib import Path
from console_logging.console import Console
from open_pose.pose_estimation import PoseEstimation

# run video
# python pose_test.py --input_video 00195.flv --img_show

# run realtime
# python pose_test.py

parser = argparse.ArgumentParser(description='Pose-Estimator video processing:')

parser.add_argument('--input_video', required=True, help='Input video.')
parser.add_argument('--data_path', default='inputs/', required=False, help='Input data.')
parser.add_argument('--out_path', default='outputs/', required=False, help='Output data.')
parser.add_argument('--out_name', default=None, required=False, help='Output video name.')
parser.add_argument('--out_fps', default=30, required=False, help='Output video fps.')
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

    VIDEO_SRC = opt.data_path + opt.input_video
    cap = cv2.VideoCapture(VIDEO_SRC)
    
    verifyDir(opt.out_path)
    if opt.out_name is None:
        opt.out_name = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
    
    video_out_path = Path(opt.out_path).joinpath(f"{opt.out_name}_pose_estimation.mp4").as_posix()
    out_video = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'),
                               opt.out_fps, (1280, 720))
    
    _, frame = cap.read()
    
    # inicializa config
    pose_estimator = PoseEstimation(max_people=10)
    console = Console()
    
    console.info("[ POSE CONSUMER ]  ....STARTED.... ")
    
    count = 0
    
    while cap.isOpened():
    
        ok, frame = cap.read()

        if opt.batch_frames is not None:
            if count >= int(opt.batch_frames):
                break

        if not ok:
            break
            
        if frame is None:
            break
            
        frame_resized = cv2.resize(frame, (640,640), interpolation=cv2.INTER_CUBIC)
        
        posedict_keypoints, frame_keypoints = pose_estimator.estimate(copy.deepcopy(frame_resized))
        
        if opt.img_show:
            cv2.imshow(f'Current pose estimation Frame', cv2.resize(frame_keypoints, (1280, 720), interpolation=cv2.INTER_CUBIC))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if opt.save_video:
            out_video.write( cv2.resize(frame_keypoints, (1280, 720)) )
             
        count += 1

    cap.release()
    cv2.destroyAllWindows()
    print("Finish frame batch pose estimation.")
