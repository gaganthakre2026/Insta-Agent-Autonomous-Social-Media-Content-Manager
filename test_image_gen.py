#!/usr/bin/env python
"""Quick test of PIL image generation."""
import base64
import io
from PIL import Image, ImageDraw, ImageFilter

# Create a test gradient image with PIL
img = Image.new('RGB', (1024, 768))
pixels = img.load()

# Create a beautiful blue-to-yellow gradient
for y in range(768):
    ratio = y / 768
    r = int(0 * (1 - ratio) + 255 * ratio)
    g = int(119 * (1 - ratio) + 200 * ratio)
    b = int(182 * (1 - ratio) + 0 * ratio)
    for x in range(1024):
        pixels[x, y] = (r, g, b)

# Add text
draw = ImageDraw.Draw(img)
draw.text((100, 350), "Beautiful Gradient Image", fill=(255, 255, 255))

# Apply blur
img = img.filter(ImageFilter.GaussianBlur(radius=2))

# Save to base64
buffer = io.BytesIO()
img.save(buffer, format='PNG', quality=95)
buffer.seek(0)
data = buffer.getvalue()

print(f"✅ Generated image: {len(data)} bytes")
print(f"✅ Base64 length: {len(base64.b64encode(data))}")
