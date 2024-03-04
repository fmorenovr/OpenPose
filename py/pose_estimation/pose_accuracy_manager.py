import numpy as np

class PoseAccuracyManager:

    @staticmethod
    # Method responsible for calculating the average accuracy over all pose keypoints
    def get_pose_accuracy(pose_keypoints):
        # Calculate overall score confiability
        pose_accuracy = 0
        poses_considered = 0

        if len(pose_keypoints) < 1:
            return 0

        for item in pose_keypoints:
            joint_accuracy = item[2]
            if joint_accuracy > 0:
                # The third position in every pose keypoints refer to its data confiability
                pose_accuracy += joint_accuracy
                poses_considered += 1

        return pose_accuracy / poses_considered

    @staticmethod
    def get_highest_accuracy(pose_keypoints):
        if type(pose_keypoints) == np.float64:
            return pose_keypoints

        n_poses = len(pose_keypoints)
        pose_accuracies = [0] * n_poses

        for i in range(n_poses):
            pose_accuracy = PoseAccuracyManager.get_pose_accuracy(pose_keypoints[i])

            pose_accuracies[i] = pose_accuracy

        highest_accuracy_index = pose_accuracies.index(max(pose_accuracies))

        return np.array(pose_keypoints[highest_accuracy_index])
