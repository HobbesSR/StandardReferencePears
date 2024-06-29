import os
import re
import json
from PIL import Image
from collections import defaultdict

def extract_sref(filename):
    match = re.search(r'--sref_(\d+)', filename)
    return match.group(1) if match else None

def create_resolutions(image_path, output_dir, base_name):
    sizes = {'S': (256, 256), 'M': (512, 512), 'L': (1024, 1024)}
    image = Image.open(image_path)
    for label, size in sizes.items():
        resized_image = image.resize(size, Image.ANTIALIAS)
        output_path = os.path.join(output_dir, f"{base_name}{label}.jpg")
        resized_image.save(output_path)

def process_images(input_directory, output_directory):
    image_groups = defaultdict(list)
    for subdir, _, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                sref = extract_sref(filename)
                if sref:
                    base_name = os.path.splitext(filename)[0]
                    match = re.search(r'(\d)$', base_name)
                    if match:
                        image_number = match.group(1)
                    else:
                        continue
                    
                    sref_dir = os.path.join(output_directory, sref)
                    if not os.path.exists(sref_dir):
                        os.makedirs(sref_dir)
                    
                    image_path = os.path.join(subdir, filename)
                    create_resolutions(image_path, sref_dir, image_number)

                    for label in ['S', 'M', 'L']:
                        rel_path = os.path.join("images/pears", sref, f"{image_number}{label}.jpg")
                        image_groups[sref].append(rel_path)
    
    return {sref: images for sref, images in image_groups.items() if len(images) == 12}  # 4 images x 3 sizes

def main():
    input_directory = './images_in'  # Input directory
    output_directory = './images/pears'  # Output directory
    grouped_images = process_images(input_directory, output_directory)
    
    with open('gallery_data.json', 'w') as f:
        json.dump(grouped_images, f, indent=2)
    
    print(f"Gallery data JSON generated. Total SREF groups: {len(grouped_images)}")
    print("Data saved to 'gallery_data.json'")

if __name__ == "__main__":
    main()
