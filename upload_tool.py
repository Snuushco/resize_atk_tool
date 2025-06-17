"""
Module met upload- en image processing functies voor Flask backend.
Bevat geen Streamlit of UI-code.
"""
import os
from PIL import Image
import io
from datetime import datetime
from logger import logger

# Zet requirements op module-niveau zodat deze overal beschikbaar is
requirements = {
    'pasfoto': {'min': (276, 355), 'max': (551, 709)},
    'handtekening': {'min': (354, 108), 'max': (945, 287)},
    'bedrijfslogo': {'min': (315, 127), 'max': (945, 382)},
}

def validate_and_resize_image(contents, image_type, filename):
    logger.debug(f"Start validatie en resizing voor {filename} (type: {image_type})")
    
    if image_type not in requirements:
        logger.error(f"Ongeldig afbeeldingstype: {image_type}")
        raise ValueError('Ongeldig afbeeldingstype.')
    
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
        image = Image.open(io.BytesIO(contents))
        logger.debug(f"Afbeelding succesvol geladen: {filename}")
    except Exception as e:
        logger.error(f"Fout bij laden afbeelding {filename}: {str(e)}")
        raise ValueError('Bestand is geen geldige afbeelding.')
    
    min_w, min_h = requirements[image_type]['min']
    max_w, max_h = requirements[image_type]['max']
    width, height = image.size
    logger.debug(f"Originele afmetingen: {width}x{height}")
    
    # Schaal naar min als kleiner, maar niet groter dan max
    new_w, new_h = width, height
    if width < min_w or height < min_h:
        scale = max(min_w/width, min_h/height)
        new_w, new_h = int(width*scale), int(height*scale)
        logger.debug(f"Upscaling nodig: {new_w}x{new_h}")
    
    if new_w > max_w or new_h > max_h:
        scale = min(max_w/new_w, max_h/new_h)
        new_w, new_h = int(new_w*scale), int(new_h*scale)
        logger.debug(f"Downscaling nodig: {new_w}x{new_h}")
    
    if (new_w, new_h) != (width, height):
        image = image.resize((new_w, new_h), Image.LANCZOS)
        logger.info(f"Afbeelding geresized van {width}x{height} naar {new_w}x{new_h}")
    
    return image

def process_upload(file, image_type):
    """
    Valideer en resize een uploadbestand. Return dict met 'success', 'image' (PIL), 'error' (str), 'orig_size' (tuple), 'resized_size' (tuple), 'min_size', 'max_size'.
    """
    logger.info(f"Start verwerking upload: {file.name} (type: {image_type})")
    
    try:
        contents = file.read()
        if len(contents) == 0:
            logger.error(f"Leeg bestand: {file.name}")
            return {'success': False, 'error': 'Bestand is leeg.'}
        
        # Originele afmetingen uitlezen
        orig_image = Image.open(io.BytesIO(contents))
        orig_size = orig_image.size
        logger.debug(f"Originele afmetingen: {orig_size}")
        
        image = validate_and_resize_image(contents, image_type, file.name)
        resized_size = image.size
        min_size = requirements[image_type]['min']
        max_size = requirements[image_type]['max']
        
        logger.info(f"Upload succesvol verwerkt: {file.name}")
        return {
            'success': True,
            'image': image,
            'error': None,
            'filename': file.name,
            'orig_size': orig_size,
            'resized_size': resized_size,
            'min_size': min_size,
            'max_size': max_size
        }
    except Exception as e:
        logger.error(f"Fout bij verwerken {file.name}: {str(e)}")
        return {'success': False, 'error': str(e)} 