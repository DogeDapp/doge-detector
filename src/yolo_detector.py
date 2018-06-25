import cv2
from YOLOv3.model.yolo_model import YOLO

class YoloDetector(): 
    def __init__(self, obj_threshold=0.6, nms_threshold=0.5, classes_file='YOLOv3/data/coco_classes.txt'):
        self.yolo = YOLO(obj_threshold, nms_threshold, 'YOLOv3/data/yolo.h5')
        self.all_classes = self.get_classes(classes_file)

    def get_classes(self, file):
        """Get classes name.

        # Argument:
            file: classes name for database.

        # Returns
            class_names: List, classes name.

        """
        with open(file) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]

        return class_names

    def process_image(self, img):
        """Resize, reduce and expand image.

        # Argument:
            img: original image.

        # Returns
            image: ndarray(64, 64, 3), processed image.
        """
        image = cv2.resize(img, (416, 416),
                           interpolation=cv2.INTER_CUBIC)
        image = np.array(image, dtype='float32')
        image /= 255.
        image = np.expand_dims(image, axis=0)

        return image
    
    def draw(self, image, boxes, scores, classes, all_classes):
        """Draw the boxes on the image.

        # Argument:
            image: original image.
            boxes: ndarray, boxes of objects.
            classes: ndarray, classes of objects.
            scores: ndarray, scores of objects.
            all_classes: all classes name.
        """
        for box, score, cl in zip(boxes, scores, classes):
            x, y, w, h = box

            top = max(0, np.floor(x + 0.5).astype(int))
            left = max(0, np.floor(y + 0.5).astype(int))
            right = min(image.shape[1], np.floor(x + w + 0.5).astype(int))
            bottom = min(image.shape[0], np.floor(y + h + 0.5).astype(int))

            cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
            cv2.putText(image, '{0} {1:.2f}'.format(all_classes[cl], score),
                        (top, left - 6),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 0, 255), 1,
                        cv2.LINE_AA)

            print('class: {0}, score: {1:.2f}'.format(all_classes[cl], score))
            print('box coordinate x,y,w,h: {0}'.format(box))
        plt.imshow(image)
        print()

    def detect_image(self, image):
        """Use yolo v3 to detect images.

        # Argument:
            image: original image.
            yolo: YOLO, yolo model.
            all_classes: all classes name.

        # Returns:
            image: processed image.
        """
        pimage = self.process_image(image)

        boxes, classes, scores = self.yolo.predict(pimage, image.shape)

        return boxes, classes, scores
    
    def detect(self, image):
        #image = cv2.imread(image_path)
        boxes, classes, scores = self.detect_image(image)
        return boxes, classes, scores