import sys
import cv2
import numpy as np
from console_logging.console import Console
from py.utils import get_absolute_path
from .pose_area_filter import PoseAreaFilter
from .pose_accuracy_manager import PoseAccuracyManager

class PoseEstimation:
    # Ids to access pose points
    LEFT_LEG_IDS = [14, 20, 19, 21]
    RIGHT_LEG_IDS = [11, 23, 22, 24]

    def __init__(self, max_people=10, frame_width = 640, frame_height = 360, xywh_type=False):
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.xywh_type = xywh_type
        self.console_logger = Console()
        self.max_people = max_people
        self.openpose, self.opWrapper = PoseEstimation.setup(self.max_people, self.console_logger)
        self.area_filter = PoseAreaFilter()
        self.accuracy_manager = PoseAccuracyManager()

    def apply_area_filter(self, pose_keypoints):
        new_keypoints = []

        if type(pose_keypoints) == np.float64:
            return new_keypoints

        for i in range(len(pose_keypoints)):
            pose_position = PoseEstimation.get_pose_feet_position(pose_keypoints[0], xywh_type=self.xywh_type)

            # Add to new keypoints if pose is inside roi
            if self.area_filter.is_point_inside_area(pose_position):
                new_keypoints.append(pose_keypoints[i].copy())

        if len(new_keypoints) > 1:
            new_keypoints = self.accuracy_manager.get_highest_accuracy(new_keypoints)

        return np.array(new_keypoints)

    @staticmethod
    def setup(max_people, console_logger):
        try:
            #path = get_absolute_path("openpose/build/python/")
            #sys.path.append(path)

            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the
            # OpenPose/python module from there. This will install OpenPose and the python library at your desired
            # installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            #from openpose import pyopenpose as op
            import pyopenpose as op

        except ImportError as e:
            console_logger.error('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` '
                  'in CMake and have this Python script in the right folder?')
            raise e
        
        model_path = get_absolute_path("openpose/models/")
        params = dict()
        params["model_folder"] = model_path
        params["face"] = True
        params["hand"] = True
        params["model_pose"] = "BODY_25"
        params["number_people_max"] = max_people
        params["net_resolution"] = "-1x304"

        # Construct it from system arguments
        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        return op, opWrapper

    def estimate(self, image):
        datum = self.openpose.Datum()
        datum.cvInputData = image
        self.opWrapper.emplaceAndPop(self.openpose.VectorDatum([datum]))
        
        pose_keypoints = datum.poseKeypoints
        if type(pose_keypoints) is not np.ndarray:
            pose_keypoints = np.nan
            
        face_keypoints = datum.faceKeypoints
        if type(face_keypoints) is not np.ndarray:
            face_keypoints = np.nan
            
        left_hand_keypoints = datum.handKeypoints[0]
        if type(left_hand_keypoints) is not np.ndarray:
            left_hand_keypoints = np.nan
            
        right_hand_keypints = datum.handKeypoints[1]
        if type(right_hand_keypints) is not np.ndarray:
            right_hand_keypints = np.nan

        pose_keypoints = np.round(pose_keypoints, 2)
        face_keypoints = np.round(face_keypoints, 2)
        left_hand_keypoints = np.round(left_hand_keypoints, 2)
        right_hand_keypints = np.round(right_hand_keypints, 2)
        
        keypoints_dict = {"body": pose_keypoints, 
                       "face": face_keypoints, 
                       "left_hand": left_hand_keypoints, 
                       "right_hand": right_hand_keypints, 
                      }
        
        result_frame = datum.cvOutputData

        return keypoints_dict, result_frame

    def adjust_frame(self, frame):
        # Limit pose_estimation search area when strictly searching for machine operators
        input_image = cv2.resize(frame, (self.frame_width, self.frame_height), interpolation=cv2.INTER_AREA)
        return input_image

    @staticmethod
    def is_pose_in_roi(point, roi):
        x1, y1, w, h = roi

        x, y = point

        if x1 < x < x1 + w:
            if y1 < y < y1 + h:
                return True

        return False

    def remove_outsider_operators(self, pose_keypoints, operator_roi, operation_string):
        if operator_roi is None:
            operator_roi = []

        new_keypoints = []

        if type(pose_keypoints) == np.float64 or len(operator_roi) != 4:
            return new_keypoints

        for i in range(len(pose_keypoints)):
            try:
                arr = np.asarray(pose_keypoints[i])
                arr_x = []
                arr_y = []
                length = len(arr[:])
                n_points = 0

                for j in range(length):
                    x_pose = arr[j, 0]
                    arr_x.append(x_pose)
                    y_pose = arr[j, 1]
                    arr_y.append(y_pose)

                    if x_pose > 0 and y_pose > 0:
                        n_points += 1

                length = len(arr_x)
                if length > 1:
                    sum_x = np.sum(arr_x)
                    sum_y = np.sum(arr_y)

                    x = int(sum_x / n_points)
                    y = int(sum_y / n_points)
                    result = x, y

                    # Add to new keypoints if pose is inside roi
                    if self.is_pose_in_roi(result, operator_roi):
                        new_keypoints.append(pose_keypoints[i].copy())
            except Exception as e:
                print("Error:", e)

        new_keypoints = np.array(new_keypoints)

        return new_keypoints

    @staticmethod
    def get_avg_pose_position(pose_keypoints):
        arr_x = []
        arr_y = []

        for j in range(len(pose_keypoints)):
            x_pose = pose_keypoints[j, 0]
            y_pose = pose_keypoints[j, 1]

            if x_pose > 0 and y_pose > 0:
                arr_x.append(x_pose)
                arr_y.append(y_pose)

        avg_pose_position = [0, 0]
        n_points = len(arr_x)
        if n_points > 0 and len(arr_y):
            sum_x = np.sum(arr_x)
            sum_y = np.sum(arr_y)

            x = int(sum_x / n_points)
            y = int(sum_y / n_points)
            avg_pose_position = x, y

        return avg_pose_position

    @staticmethod
    def get_pose_feet_position(pose_keypoints, reid_bbox=None, xywh_type=False):
        if reid_bbox is not None:
            if xywh_type:
                x1, y1, w, h = reid_bbox
                pos_x, pos_y = x1 + w / 2, y1 + h
            else:
                x1, y1, x2, y2 = reid_bbox
                pos_x, pos_y = x1 + (x2 - x1)/2, y2

        if type(pose_keypoints) is np.float64 or len(pose_keypoints) == 0:
            return np.nan, np.nan

        if len(pose_keypoints.shape) > 2:
            pose_keypoints = pose_keypoints[0]

        left_foot_pos = PoseEstimation.get_left_foot_position(pose_keypoints)
        right_foot_pos = PoseEstimation.get_right_foot_position(pose_keypoints)
        pose_position = PoseEstimation.get_pose_position(left_foot_pos, right_foot_pos, reid_bbox, xywh_type)

        return pose_position

    @staticmethod
    def get_left_foot_position(pose_keypoints):
        left_foot_pos = [0, 0]
        for left_joint_id in PoseEstimation.LEFT_LEG_IDS:
            left_foot_pos[0], left_foot_pos[1], _ = pose_keypoints[left_joint_id, :]
            if left_foot_pos[0] != 0.0 and left_foot_pos[1] != 0.0:
                break
        return left_foot_pos

    @staticmethod
    def get_right_foot_position(pose_keypoints):
        right_foot_pos = [0, 0]
        for right_joint_id in PoseEstimation.RIGHT_LEG_IDS:
            right_foot_pos[0], right_foot_pos[1], _ = pose_keypoints[right_joint_id, :]
            if right_foot_pos[0] != 0.0 and right_foot_pos[1] != 0.0:
                break
        return right_foot_pos

    @staticmethod
    def get_pose_position(left_foot_pos, right_foot_pos, reid_bbox, xywh_type):
        if reid_bbox is not None:
            if xywh_type:
                x1, y1, w, h = reid_bbox
                pos_x, pos_y = x1 + w / 2, y1 + h
            else:
                x1, y1, x2, y2 = reid_bbox
                pos_x, pos_y = x1 + (x2 - x1)/2, y2
        
        elif left_foot_pos[0] != 0 and right_foot_pos != 0:
            pos_x = round((left_foot_pos[0] + right_foot_pos[0]) / 2, 0)
            pos_y = round((left_foot_pos[1] + right_foot_pos[1]) / 2, 0)
        else:
            pos_x, pos_y = np.nan, np.nan
        return pos_x, pos_y
