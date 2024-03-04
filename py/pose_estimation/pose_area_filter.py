import numpy as np
import cv2


# Stellantis hardcoded parameter for poc... POSE ESTIMATION IS DESIGNED TO WORK WITH REID, areafilter is a workaround
class PoseAreaFilter:
    def __init__(self):
#        self.area = [[154, 719], [826, 252], [969, 270], [1020, 352], [986, 714]]
        self.area =[[269, 718], [792, 356], [966, 369], [923, 714]]

        if self.area_loaded():
            self.area_contour = PoseAreaFilter.convert_to_contour(self.area)

    def area_loaded(self):
        return self.area != []

    def is_point_inside_area(self, operator_position):
        area = self.area

        x, y = operator_position
        contour = np.array(area).reshape((-1, 1, 2)).astype(np.int32)
        result = cv2.pointPolygonTest(contour, (x, y), False)

        if result >= 0:
            return True
        else:
            return False

    @staticmethod
    def convert_to_contour(polygon):
        contour = np.array(polygon).reshape((-1, 1, 2)).astype(np.int32)
        return contour

    def print_area_filter(self, input_frame):
        output_frame = input_frame.copy()

        # No area defined
        if not self.area:
            return output_frame

        fra_h, fra_w, fra_channels = output_frame.shape
        poly_mask = np.zeros((fra_h, fra_w), np.uint8)
        cv2.fillPoly(poly_mask, [self.area_contour], 255)
        aux_frame = cv2.bitwise_and(output_frame,
                                    output_frame, mask=poly_mask)
        output_frame = cv2.addWeighted(output_frame, 0.5, aux_frame, 1 - 0.5, 0)
        return output_frame
