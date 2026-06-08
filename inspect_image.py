#!/usr/bin/env python
"""Decode and inspect the image returned by the API."""
import requests
import base64
import json

prompt = "test forest landscape"
body = {"prompt": prompt}

response = requests.post(
    "http://localhost:8000/api/v1/content/generate-image-with-content",
    json=body,
    timeout=30
)

data = response.json()
image_url = data['image_url']

# Extract base64 data
if image_url.startswith('data:image/'):
    # Format: data:image/png;base64,<data>
    base64_data = image_url.split(',')[1]
    raw_image = base64.b64decode(base64_data)
    
    print(f"✅ Image URL length in chars: {len(image_url)}")
    print(f"✅ Base64 data length in chars: {len(base64_data)}")
    print(f"✅ Decoded image size: {len(raw_image)} bytes")
    print(f"✅ First 20 bytes: {raw_image[:20]}")
    
    # Check if it's a valid PNG
    if raw_image[:8] == b'\x89PNG\r\n\x1a\n':
        print(f"✅ Valid PNG file detected!")
    elif raw_image[:2] == b'\xff\xd8':
        print(f"✅ Valid JPEG file detected!")
    else:
        print(f"⚠️ Unknown image format. First bytes: {raw_image[:20]}")
        print(f"⚠️ As hex: {raw_image[:20].hex()}")

print(f"\n✅ Caption: {data['caption']}")
print(f"✅ Hashtags: {data['hashtags']}")
