#!/usr/bin/env python3
"""
PNG to BIN File Converter
Converts PNG images to binary format with metadata
"""

import struct
import sys
from pathlib import Path
from PIL import Image


def convert_png_to_bin(png_path, bin_path=None, include_metadata=True):
    """
    Convert a PNG image to a binary file.
    
    Args:
        png_path (str or Path): Path to the PNG file
        bin_path (str or Path, optional): Path for the output BIN file.
                                         If None, uses PNG filename with .bin extension
        include_metadata (bool): Whether to include image metadata in binary
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        png_path = Path(png_path)
        
        if not png_path.exists():
            return False, f"PNG file not found: {png_path}"
        
        if not png_path.suffix.lower() == '.png':
            return False, f"File is not a PNG: {png_path}"
        
        # Open PNG image
        img = Image.open(png_path)
        
        # Set default output path if not provided
        if bin_path is None:
            bin_path = png_path.with_suffix('.bin')
        else:
            bin_path = Path(bin_path)
        
        # Convert image to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get image dimensions
        width, height = img.size
        
        # Extract pixel data
        pixel_data = img.tobytes()
        
        with open(bin_path, 'wb') as f:
            if include_metadata:
                # Write metadata header
                # Format: [MAGIC:4][WIDTH:4][HEIGHT:4][MODE:1][DATA_SIZE:4][DATA:variable]
                magic = b'PNG\x00'
                f.write(magic)
                f.write(struct.pack('<I', width))
                f.write(struct.pack('<I', height))
                f.write(struct.pack('B', 4))  # RGBA mode (4 bytes per pixel)
                f.write(struct.pack('<I', len(pixel_data)))
                f.write(pixel_data)
            else:
                # Write raw pixel data only
                f.write(pixel_data)
        
        return True, f"Successfully converted: {png_path} -> {bin_path}"
    
    except Exception as e:
        return False, f"Error converting PNG: {str(e)}"


def read_bin_to_png(bin_path, png_path=None, has_metadata=True):
    """
    Convert a BIN file back to PNG image.
    
    Args:
        bin_path (str or Path): Path to the BIN file
        png_path (str or Path, optional): Path for the output PNG file.
                                         If None, uses BIN filename with .png extension
        has_metadata (bool): Whether the BIN file includes metadata
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        bin_path = Path(bin_path)
        
        if not bin_path.exists():
            return False, f"BIN file not found: {bin_path}"
        
        # Set default output path if not provided
        if png_path is None:
            png_path = bin_path.with_suffix('.png')
        else:
            png_path = Path(png_path)
        
        with open(bin_path, 'rb') as f:
            if has_metadata:
                # Read metadata header
                magic = f.read(4)
                if magic != b'PNG\x00':
                    return False, "Invalid BIN file format (missing PNG magic number)"
                
                width = struct.unpack('<I', f.read(4))[0]
                height = struct.unpack('<I', f.read(4))[0]
                mode_bytes = struct.unpack('B', f.read(1))[0]
                data_size = struct.unpack('<I', f.read(4))[0]
                pixel_data = f.read(data_size)
            else:
                # For raw data, we need width and height from somewhere
                # This is a limitation without metadata
                return False, "Cannot read raw BIN without metadata (width/height unknown)"
        
        # Create image from pixel data
        img = Image.frombytes('RGBA', (width, height), pixel_data)
        img.save(png_path, 'PNG')
        
        return True, f"Successfully converted: {bin_path} -> {png_path}"
    
    except Exception as e:
        return False, f"Error converting BIN to PNG: {str(e)}"


def main():
    """Command-line interface for the converter."""
    if len(sys.argv) < 2:
        print("PNG to BIN Converter")
        print("\nUsage:")
        print("  python png_to_bin.py <input.png> [output.bin]")
        print("  python png_to_bin.py --to-png <input.bin> [output.png]")
        print("\nExamples:")
        print("  python png_to_bin.py image.png")
        print("  python png_to_bin.py image.png image.bin")
        print("  python png_to_bin.py --to-png image.bin")
        sys.exit(1)
    
    if sys.argv[1] == '--to-png':
        # Convert BIN to PNG
        if len(sys.argv) < 3:
            print("Error: Input BIN file required")
            sys.exit(1)
        
        bin_file = sys.argv[2]
        png_file = sys.argv[3] if len(sys.argv) > 3 else None
        success, message = read_bin_to_png(bin_file, png_file)
    else:
        # Convert PNG to BIN
        png_file = sys.argv[1]
        bin_file = sys.argv[2] if len(sys.argv) > 2 else None
        success, message = convert_png_to_bin(png_file, bin_file)
    
    print(message)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
