#!/usr/bin/env python3
"""
PNG to BIN Converter Web Application
Flask-based web interface for the converter
"""

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import io
from pathlib import Path
from png_to_bin import convert_png_to_bin, read_bin_to_png

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['ALLOWED_EXTENSIONS_PNG'] = {'png'}
app.config['ALLOWED_EXTENSIONS_BIN'] = {'bin'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_png(filename):
    """Check if file is a PNG"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_PNG']


def allowed_bin(filename):
    """Check if file is a BIN"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_BIN']


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/png-to-bin', methods=['POST'])
def png_to_bin_api():
    """API endpoint to convert PNG to BIN"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_png(file.filename):
            return jsonify({'success': False, 'error': 'File must be a PNG image'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        png_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(png_path)
        
        # Convert to BIN
        bin_filename = filename.rsplit('.', 1)[0] + '.bin'
        bin_path = os.path.join(app.config['UPLOAD_FOLDER'], bin_filename)
        
        success, message = convert_png_to_bin(png_path, bin_path)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 400
        
        # Get file size info
        png_size = os.path.getsize(png_path)
        bin_size = os.path.getsize(bin_path)
        
        return jsonify({
            'success': True,
            'message': message,
            'filename': bin_filename,
            'original_size': f'{png_size:,} bytes',
            'converted_size': f'{bin_size:,} bytes',
            'file_id': bin_filename
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500


@app.route('/api/bin-to-png', methods=['POST'])
def bin_to_png_api():
    """API endpoint to convert BIN back to PNG"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_bin(file.filename):
            return jsonify({'success': False, 'error': 'File must be a BIN file'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        bin_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(bin_path)
        
        # Convert to PNG
        png_filename = filename.rsplit('.', 1)[0] + '.png'
        png_path = os.path.join(app.config['UPLOAD_FOLDER'], png_filename)
        
        success, message = read_bin_to_png(bin_path, png_path)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 400
        
        # Get file size info
        bin_size = os.path.getsize(bin_path)
        png_size = os.path.getsize(png_path)
        
        return jsonify({
            'success': True,
            'message': message,
            'filename': png_filename,
            'original_size': f'{bin_size:,} bytes',
            'converted_size': f'{png_size:,} bytes',
            'file_id': png_filename
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download converted file"""
    try:
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/api/cleanup/<filename>', methods=['POST'])
def cleanup_file(filename):
    """Delete temporary files"""
    try:
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({'success': True}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large"""
    return jsonify({'success': False, 'error': 'File too large (max 50MB)'}), 413


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
