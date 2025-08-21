"""
This script downloads the COCO dataset from the Hugging Face Hub.
"""
from datasets import load_dataset

def download_coco():
    """
    Downloads the COCO dataset from the Hugging Face Hub.
    """
    print("Downloading COCO dataset...")
    dataset = load_dataset("detection-datasets/coco")
    print("Dataset downloaded successfully!")
    print("Dataset information:")
    print(dataset)
    print("Dataset cache files:")
    print(dataset.cache_files)

if __name__ == "__main__":
    download_coco()
