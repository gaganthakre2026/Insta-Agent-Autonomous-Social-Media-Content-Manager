#!/usr/bin/env python
"""Save generated image to disk for inspection."""
import requests
import base64

prompt = "beautiful sunset beach"
body = {"prompt": prompt}

response = requests.post(
    "http://localhost:8000/api/v1/content/generate-image-with-content",
    json=body,
    timeout=30
)

data = response.json()
image_url = data['image_url']

# Extract base64 data and save
if image_url.startswith('data:image/'):
    base64_data = image_url.split(',')[1]
    raw_image = base64.b64decode(base64_data)
    
    with open('generated_image.png', 'wb') as f:
        f.write(raw_image)
    
    print(f"✅ Saved image: generated_image.png ({len(raw_image)} bytes)")
