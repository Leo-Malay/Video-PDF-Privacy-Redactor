# PDF Privacy Redactor & Video Face Blurring

Offline tools for redacting sensitive information from PDFs and blurring faces in videos.

## Requirements

- PDF Redaction: Python 3.x + PyMuPDF (pip install pymupdf)
- Video Blurring: Python 3.x + facenet-pytorch, opencv-python, torch & CUDA dependencies

Install everything with:

```bash
pip install -r requirements.txt
```

## Quick Usage

### PDF Redaction Example

```python
# Initialize the redactor
pdf_redactor = PDF_Privacy_Redactor()

# Load a PDF document
pdf_redactor.loadDocument("input.pdf")

# Add redaction patterns
pdf_redactor.addPattern("Confidential")
pdf_redactor.addPattern("Sensitive Information")

# List patterns
print(pdf_redactor.listPattern())

# Identify all matches in the document
matches = pdf_redactor.identify()
print(matches)

# Redact all matches
pdf_redactor.redact()

# Save the redacted document
pdf_redactor.saveDocument("output_redacted.pdf")
```

### Video Face Blurring Example

```python
from face_blur_pipeline import FaceBlurPipeline

pipeline = FaceBlurPipeline(input_path='input.mp4', output_path='output_blurred.mp4')
pipeline.process_video()
```

Additionally, you may want to use it over the command line using the followng command.

```bash
python face_blur_pipeline.py --input ./input/input.mp4 --output ./output/output_blurred.mp4 --batch_size 16
```
