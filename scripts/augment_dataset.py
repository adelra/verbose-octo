import argparse
import os
import cv2
import numpy as np
import albumentations as A
from tqdm import tqdm

def parse_yolo_label(label_path, img_width, img_height):
    """Parses a YOLO format label file."""
    boxes = []
    with open(label_path, 'r') as f:
        for line in f:
            parts = list(map(float, line.strip().split()))
            class_id = int(parts[0])
            # YOLO format: class_id center_x center_y width height (normalized)
            # Convert to x_min, y_min, x_max, y_max (absolute) for albumentations
            center_x, center_y, w, h = parts[1:]
            x_min = (center_x - w / 2) * img_width
            y_min = (center_y - h / 2) * img_height
            x_max = (center_x + w / 2) * img_width
            y_max = (center_y + h / 2) * img_height
            boxes.append([x_min, y_min, x_max, y_max, class_id])
    return boxes

def format_yolo_label(boxes, img_width, img_height):
    """Formats bounding boxes back to YOLO format."""
    yolo_labels = []
    for box in boxes:
        x_min, y_min, x_max, y_max, class_id = box[:5] # Take only the first 5 elements
        
        # Convert to center_x, center_y, width, height (absolute)
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        w = x_max - x_min
        h = y_max - y_min

        # Normalize
        center_x /= img_width
        center_y /= img_height
        w /= img_width
        h /= img_height
        
        yolo_labels.append(f"{int(class_id)} {center_x:.6f} {center_y:.6f} {w:.6f} {h:.6f}")
    return yolo_labels

def augment_dataset(input_dir, output_dir, num_augmentations_per_image=1):
    """
    Augments a dataset of images and YOLO-format labels.

    Args:
        input_dir (str): Path to the input dataset directory.
        output_dir (str): Path to the output directory for augmented data.
        num_augmentations_per_image (int): Number of augmented samples to generate per original image.
    """
    images_input_path = os.path.join(input_dir, 'images')
    labels_input_path = os.path.join(input_dir, 'labels')
    
    images_output_path = os.path.join(output_dir, 'images')
    labels_output_path = os.path.join(output_dir, 'labels')

    os.makedirs(images_output_path, exist_ok=True)
    os.makedirs(labels_output_path, exist_ok=True)

    # Define augmentation pipeline
    transform = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.1),
        A.RandomBrightnessContrast(p=0.2),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5),
        A.GaussNoise(p=0.2),
        A.MotionBlur(p=0.2),
        A.MedianBlur(blur_limit=3, p=0.1),
        A.CLAHE(clip_limit=2, p=0.1),
        A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.2),
    ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_ids']))

    image_files = [f for f in os.listdir(images_input_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    for image_file in tqdm(image_files, desc="Augmenting images"):
        image_name, _ = os.path.splitext(image_file)
        image_path = os.path.join(images_input_path, image_file)
        label_path = os.path.join(labels_input_path, image_name + '.txt')

        if not os.path.exists(label_path):
            print(f"Warning: No label file found for {image_file}. Skipping.")
            continue

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_height, img_width = image.shape[:2]

        bboxes = parse_yolo_label(label_path, img_width, img_height)
        class_ids = [box[4] for box in bboxes] # Extract class_ids

        # Remove class_ids from bboxes for albumentations input
        bboxes_for_transform = [box[:4] for box in bboxes]

        for i in range(num_augmentations_per_image):
            augmented = transform(image=image, bboxes=bboxes_for_transform, class_ids=class_ids)
            aug_image = augmented['image']
            aug_bboxes = augmented['bboxes']
            aug_class_ids = augmented['class_ids']

            # Re-attach class_ids to augmented bboxes
            final_aug_bboxes = [list(bbox) + [class_id] for bbox, class_id in zip(aug_bboxes, aug_class_ids)]

            aug_image_name = f"{image_name}_aug_{i}.jpg"
            aug_label_name = f"{image_name}_aug_{i}.txt"

            cv2.imwrite(os.path.join(images_output_path, aug_image_name), cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR))
            
            aug_yolo_labels = format_yolo_label(final_aug_bboxes, aug_image.shape[1], aug_image.shape[0])
            with open(os.path.join(labels_output_path, aug_label_name), 'w') as f:
                for line in aug_yolo_labels:
                    f.write(line + '\n')

def main():
    parser = argparse.ArgumentParser(description="Augment a dataset of images and YOLO-format labels.")
    parser.add_argument("--input_dir", type=str, required=True, help="Path to the input dataset directory (e.g., 'data/train').")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to the output directory for augmented data.")
    parser.add_argument("--num_augmentations_per_image", type=int, default=1,
                        help="Number of augmented samples to generate per original image.")
    
    args = parser.parse_args()

    augment_dataset(args.input_dir, args.output_dir, args.num_augmentations_per_image)
    print(f"Dataset augmentation complete. Augmented data saved to {args.output_dir}")

if __name__ == "__main__":
    main()
