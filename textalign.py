import os
import cv2
import numpy as np
import argparse
import logging
import imghdr

SUPPORTED_IMAGE_FORMATS = {'.jpeg', '.jpg', '.png', '.bmp', '.tiff', '.tif'}

class TextBoundingBoxExtractor:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.intermediate_files = []
        
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def load_image(self, input_path):
        file_type = imghdr.what(input_path)
        if file_type and file_type.lower() in SUPPORTED_IMAGE_FORMATS:
            return cv2.imread(input_path)
        else:
            logging.error(f'Skipped unsupported image format: {input_path}')
            return None

    def process_image(self, input_path):
        image = self.load_image(input_path)
        if image is not None:
            try:
                edge_image = self.apply_edge_detection(image)
                contours = self.find_contours(edge_image)
                filtered_image = self.filter_small_regions(contours, edge_image)
                mask = self.create_mask(filtered_image)
                blackened_image = self.blacken_image(image, mask)
                rotated_rect = self.get_rotated_rect(filtered_image)
                angle = self.calculate_unrotation_angle(rotated_rect)
                unrotated_image = self.unrotate_image(blackened_image, angle, mask)
                intermediate_filename = self.get_intermediate_filename(input_path, "unrotated")
                self.save_result(intermediate_filename, unrotated_image)
                self.cleanup_intermediate_files()
            except cv2.error as e:
                logging.error(f'OpenCV Error processing {input_path}: {e}')
            except Exception as e:
                logging.error(f'Error processing {input_path}: {e}')
        else:
            logging.warning(f'Skipped unsupported image: {input_path}')

    def apply_edge_detection(self, image):
        return cv2.Canny(image, 50, 200)

    def find_contours(self, edge_image):
        contours = cv2.findContours(edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours[0] if len(contours) == 2 else contours[1]

    def filter_small_regions(self, contours, edge_image):
        filtered_image = np.zeros_like(edge_image)
        for cntr in contours:
            area = cv2.contourArea(cntr)
            if area > 20:
                cv2.drawContours(filtered_image, [cntr], 0, 255, 1)
        return filtered_image

    def create_mask(self, filtered_image):
        points = np.column_stack(np.where(filtered_image.transpose() > 0))
        hull = cv2.convexHull(points)
        mask = np.zeros_like(filtered_image, dtype=np.uint8)
        cv2.fillPoly(mask, [hull], 255)
        return mask

    def blacken_image(self, image, mask):
        return cv2.bitwise_and(image, image, mask=mask)

    def get_rotated_rect(self, filtered_image):
        return cv2.minAreaRect(cv2.convexHull(np.column_stack(np.where(filtered_image.transpose() > 0)))

    def calculate_unrotation_angle(self, rotated_rect):
        (center), (width, height), angle = rotated_rect
        if angle < -45:
            angle = -(90 + angle)
        else:
            if width > height:
                angle = -(90 + angle)
            else:
                angle = -angle
        return -angle

    def unrotate_image(self, image, angle, mask):
        M = cv2.getRotationMatrix2D((image.shape[1] // 2, image.shape[0] // 2), angle, scale=1.0)
        return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0)

    def save_result(self, filename, result_image):
        output_path = os.path.join(self.output_directory, filename)
        cv2.imwrite(output_path, result_image)
        logging.info(f'Saved: {output_path}')
        return output_path

    def get_intermediate_filename(self, input_path, step):
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        intermediate_filename = f"{name}_{step}{ext}"
        self.intermediate_files.append(intermediate_filename)
        return intermediate_filename

    def cleanup_intermediate_files(self):
        for filename in self.intermediate_files:
            file_path = os.path.join(self.output_directory, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def process_images(self):
        for filename in os.listdir(self.input_directory):
            if filename.lower().endswith(tuple(SUPPORTED_IMAGE_FORMATS)):
                input_path = os.path.join(self.input_directory, filename)
                self.process_image(input_path)

def main():
    parser = argparse.ArgumentParser(description='Process images to extract text bounding boxes.')
    parser.add_argument('input_directory', help='Path to the directory containing input images')
    parser.add_argument('output_directory', help='Path to the directory to save the results')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='processing.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info(f'Started processing images in {args.input_directory}')
    
    extractor = TextBoundingBoxExtractor(args.input_directory, args.output_directory)
    extractor.process_images()

    logging.info(f'Finished processing images in {args.input_directory}')

if __name__ == "__main__":
    main()
