# AI-Powered Form Filling Assistant

An AI-powered web application designed to help users at Indian Seva Kendras fill government forms using OCR and NLP technology. The application extracts information from government documents (Aadhaar, PAN, Voter ID, etc.) and automatically fills predefined government form templates.

## Features

- **Document Upload**: Accepts government documents (Aadhaar, PAN, Voter ID, etc.)
- **OCR & NLP**: Extracts key entities using OCR and natural language processing
- **Form Mapping**: Automatically maps extracted data to government form templates
- **User Review**: Allows users to review and edit extracted information
- **Multilingual Support**: Supports English, Hindi, and Marathi languages
- **Text-to-Speech**: Accessibility feature for users who cannot read
- **Voice Input**: Voice recognition for filling forms
- **PDF Generation**: Outputs filled, downloadable PDF forms
- **Elderly-Friendly UI**: Large fonts, clear buttons, and simple interface
- **Responsive Design**: Works on various screen sizes

## Technologies Used

- **Backend**: FastAPI, Python
- **OCR**: Tesseract, EasyOCR
- **NLP**: Rule-based entity extraction
- **PDF Generation**: ReportLab
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Custom styling with animations and transitions

## Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure Tesseract OCR is installed on your system
4. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
5. Access the application at `http://127.0.0.1:8000`

## Usage

1. Upload a government document (Aadhaar, PAN, Voter ID, etc.)
2. The system will process and extract information
3. Review and edit extracted information if needed
4. Select the form type you want to fill
5. Review the pre-filled form
6. Use voice input to add additional information if needed
7. Generate and download the filled PDF form

## Project Structure

```
ai form filling assistance/
├── backend/
│   ├── main.py             # FastAPI application
│   ├── ocr_utils.py        # OCR and entity extraction
│   ├── form_mapping.py     # Form mapping engine
│   ├── pdf_generator.py    # PDF generation
│   ├── templates/          # Form templates
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── app.js              # Frontend JavaScript
│   └── style.css           # Styling
└── README.md
```

## Form Templates

The application supports three main government forms:
- Income Certificate
- Birth Certificate
- Ration Card

## Accessibility Features

- Large, clear buttons and text
- Text-to-speech for reading interface elements aloud
- Multilingual support for Hindi and Marathi
- Voice input for filling forms
- Simple, intuitive workflow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.