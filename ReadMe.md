# PDF Privacy Redactor

The **PDF_Privacy_Redactor** class allows you to load a PDF document, search for sensitive text patterns, and redact (blackout) those patterns to ensure privacy. It provides functionalities to manage redaction patterns, identify sensitive content, and redact the identified text on a page or across the entire document.

## Requirements

- Python 3.x
- **PyMuPDF** (`fitz`): Install using `pip install pymupdf`

## Class Overview

### `PDF_Privacy_Redactor`

A class for redacting sensitive data within a PDF document. It supports loading a document, identifying sensitive content, adding and removing redaction patterns, and saving the modified document.

## Methods

### `__init__(self) -> None`

Initializes an empty PDF document and a pattern dictionary.

- **Attributes:**
  - `filepath`: Path to the loaded PDF file.
  - `file`: PDF file object.
  - `tokens`: Dictionary containing the redaction patterns (key-value pairs).

### `loadDocument(self, input_file: str) -> None`

Loads a PDF document from the specified `input_file`.

- **Parameters:**
  - `input_file`: Path to the PDF file to be loaded.
- **Raises:**
  - `Exception`: If the file does not exist at the given path.

### `saveDocument(self, output_file: str) -> None`

Saves the modified PDF document to a new file.

- **Parameters:**
  - `output_file`: Path to save the redacted document.

### `listPattern(self) -> dict`

Returns the current redaction patterns as a dictionary.

- **Returns:**
  - `dict`: Dictionary of patterns (key-value pairs).

### `getPattern(self, key: str) -> str`

Gets the redaction pattern associated with the given key.

- **Parameters:**
  - `key`: The key for the pattern to retrieve.
- **Returns:**
  - `str`: The pattern string associated with the key, or `None` if the key does not exist.

### `addPattern(self, token: str) -> None`

Adds a new redaction pattern to the list of tokens. If the pattern already exists, an exception is raised.

- **Parameters:**
  - `token`: The text pattern to be redacted.
- **Raises:**
  - `Exception`: If the pattern already exists in the dictionary.

### `removePattern(self, key: str) -> None`

Removes a redaction pattern identified by the given key.

- **Parameters:**
  - `key`: The key associated with the pattern to be removed.
- **Raises:**
  - `Exception`: If no such key exists.

### `identify(self) -> list`

Identifies the locations of all redaction patterns in the document.

- **Returns:**
  - `list`: A list of dictionaries where each entry corresponds to a page and its associated token matches.

### `redact_page(self, page_num: int) -> None`

Redacts the text matching the patterns on the specified page.

- **Parameters:**
  - `page_num`: The page number (starting from 0) on which the redactions should be applied.

### `redact(self) -> None`

Redacts all occurrences of the specified patterns across all pages in the PDF document.

## Example Usage

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

## Error Handling

- **File Loading:** If the provided file path does not exist, the `loadDocument()` method raises an exception.
- **Pattern Management:** When adding a pattern, if it already exists, an exception is raised. Similarly, trying to remove a pattern with a non-existing key also raises an exception.

## Notes

- The `redact()` and `redact_page()` methods apply redactions on text matching the provided patterns. These redactions cannot be undone after saving the document.
- Redactions are applied with a black fill (RGB: 0, 0, 0) to hide the sensitive text.
