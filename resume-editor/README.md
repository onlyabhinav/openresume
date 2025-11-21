# 📝 Resume Editor

A simple Flask-based web application to edit your resume JSON file with a user-friendly UI.

## Features

- ✅ **Visual Editor** - Edit all resume sections through a clean web interface
- ✅ **Auto Backup** - Every save creates a timestamped backup in `archive/` folder
- ✅ **Live Preview** - Preview your resume before saving
- ✅ **PDF Export** - Print-to-PDF directly from preview
- ✅ **Add/Remove Items** - Easily add or remove skills, experiences, achievements
- ✅ **No Database** - All data stored in a simple JSON file

## Quick Start

### 1. Install Dependencies

```bash
pip install flask
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Run the Editor

```bash
python app.py
```

### 3. Open in Browser

Go to: **http://localhost:5000**

## File Structure

```
resume-editor/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── resume-data.json    # Your resume data (created/edited by the app)
├── archive/            # Backup folder (auto-created)
│   ├── resume-data_20241121_143022.json
│   ├── resume-data_20241121_150315.json
│   └── ...
└── README.md           # This file
```

## Usage

### Editing Your Resume

1. **Profile Section** - Edit your name, title, contact info, and summary
2. **Skills Section** - Add/remove skill categories with comma-separated skills
3. **Experience Section** - Add jobs with multiple responsibilities
4. **Achievements Section** - Add achievements with multiple bullet points

### Saving

- Click the **"💾 Save"** button in the header
- A backup is automatically created before saving
- Toast notification confirms successful save

### Preview

- Click the **"👁️ Preview"** button to see your resume
- From preview, you can print to PDF (high quality, selectable text)

### Backups

- All backups are stored in the `archive/` folder
- Filename format: `resume-data_YYYYMMDD_HHMMSS.json`
- To restore a backup, simply copy it to `resume-data.json`

## Keyboard Shortcuts

- **Ctrl+S** - Not implemented (use Save button)
- **Ctrl+P** - Print to PDF (in preview window)

## Integrating with Resume HTML

After editing, your `resume-data.json` file is ready to use with:

- `resume.html` (external JSON version)
- Or copy the data to `fast-resume.html` (embedded version)

Just make sure `resume-data.json` is in the same folder as your HTML file.

## Configuration

In `app.py`, you can modify:

```python
RESUME_FILE = 'resume-data.json'  # Path to your JSON file
ARCHIVE_DIR = 'archive'           # Backup folder name
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main editor page |
| `/save` | POST | Save resume data |
| `/preview` | GET | Preview resume |
| `/backups` | GET | List backup files (JSON) |

## Troubleshooting

### Port Already in Use

If port 5000 is busy, change it in `app.py`:

```python
app.run(debug=True, port=5001)  # Use different port
```

### JSON Parsing Errors

If you manually edited `resume-data.json` and broke the format:
1. Check for missing commas or brackets
2. Use https://jsonlint.com to validate
3. Or restore from a backup in `archive/`

### Permission Errors

Make sure you have write permission in the folder:

```bash
chmod 755 resume-editor/
chmod 644 resume-editor/resume-data.json
```

## Development

To run in development mode with auto-reload:

```bash
FLASK_DEBUG=1 python app.py
```

## License

Free to use and modify.
