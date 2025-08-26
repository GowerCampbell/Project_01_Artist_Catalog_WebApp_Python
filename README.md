
# Artist Catalog Web Application

A full-stack web application built with Python and Flask that allows artists, estates, or collectors to document, manage, and preserve an artistic legacy.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_Site-brightgreen?style=for-the-badge&logo=rocket)](https://project-01-artist-catalog-webapp-python.onrender.com/)]

## About The Project

This tool was originally created to help my mom catalog my grandmother's artwork in a way that could be easily shared with others. Believing that artists and collectors everywhere could benefit from a simple, organized system, I decided to make this project public. It provides a comprehensive framework for cataloging artworks, drawing on established practices from museums and galleries.

The application allows users to add, view, edit, and delete artwork entries. All data is stored in a SQLite database, and the entire catalog can be downloaded as a structured XML file, ensuring data portability.

## Built With

- Python
- Flask
- SQLite
- Bootstrap 5
- HTML & CSS

## Key Features

- **Full CRUD Functionality**: Create, Read, Update, and Delete artwork entries.
- **Comprehensive Data Model**: Includes fields for core information, administrative details, physical attributes, and contextual history.
- **Image Uploads**: Securely upload and store an image for each artwork.
- **Dynamic Search**: Filter the catalog in real-time by artist name or artwork title.
- **XML Export**: Download the entire catalog as a well-formed XML file, with artworks grouped by artist.
- **Responsive Design**: A clean, mobile-first interface built with Bootstrap 5.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

You will need to have Python 3 installed on your system.

### Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/artist-catalog-app.git
   ```

2. Navigate into the project directory:
   ```bash
   cd artist-catalog-app
   ```

3. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database (run this once):
   ```bash
   python database.py
   ```

6. Run the Flask application:
   ```bash
   flask run
   ```

7. Open your browser and go to `http://127.0.0.1:5000`
