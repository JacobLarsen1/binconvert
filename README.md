# binconvert
PNG to BIN file converter

Convert PNG images to binary format and back with optional metadata.

## Features
- ✅ Convert PNG images to binary (.bin) files
- ✅ Convert BIN files back to PNG images
- ✅ Optional metadata header (image dimensions, mode)
- ✅ Command-line interface
- ✅ Python library for programmatic use

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

**PNG to BIN conversion:**
```bash
python png_to_bin.py image.png
# Output: image.bin
```

**PNG to BIN with custom output:**
```bash
python png_to_bin.py image.png custom_name.bin
```

**BIN back to PNG:**
```bash
python png_to_bin.py --to-png image.bin
# Output: image.png
```

**BIN to PNG with custom output:**
```bash
python png_to_bin.py --to-png image.bin custom_output.png
```

### Python Library

```python
from png_to_bin import convert_png_to_bin, read_bin_to_png

# Convert PNG to BIN
success, message = convert_png_to_bin('image.png', 'image.bin')
print(message)

# Convert BIN back to PNG
success, message = read_bin_to_png('image.bin', 'output.png')
print(message)

# Convert without metadata
success, message = convert_png_to_bin('image.png', 'image.bin', include_metadata=False)
```

## Binary Format

The converter includes a metadata header by default:

```
[MAGIC:4 bytes] [WIDTH:4 bytes] [HEIGHT:4 bytes] [MODE:1 byte] [DATA_SIZE:4 bytes] [PIXEL_DATA:variable]

MAGIC: "PNG\0" (0x504E4700)
WIDTH: Image width (little-endian 32-bit unsigned)
HEIGHT: Image height (little-endian 32-bit unsigned)
MODE: Color mode - 4 = RGBA (1 byte)
DATA_SIZE: Size of pixel data in bytes (little-endian 32-bit unsigned)
PIXEL_DATA: Raw RGBA pixel data
```

## Examples

Create a simple test image:
```python
from PIL import Image

# Create a simple 10x10 red image
img = Image.new('RGBA', (10, 10), (255, 0, 0, 255))
img.save('test.png')
```

Then convert it:
```bash
python png_to_bin.py test.png test.bin
python png_to_bin.py --to-png test.bin test_output.png
```

## Requirements
- Python 3.6+
- Pillow (PIL)
