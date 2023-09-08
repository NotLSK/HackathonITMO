import cv2
import numpy as np


class SaleChecker:
    def __init__(
        self,
        lower_thresh=[20, 50, 70],
        upper_thresh=[50, 255, 255],
        yellow_area_thresh=0.4,
    ):
        self.lower_thresh = np.array(lower_thresh, np.uint8)
        self.upper_thresh = np.array(upper_thresh, np.uint8)
        self.yellow_area_thresh = yellow_area_thresh

    def is_sale(self, image: np.ndarray) -> bool:

        image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(image_hsv, self.lower_thresh, self.upper_thresh)

        promo_flag = ((mask != 0).sum() / mask.size) >= self.yellow_area_thresh

        return bool(promo_flag)
