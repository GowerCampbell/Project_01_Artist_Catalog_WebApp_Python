# app.py
import os
import uuid
import sqlite3
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, redirect, url_for, g, Response, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
from collections import defaultdict

# --- App Configuration ---
DATABASE = 'artworks.db'
UPLOAD_FOLDER = 'uploads/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Helper Functions ---
def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Database Connection ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# --- Routes ---
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM artworks ORDER BY artist_name, artwork_title")
    artworks = cursor.fetchall()
    return render_template('index.html', artworks=artworks)

@app.route('/add', methods=['GET', 'POST'])
def add_artwork():
    if request.method == 'POST':
        new_uuid = str(uuid.uuid4())
        image_filename = None
        if 'artwork_image' in request.files:
            file = request.files['artwork_image']
            if file and allowed_file(file.filename):
                # --- REFINEMENT: Use a cleaner filename format ---
                extension = secure_filename(file.filename).rsplit('.', 1)[1].lower()
                image_filename = f"{new_uuid}.{extension}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # (The rest of this function is already excellent)
        db = get_db()
        cursor = db.cursor()
        artist_name = request.form.get('artist_name', "Unknown Artist") or "Unknown Artist"
        artwork_title = request.form.get('artwork_title', "Untitled") or "Untitled"
        # ... (rest of form handling)
        current_location = request.form.get('current_location', "")
        try:
            artwork_value = float(request.form.get('artwork_value') or 0)
        except (ValueError, TypeError):
            artwork_value = 0.0
        materials = request.form.get('materials', "")
        dimensions = request.form.get('dimensions', "")
        signature_details = request.form.get('signature_details', "")
        condition_notes = request.form.get('condition_notes', "")
        subject_content = request.form.get('subject_content', "")
        description = request.form.get('description', "")
        exhibition_history = request.form.get('exhibition_history', "")
        provenance = request.form.get('provenance', "")
        bibliography = request.form.get('bibliography', "")

        cursor.execute("""
            INSERT INTO artworks (artwork_uuid, artist_name, artwork_title, date_added, image_filename, 
            current_location, artwork_value, materials, dimensions, signature_details, condition_notes,
            subject_content, description, exhibition_history, provenance, bibliography)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_uuid, artist_name, artwork_title, datetime.now().strftime("%Y-%m-%d"), image_filename,
            current_location, artwork_value, materials, dimensions, signature_details,
            condition_notes, subject_content, description, exhibition_history, provenance, bibliography
        ))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_artwork.html')


@app.route('/artwork/<string:artwork_uuid>', methods=['GET', 'POST'])
def view_artwork(artwork_uuid):
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        # --- FIX: Use .get() for safety ---
        image_filename = request.form.get('current_image')
        if 'artwork_image' in request.files:
            file = request.files['artwork_image']
            if file and allowed_file(file.filename):
                # Delete old image if it exists
                if image_filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image_filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                # --- REFINEMENT: Use a cleaner filename format ---
                extension = secure_filename(file.filename).rsplit('.', 1)[1].lower()
                image_filename = f"{artwork_uuid}.{extension}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        # (The rest of the form handling is already excellent)
        artist_name = request.form.get('artist_name', "Unknown Artist") or "Unknown Artist"
        artwork_title = request.form.get('artwork_title', "Untitled") or "Untitled"
        # ... (rest of form handling)
        current_location = request.form.get('current_location', "")
        try:
            artwork_value = float(request.form.get('artwork_value') or 0)
        except (ValueError, TypeError):
            artwork_value = 0.0
        materials = request.form.get('materials', "")
        dimensions = request.form.get('dimensions', "")
        signature_details = request.form.get('signature_details', "")
        condition_notes = request.form.get('condition_notes', "")
        subject_content = request.form.get('subject_content', "")
        description = request.form.get('description', "")
        exhibition_history = request.form.get('exhibition_history', "")
        provenance = request.form.get('provenance', "")
        bibliography = request.form.get('bibliography', "")

        cursor.execute("""
            UPDATE artworks SET artist_name=?, artwork_title=?, image_filename=?, current_location=?, 
            artwork_value=?, materials=?, dimensions=?, signature_details=?, condition_notes=?, 
            subject_content=?, description=?, exhibition_history=?, provenance=?, bibliography=?
            WHERE artwork_uuid=?
        """, (
            artist_name, artwork_title, image_filename, current_location, artwork_value,
            materials, dimensions, signature_details, condition_notes, subject_content,
            description, exhibition_history, provenance, bibliography, artwork_uuid
        ))
        db.commit()
        # --- UX IMPROVEMENT: Redirect back to the edit page ---
        return redirect(url_for('view_artwork', artwork_uuid=artwork_uuid))

    cursor.execute("SELECT * FROM artworks WHERE artwork_uuid = ?", (artwork_uuid,))
    artwork = cursor.fetchone()
    if artwork is None:
        return "Artwork not found", 404
    return render_template('view_artwork.html', artwork=artwork)


@app.route('/uploads/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<string:artwork_uuid>', methods=['POST'])
def delete_artwork(artwork_uuid):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT image_filename FROM artworks WHERE artwork_uuid = ?", (artwork_uuid,))
    artwork = cursor.fetchone()
    if artwork and artwork['image_filename']:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], artwork['image_filename']))
        except OSError as e:
            print(f"Error deleting file: {e.strerror}")
    cursor.execute("DELETE FROM artworks WHERE artwork_uuid = ?", (artwork_uuid,))
    db.commit()
    return redirect(url_for('index'))


@app.route('/download.xml')
def download_xml():
    db = get_db()
    artworks = db.execute("SELECT * FROM artworks ORDER BY artist_name").fetchall()
    artists = defaultdict(list)
    for art in artworks:
        artists[art['artist_name']].append(dict(art))
    root = ET.Element('ArtCatalog')
    for artist_name, works in artists.items():
        artist_element = ET.SubElement(root, 'Artist', {'name': artist_name})
        for work in works:
            artwork_element = ET.SubElement(artist_element, 'Artwork')
            for key, value in work.items():
                if key not in ['id', 'artist_name']:
                    field = ET.SubElement(artwork_element, key.replace('_', ' ').title().replace(' ', ''))
                    field.text = str(value) if value is not None else ''
    xml_string = ET.tostring(root, encoding='unicode', xml_declaration=True)
    return Response(xml_string, mimetype='application/xml', headers={'Content-Disposition': 'attachment;filename=artist_catalog.xml'})


if __name__ == '__main__':
    app.run(debug=True)