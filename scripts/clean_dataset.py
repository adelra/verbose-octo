
import os
import cv2
import numpy as np
from PIL import Image
import imagehash
from collections import Counter
import json
import argparse

def is_blurry(image_path, threshold=100.0):
    """
    Check if an image is blurry using the variance of the Laplacian.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False, 0
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var < threshold, laplacian_var
    except Exception as e:
        print(f"Could not process {image_path} for blurriness: {e}")
        return False, 0

def is_poorly_lit(image_path, threshold=50):
    """
    Check if an image is poorly lit by checking its brightness.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False, 0
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        brightness = hsv[2].mean()
        return brightness < threshold, brightness
    except Exception as e:
        print(f"Could not process {image_path} for brightness: {e}")
        return False, 0

def find_duplicate_images(image_dir, hash_size=8):
    """
    Find duplicate images in a directory using perceptual hashing.
    """
    hashes = {}
    duplicates = []
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        try:
            with Image.open(image_path) as img:
                hash = imagehash.phash(img, hash_size=hash_size)
                if hash in hashes:
                    duplicates.append((image_path, hashes[hash]))
                else:
                    hashes[hash] = image_path
        except Exception as e:
            print(f"Could not process {image_path} for duplicates: {e}")
    return duplicates

def find_corrupted_images(image_dir):
    """
    Find corrupted images in a directory.
    """
    corrupted = []
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        try:
            with Image.open(image_path) as img:
                img.verify()
        except (IOError, SyntaxError) as e:
            print(f"Corrupted image {image_path}: {e}")
            corrupted.append(image_path)
    return corrupted

def analyze_class_distribution(annotation_file):
    """
    Analyze the class distribution in a COCO annotation file.
    """
    with open(annotation_file, 'r') as f:
        data = json.load(f)
    
    category_counts = Counter()
    if 'annotations' in data:
        for ann in data['annotations']:
            category_counts[ann['category_id']] += 1
            
    return category_counts

def find_label_outliers(annotation_file, size_threshold_low=10, size_threshold_high=0.9):
    """
    Find potential label outliers based on bounding box size.
    This is a heuristic and may not always indicate incorrect labels.
    """
    with open(annotation_file, 'r') as f:
        data = json.load(f)
        
    outliers = []
    if 'annotations' not in data or 'images' not in data:
        return outliers
        
    image_dims = {img['id']: (img['width'], img['height']) for img in data['images']}
    
    for ann in data['annotations']:
        image_id = ann['image_id']
        if image_id in image_dims:
            img_w, img_h = image_dims[image_id]
            box_w, box_h = ann['bbox'][2], ann['bbox'][3]
            
            # Check for very small boxes
            if box_w < size_threshold_low or box_h < size_threshold_low:
                outliers.append((ann['id'], 'very_small'))
                
            # Check for very large boxes
            if box_w > img_w * size_threshold_high or box_h > img_h * size_threshold_high:
                outliers.append((ann['id'], 'very_large'))
                
    return outliers


def clean_dataset(image_dir, annotation_file):
    """
    Run the full dataset cleaning process.
    """
    print("Starting dataset cleaning process...")

    print("
1. Finding corrupted images...")
    corrupted_images = find_corrupted_images(image_dir)
    print(f"Found {len(corrupted_images)} corrupted images.")

    print("
2. Finding duplicate images...")
    duplicate_images = find_duplicate_images(image_dir)
    print(f"Found {len(duplicate_images)} pairs of duplicate images.")

    print("
3. Checking for blurry images...")
    blurry_images = []
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        is_blur, var = is_blurry(image_path)
        if is_blur:
            blurry_images.append((image_path, var))
    print(f"Found {len(blurry_images)} blurry images.")

    print("
4. Checking for poorly lit images...")
    poorly_lit_images = []
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        is_dark, brightness = is_poorly_lit(image_path)
        if is_dark:
            poorly_lit_images.append((image_path, brightness))
    print(f"Found {len(poorly_lit_images)} poorly lit images.")

    if annotation_file:
        print("
5. Analyzing class distribution...")
        class_distribution = analyze_class_distribution(annotation_file)
        print("Class distribution:", class_distribution)

        print("
6. Finding label outliers...")
        label_outliers = find_label_outliers(annotation_file)
        print(f"Found {len(label_outliers)} potential label outliers.")

    print("
Cleaning process finished.")
    
    # In a real scenario, you would now programmatically remove or flag these files.
    # For this script, we are just printing the results.

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Clean a COCO dataset.")
    parser.add_argument("--image_dir", type=str, required=True, help="Directory containing the images.")
    parser.add_argument("--annotation_file", type=str, help="Path to the COCO annotation file.")
    args = parser.parse_args()
    
    clean_dataset(args.image_dir, args.annotation_file)
