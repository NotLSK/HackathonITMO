from ultralytics import YOLO
import torch


class ProductDetector:
    def __init__(self, model_path="/content/yolov5_sku_pretrained.pt"):
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path)

    def count_objects(self, image):
        prediction_result = self.model(image)
        return prediction_result.pred[0].shape[0]


class EmptySpaceDetector:
    def __init__(self, model_path="/content/yolov5_empty_shelf_detector.pt"):
        self.model = YOLO(model_path)

    def count_objects(self, image):
        prediction_result = self.model(image)
        return prediction_result[0].boxes.data.shape[0]


class ShelfAnalyser:
    def __init__(
        self,
        product_detector_path="/app/ml_models/weights/yolov5_sku_pretrained.pt",
        empty_shelf_detector="/app/ml_models/weights/yolov8_empty_shelf_detector.pt",
    ):

        self.product_model = ProductDetector(product_detector_path)
        self.empty_space_detector = EmptySpaceDetector(empty_shelf_detector)

    def count_objects(self, image):
        products_count = self.product_model.count_objects(image)
        empty_space_count = self.empty_space_detector.count_objects(image)

        return {
            "total_items": products_count,
            "total_empty_space": empty_space_count,
        }
