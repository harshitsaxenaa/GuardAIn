import math

class ObjectProcessor:
    def __init__(self):
        
        self.previous_centers = {}

    def process(self, detections):
        valid_detections = []

        for box in detections:
            x, y, w, h = box
            center_x = (2 * x + w) // 2
            center_y = (2 * y + h) // 2

            is_duplicate = False
            for prev_center in self.previous_centers.values():
                distance = math.hypot(center_x - prev_center[0], center_y - prev_center[1])
                if distance < 35:
                    is_duplicate = True
                    break

            if not is_duplicate:
                valid_detections.append([x, y, w, h])
                self.previous_centers[len(self.previous_centers)] = (center_x, center_y)

        updated_centers = {}
        for i, box in enumerate(valid_detections):
            x, y, w, h = box
            cx = (2 * x + w) // 2
            cy = (2 * y + h) // 2
            updated_centers[i] = (cx, cy)

        self.previous_centers = updated_centers.copy()
        return valid_detections
