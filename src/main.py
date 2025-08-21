from ultralytics import YOLO

def main():
    # Load a pretrained YOLOv8 model
    model = YOLO("yolov8n.pt")

    # Run inference on a sample image
    # Note: You will need to provide your own image path here.
    results = model("path/to/your/image.jpg")

    # Print the results
    print(results)

if __name__ == "__main__":
    main()
