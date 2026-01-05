# AI-Powered Form Filling Assistant for Indian Seva Kendras

An advanced web application that helps citizens at Indian Seva Kendras automatically fill government forms by extracting information from government documents like Aadhaar, PAN, Voter ID, etc.

## Features

### Document Processing
- OCR-based text extraction from government documents
- Entity extraction for Name, Date of Birth, Address, Aadhaar number, PAN number, Gender
- Support for Aadhaar, PAN, Voter ID and other government documents
- Context-aware extraction based on document type

### User Interface
- Full-page responsive design with large, accessible fonts
- Three-panel document type selection (Aadhaar, PAN, Voter ID)
- Signature upload functionality
- Government forms section for elderly citizens
- Multilingual support (English, Hindi, Marathi)
- Text-to-speech functionality for accessibility
- Large buttons and controls for elderly users

### Form Processing
- Automatic mapping of extracted entities to form fields
- Support for Income Certificate, Birth Certificate, and Ration Card forms
- PDF generation of filled forms
- Form validation and error handling

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **OCR**: Tesseract and EasyOCR
- **NLP**: spaCy for named entity recognition
- **PDF Generation**: ReportLab
- **Text-to-Speech**: Web Speech API

## Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Install spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. Install Tesseract OCR on your system
5. Update the Tesseract path in `backend/ocr_utils.py` if needed

## Usage

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8001
   ```
2. Access the application at `http://127.0.0.1:8001`

## Key Improvements in Upgraded Version

### Enhanced OCR and Entity Extraction
- Improved regex patterns for better extraction accuracy
- Context-aware extraction based on document type
- Better handling of character ranges in text
- Enhanced name extraction with context patterns
- Complete address extraction spanning multiple lines

### UI/UX Improvements
- Full-page responsive design
- Increased font sizes throughout the application
- Larger buttons and controls for elderly users
- Signature upload panel
- Improved accessibility features
- Better visual hierarchy and spacing

### Document Type Awareness
- Context-aware PAN number extraction
- Different confidence scoring based on document type
- Specialized extraction patterns for each document type

### Error Handling and Validation
- Proper regex escaping to prevent character range errors
- Comprehensive error handling throughout the application
- Input validation and sanitization

## API Endpoints

- `GET /` - Main application page
- `POST /upload` - Upload document
- `POST /extract` - Extract entities from document
- `POST /fill-form` - Map entities to form fields
- `POST /generate-pdf` - Generate filled PDF form
- `GET /health` - Health check

## Configuration

The application can be configured through environment variables or by modifying the source code:

- Tesseract path: Update in `backend/ocr_utils.py`
- Port: Modify in the uvicorn command
- Temporary file storage: Configured in `backend/main.py`

## File Structure

```
ai-form-filling-assistance/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── ocr_utils.py      # OCR and entity extraction
│   ├── form_mapping.py   # Form mapping engine
│   ├── pdf_generator.py  # PDF generation
│   ├── templates/        # Form templates
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html        # Main HTML page
│   ├── app.js            # Frontend JavaScript
│   └── style.css         # Styling
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.