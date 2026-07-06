import os
from PIL import Image, ImageDraw

def create_app_icon():
    print("Generating premium application icon...")
    # Create a 256x256 image with transparent background
    im = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Draw a beautiful circle with radial-like linear gradient from deep purple to pink
    for y in range(256):
        for x in range(256):
            # Distance from center
            dx = x - 128
            dy = y - 128
            dist = (dx*dx + dy*dy)**0.5
            if dist <= 110:
                # Gradient color interpolation (purple to pink)
                factor_x = x / 256.0
                factor_y = y / 256.0
                r = int(139 + factor_x * 98)  # 139 to 237
                g = int(92 - factor_y * 20)   # 92 to 72
                b = int(246 - factor_x * 93)  # 246 to 153
                
                # Smooth anti-aliased edge
                alpha = 255
                if dist > 106:
                    alpha = int(255 * (110 - dist) / 4)
                
                im.putpixel((x, y), (r, g, b, alpha))

    # Draw a clean, premium white download arrow + disc base
    # Arrow stem
    draw.rectangle([118, 55, 138, 120], fill="white")
    # Arrow head
    draw.polygon([(95, 120), (161, 120), (128, 155)], fill="white")
    # Disk base
    draw.arc([75, 155, 181, 195], start=20, end=160, fill="white", width=12)

    # Save as ICO with multiple sizes for standard Windows scaling
    icon_path = "app_icon.ico"
    im.save(icon_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print(f"[OK] Icon created successfully at: {os.path.abspath(icon_path)}")

if __name__ == "__main__":
    create_app_icon()
