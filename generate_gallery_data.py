import os
import re
import json
from collections import defaultdict

def extract_sref(filename):
    match = re.search(r'--sref_(\d+)', filename)
    return match.group(1) if match else None

def process_images(root_directory):
    image_groups = defaultdict(list)
    for subdir, _, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                sref = extract_sref(filename)
                if sref:
                    rel_path = os.path.relpath(os.path.join(subdir, filename), root_directory)
                    image_groups[sref].append(rel_path)
    return {sref: images for sref, images in image_groups.items() if len(images) == 4}

def main():
    root_directory = '.'  # Current directory
    grouped_images = process_images(root_directory)
    
    with open('gallery_data.json', 'w') as f:
        json.dump(grouped_images, f, indent=2)
    
    print(f"Gallery data JSON generated. Total SREF groups: {len(grouped_images)}")
    print("Data saved to 'gallery_data.json'")

if __name__ == "__main__":
    main()