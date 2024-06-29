import os
import re
from collections import defaultdict
import json

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
    print(f"Image Groups: {dict(image_groups)}")
    return {sref: images for sref, images in image_groups.items() if len(images) == 4}

def generate_html(grouped_images):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Standard Reference Pear Gallery</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background-color: #f0f0f0; 
                perspective: 1px;
                height: 100vh;
                overflow-x: hidden;
                overflow-y: auto;
            }}
            .parallax-container {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                transform-style: preserve-3d;
            }}
            .parallax-background {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                transform: translateZ(-1px) scale(2);
                background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="%23f0f0f0"/><path d="M0 0l100 100M100 0L0 100" stroke="%23e0e0e0" stroke-width="1"/></svg>');
                background-repeat: repeat;
                z-index: -1;
            }}
            .content {{
                position: relative;
                z-index: 1;
                background-color: rgba(240, 240, 240, 0.9);
                transform: translateZ(0);
                padding: 20px;
            }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            h1 {{ color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }}
            .credit {{ font-style: italic; color: #7f8c8d; }}
            .controls {{ 
                position: fixed; 
                top: 20px; 
                right: 20px; 
                background-color: white; 
                padding: 15px; 
                border-radius: 10px; 
                box-shadow: 0 0 15px rgba(0,0,0,0.1);
                z-index: 1000;
            }}
            .gallery {{ display: flex; flex-wrap: wrap; justify-content: center; }}
            .item {{ 
                margin: 20px; 
                background-color: white; 
                border-radius: 15px; 
                overflow: hidden; 
                box-shadow: 0 0 20px rgba(0,0,0,0.1); 
                position: relative; 
                transition: all 0.3s ease; 
            }}
            .item:hover {{ transform: scale(1.05); }}
            .background {{ 
                position: absolute; 
                top: 0; 
                left: 0; 
                width: 100%; 
                height: 100%; 
                background-size: cover; 
                background-position: center; 
                filter: blur(10px); 
                opacity: 0.5; 
            }}
            .images-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 10px;
            }}
            .images {{ 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 5px; 
                padding: 5px; 
                position: relative; 
            }}
            .images img {{ width: 100%; height: auto; object-fit: cover; }}
            .sref-container {{
                padding: 10px;
                text-align: center;
                background-color: rgba(240, 240, 240, 0.9);
                margin-top: 10px;
            }}
            .sref {{ 
                background-color: rgba(44, 62, 80, 0.8); 
                color: white; 
                padding: 10px;
                border-radius: 5px;
                display: inline-block;
            }}
            .copy-btn {{ 
                cursor: pointer; 
                padding: 5px 10px; 
                background-color: #27ae60; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                transition: background-color 0.3s ease; 
                margin-left: 10px;
            }}
            .copy-btn:hover {{ background-color: #2ecc71; }}
            .size-btn {{
                cursor: pointer;
                padding: 5px 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                margin: 0 5px;
                transition: background-color 0.3s ease;
            }}
            .size-btn:hover {{ background-color: #2980b9; }}
            .size-btn.active {{ background-color: #2980b9; }}
        </style>
    </head>
    <body>
        <div class="parallax-container">
            <div class="parallax-background"></div>
        </div>
        <div class="content">
            <div class="header">
                <h1>Standard Reference Pear Gallery</h1>
                <div class="credit">Generated by Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest.</div>
            </div>
            <div class="controls">
                <span>Image Size: </span>
                <button class="size-btn" data-size="150">XS</button>
                <button class="size-btn" data-size="225">S</button>
                <button class="size-btn active" data-size="300">M</button>
                <button class="size-btn" data-size="375">L</button>
                <button class="size-btn" data-size="450">XL</button>
            </div>
            <div class="gallery">
                <!-- Gallery items will be dynamically inserted here -->
            </div>
        </div>
        <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(function() {{
                    alert('SREF code copied to clipboard!');
                }}, function(err) {{
                    console.error('Could not copy text: ', err);
                }});
            }}

            const gallery = document.querySelector('.gallery');
            const sizeButtons = document.querySelectorAll('.size-btn');

            function updateSize(size) {{
                document.querySelectorAll('.item').forEach(item => {{
                    item.style.width = `${{size}}px`;
                    item.style.height = 'auto';
                }});
                sizeButtons.forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.size === size.toString());
                }});
            }}

            sizeButtons.forEach(btn => {{
                btn.addEventListener('click', () => updateSize(parseInt(btn.dataset.size)));
            }});

            function createGalleryItem(sref, images) {{
                const item = document.createElement('div');
                item.className = 'item';
                item.innerHTML = `
                    <div class="images-container">
                        <div class="images">
                            ${{images.map(img => `<img src="${{img}}" alt="Pear" loading="lazy">`).join('')}}
                        </div>
                    </div>
                    <div class="sref-container">
                        <div class="sref">
                            SREF: ${{sref}}
                            <button class="copy-btn" onclick="copyToClipboard('${{sref}}')">Copy</button>
                        </div>
                    </div>
                `;
                return item;
            }}

            // Populate gallery
            const groupedImages = {json.dumps(grouped_images)};
            for (const [sref, images] of Object.entries(groupedImages)) {{
                gallery.appendChild(createGalleryItem(sref, images));
            }}

            // Initialize sizes
            updateSize(300);

            // Parallax effect
            window.addEventListener('scroll', () => {{
                const scrollY = window.scrollY;
                document.querySelector('.parallax-background').style.transform = `translateZ(-1px) scale(2) translateY(${{scrollY * 0.5}}px)`;
            }});
        </script>
    </body>
    </html>
    """
    return html

def main():
    root_directory = '.'  # Current directory
    grouped_images = process_images(root_directory)
    html_content = generate_html(grouped_images)
    
    with open('gallery.html', 'w') as f:
        f.write(html_content)
    
    print(f"Enhanced gallery HTML generated. Total SREF groups: {len(grouped_images)}")
    print("Open 'gallery.html' in a web browser to view the gallery.")

if __name__ == "__main__":
    main()
