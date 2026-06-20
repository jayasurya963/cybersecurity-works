# ForTool - Digital Forensics Metadata Tool.
A Python tool that extracts hidden metadata from images, PDFs, Word documents, and audio files. Perfect for digital forensics, OSINT, and security investigations.

## Features
- Extracts metadata using **ExifTool**, PIL, ExifRead, PyPDF2, python-docx, and Mutagen
- Supports: **Images** (.jpg, .png, etc.), **PDFs**, **Word Documents** (.docx), **Audio** files
- Detects GPS location data from photos
- Generates beautiful **HTML report** + **JSON export**

**Note** - Place exiftool.exe in the project folder (download from https://exiftool.org/).

**Example Use Cases** 
- Analyze photos for GPS coordinates and camera details.
- Check PDFs and Word docs for author names and revision history.
- Extract hidden information from audio recordings.
- Bulk analysis of evidence folders.

**Install**
- python -m venv venv
- Install the dependencies from the "/requirements.txt".
- Add any data that you want to analyse to the "/data" folder.
- **Output** - Stored in & as forensics_report.html , forensics_report.json.

