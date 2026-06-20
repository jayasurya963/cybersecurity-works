import os
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

from PIL import Image
import exifread
from docx import Document
import PyPDF2
from mutagen import File as MutagenFile

class DigitalForensicsTool:
    def __init__(self):
        self.results = []
        self.exiftool_path = "exiftool.exe"

    def run_exiftool(self, filepath):
        """Use ExifTool for maximum metadata extraction"""
        try:
            result = subprocess.run([self.exiftool_path, '-j', filepath], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return json.loads(result.stdout)[0]
        except:
            pass
        return {}

    def analyze_file(self, filepath):
        ext = Path(filepath).suffix.lower()
        basic_info = {
            "file": filepath,
            "filename": Path(filepath).name,
            "size_bytes": os.path.getsize(filepath),
            "type": ext,
            "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
        }

        metadata = {"basic": basic_info}

        try:
            # ExifTool (Best source)
            exif_data = self.run_exiftool(filepath)
            metadata["exiftool"] = exif_data

            # File-type specific
            if ext in ['.jpg', '.jpeg', '.png', '.tiff']:
                with open(filepath, 'rb') as f:
                    tags = exifread.process_file(f)
                    metadata["exif"] = {str(k): str(v) for k, v in tags.items()}
                
                # GPS Check
                if any("GPS" in k for k in exif_data.keys()):
                    metadata["has_gps"] = True

            elif ext == '.pdf':
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    if reader.metadata:
                        metadata["pdf"] = {k: str(v) for k, v in reader.metadata.items()}

            elif ext == '.docx':
                doc = Document(filepath)
                core = doc.core_properties
                metadata["docx"] = {
                    "author": core.author,
                    "created": str(core.created),
                    "modified": str(core.modified),
                    "last_modified_by": core.last_modified_by
                }

            elif ext in ['.mp3', '.wav', '.m4a']:
                audio = MutagenFile(filepath)
                if audio:
                    metadata["audio"] = {str(k): str(v) for k, v in audio.tags.items()} if audio.tags else {}

        except Exception as e:
            metadata["error"] = str(e)

        self.results.append(metadata)
        return metadata

    def generate_html_report(self):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Digital Forensics Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; padding: 20px; }}
                .container {{ max-width: 1300px; margin: auto; }}
                .card {{ background: #1e2937; padding: 20px; margin: 15px 0; border-radius: 12px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 10px; border-bottom: 1px solid #475569; text-align: left; }}
                th {{ background: #334155; }}
                .highlight {{ background: #78350f; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Digital Forensics Metadata Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """

        for item in self.results:
            html += f'<div class="card"><h2>{item["basic"]["filename"]} ({item["basic"]["type"]})</h2>'
            html += "<table>"
            for section, data in item.items():
                if section == "basic":
                    continue
                html += f"<tr><th colspan='2' style='background:#334155;'>{section.upper()}</th></tr>"
                if isinstance(data, dict):
                    for k, v in data.items():
                        html += f"<tr><td>{k}</td><td>{v}</td></tr>"
            html += "</table></div>"

        html += "</div></body></html>"

        with open("forensics_report.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"📊 HTML Report generated: forensics_report.html")

    def save_json(self):
        with open("forensics_report.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)
        print("💾 JSON Report saved: forensics_report.json")

# ====================== CLI ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digital Forensics Metadata Tool")
    parser.add_argument("path", nargs="?", default=".", help="Folder or file to analyze")
    parser.add_argument("-o", "--output", choices=["html", "json", "both"], default="both")
    args = parser.parse_args()

    tool = DigitalForensicsTool()
    path = Path(args.path)

    print("🔍 Starting Digital Forensics Analysis...")

    if path.is_file():
        tool.analyze_file(str(path))
    else:
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.jpg','.jpeg','.png','.pdf','.docx','.mp3','.wav','.m4a','.tiff')):
                    filepath = os.path.join(root, file)
                    print(f"Analyzing: {file}")
                    tool.analyze_file(filepath)

    tool.generate_html_report()
    if args.output in ["json", "both"]:
        tool.save_json()

    print("\n Analysis Completed!")