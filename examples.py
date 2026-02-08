#!/usr/bin/env python3
"""
Example usage of the PNG to BIN converter
"""

from png_to_bin import convert_png_to_bin, read_bin_to_png
from PIL import Image


def example_1_basic_conversion():
    """Example 1: Basic PNG to BIN conversion"""
    print("=" * 50)
    print("Example 1: Basic PNG to BIN Conversion")
    print("=" * 50)
    
    # Create a sample image
    img = Image.new('RGB', (100, 100), color='red')
    img.save('example1_original.png')
    print("✓ Created example1_original.png")
    
    # Convert to BIN
    success, message = convert_png_to_bin('example1_original.png', 'example1_converted.bin')
    print(f"✓ {message}")
    print()


def example_2_bin_back_to_png():
    """Example 2: Convert BIN back to PNG"""
    print("=" * 50)
    print("Example 2: Convert BIN Back to PNG")
    print("=" * 50)
    
    # Convert back to PNG
    success, message = read_bin_to_png('example1_converted.bin', 'example1_restored.png')
    print(f"✓ {message}")
    
    # Verify
    original = Image.open('example1_original.png')
    restored = Image.open('example1_restored.png')
    print(f"✓ Original size: {original.size}, Restored size: {restored.size}")
    print()


def example_3_without_metadata():
    """Example 3: Convert without metadata (raw pixel data only)"""
    print("=" * 50)
    print("Example 3: Raw Pixel Data (No Metadata)")
    print("=" * 50)
    
    # Create image
    img = Image.new('RGB', (50, 50), color='blue')
    img.save('example3_original.png')
    
    # Convert without metadata
    success, message = convert_png_to_bin(
        'example3_original.png', 
        'example3_raw.bin',
        include_metadata=False
    )
    print(f"✓ {message}")
    
    # Note: Cannot restore raw BIN without knowing dimensions
    print("ℹ Note: Raw BIN files cannot be restored without external dimension info")
    print()


def example_4_batch_conversion():
    """Example 4: Batch convert multiple PNG files"""
    print("=" * 50)
    print("Example 4: Batch Conversion")
    print("=" * 50)
    
    colors = ['red', 'green', 'blue', 'yellow', 'magenta']
    
    for i, color in enumerate(colors, 1):
        # Create image
        img = Image.new('RGB', (50, 50), color=color)
        png_file = f'example4_color_{i}.png'
        bin_file = f'example4_color_{i}.bin'
        
        img.save(png_file)
        success, message = convert_png_to_bin(png_file, bin_file)
        print(f"✓ {color.capitalize()}: {message}")
    print()


def example_5_complex_image():
    """Example 5: Convert a more complex image"""
    print("=" * 50)
    print("Example 5: Complex Image with Gradient")
    print("=" * 50)
    
    # Create a gradient image
    img = Image.new('RGBA', (200, 200))
    pixels = img.load()
    
    for y in range(200):
        for x in range(200):
            r = int((x / 200) * 255)
            g = int((y / 200) * 255)
            b = 128
            a = int(((x + y) / 400) * 255)
            pixels[x, y] = (r, g, b, a)
    
    img.save('example5_gradient.png')
    print("✓ Created gradient image")
    
    # Convert to BIN
    success, message = convert_png_to_bin('example5_gradient.png', 'example5_gradient.bin')
    print(f"✓ {message}")
    
    # Check file sizes
    import os
    png_size = os.path.getsize('example5_gradient.png')
    bin_size = os.path.getsize('example5_gradient.bin')
    print(f"  PNG size: {png_size:,} bytes")
    print(f"  BIN size: {bin_size:,} bytes (includes metadata)")
    print()


if __name__ == '__main__':
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " PNG to BIN Converter - Usage Examples ".center(48) + "║")
    print("╚" + "=" * 48 + "╝")
    print()
    
    example_1_basic_conversion()
    example_2_bin_back_to_png()
    example_3_without_metadata()
    example_4_batch_conversion()
    example_5_complex_image()
    
    print("=" * 50)
    print("All examples completed successfully!")
    print("=" * 50)
