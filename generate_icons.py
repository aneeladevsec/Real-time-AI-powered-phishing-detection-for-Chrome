#!/usr/bin/env python3
"""Generate extension icons"""

from PIL import Image, ImageDraw

# Define icon sizes and create icons
sizes = [
    (16, 'extension/icons/shield16.png'),
    (48, 'extension/icons/shield48.png'),
    (128, 'extension/icons/shield128.png')
]

for size, path in sizes:
    # Create image with gradient background (dark blue)
    img = Image.new('RGBA', (size, size), (26, 26, 46, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw shield outline and fill
    margin = size // 8
    
    # Shield shape (simplified)
    # Top left, top right, bottom right, bottom left (pointing down)
    shield_points = [
        (margin, margin),                    # Top left
        (size - margin, margin),             # Top right
        (size - margin, size // 2),          # Right middle
        (size // 2, size - margin),          # Bottom point
        (margin, size // 2)                  # Left middle
    ]
    
    # Draw filled shield in bright green (safe color)
    draw.polygon(shield_points, fill=(76, 175, 80, 255), outline=(255, 255, 255, 255))
    
    # Draw checkmark inside shield
    check_margin = size // 4
    # Checkmark coordinates (simplified)
    check_start_x = size // 3
    check_start_y = size // 2 - size // 8
    check_mid_x = size // 2 - size // 16
    check_mid_y = size // 2 + size // 8
    check_end_x = size // 2 + size // 8
    check_end_y = size // 2 - size // 8
    
    # Draw checkmark in white
    draw.line([(check_start_x, check_start_y), (check_mid_x, check_mid_y)], 
              fill=(255, 255, 255, 255), width=max(1, size // 16))
    draw.line([(check_mid_x, check_mid_y), (check_end_x, check_end_y)], 
              fill=(255, 255, 255, 255), width=max(1, size // 16))
    
    # Save image
    img.save(path)
    print(f"✅ Created {path} ({size}x{size}px)")

print("\n✅ All icons created successfully!")
