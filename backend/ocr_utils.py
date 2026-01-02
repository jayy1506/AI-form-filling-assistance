import pytesseract
import os
# Set the path to the local Tesseract installation
pytesseract.pytesseract_cmd = r'c:\Users\jthak\OneDrive\Attachments\Desktop\ai form filling assistance\Tesseract-OCR\tesseract.exe'

from PIL import Image
import re
from typing import Dict, Any, List
import easyocr
import spacy
from datetime import datetime

# Initialize OCR and NLP tools
reader = easyocr.Reader(['en', 'hi'])  # English and Hindi support

# Load spaCy model for NER
def load_nlp_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        print("spaCy model 'en_core_web_sm' not found. Please install it using: python -m spacy download en_core_web_sm")
        return None

nlp = load_nlp_model()

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using OCR
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text as a string
    """
    try:
        print(f"Starting OCR extraction for image: {image_path}")
        
        # Open the image
        image = Image.open(image_path)
        print(f"Image opened successfully. Mode: {image.mode}, Size: {image.size}")
        
        # Convert to RGB if necessary (for some image formats)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        text = ""
        
        # Try pytesseract for OCR
        try:
            print("Attempting pytesseract OCR...")
            # Use pytesseract with custom configuration for better accuracy
            custom_config = r'--oem 3 --psm 6 -l eng+hin'
            text = pytesseract.image_to_string(image, config=custom_config)
            print(f"Pytesseract result length: {len(text)}")
            if len(text.strip()) > 0:
                print(f"Pytesseract extracted: {text[:200]}...")  # Print first 200 chars
        except Exception as tesseract_error:
            print(f"Tesseract error: {tesseract_error}")
            # If tesseract fails, continue with easyocr
            pass
        
        # Also try easyocr for better accuracy
        try:
            print("Attempting EasyOCR...")
            easy_results = reader.readtext(image_path)
            print(f"EasyOCR found {len(easy_results)} text regions")
            easy_text = " ".join([result[1] for result in easy_results])
            print(f"EasyOCR result length: {len(easy_text)}")
            
            # Use the longer text as it might be more complete
            if len(easy_text) > len(text):
                text = easy_text
                print(f"Using EasyOCR result as it's longer")
        except Exception as easy_error:
            print(f"EasyOCR error: {easy_error}")
            # If easyocr fails, fall back to pytesseract result (even if empty)
            pass
        
        # Additional processing to clean up the text
        text = clean_extracted_text(text)
        print(f"Final cleaned text length: {len(text)}")
        
        return text.strip()
    
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def extract_entities_from_text(text: str, document_type: str = None) -> Dict[str, Any]:
    """
    Extract structured entities from text using rule-based and NLP approaches
    
    Args:
        text: Raw text to extract entities from
        document_type: Type of document (aadhaar, pan, voter) to help with extraction
        
    Returns:
        Dictionary with extracted entities and confidence scores
    """
    entities = {}
    
    # Clean the text
    clean_text = text.lower()
    
    # Use NER if spaCy model is available
    if nlp:
        doc = nlp(text)
        
        # Extract named entities using spaCy NER
        for ent in doc.ents:
            if ent.label_ == "PERSON" and "name" not in entities:
                entities["name"] = {"value": ent.text, "confidence": 0.8}
            elif ent.label_ == "DATE" and "dob" not in entities:
                # Check if this date looks like a birth date
                if any(keyword in clean_text for keyword in ["birth", "dob", "date of birth"]):
                    entities["dob"] = {"value": ent.text, "confidence": 0.8}
            elif ent.label_ in ["GPE", "LOC"] and "address" not in entities:
                entities["address"] = {"value": ent.text, "confidence": 0.7}
    
    # Extract Name using rule-based approach (always try to extract)
    name = extract_name(clean_text)
    if name and "name" not in entities:
        entities["name"] = {"value": name, "confidence": calculate_confidence(name, clean_text)}
    elif "name" not in entities:
        # Add empty name entry if not found
        entities["name"] = {"value": "", "confidence": 0.0}
    
    # Extract Date of Birth (always try to extract)
    dob = extract_date_of_birth(clean_text)
    if dob and "dob" not in entities:
        entities["dob"] = {"value": dob, "confidence": calculate_confidence(dob, clean_text)}
        # Calculate age from date of birth
        age = calculate_age_from_dob(dob)
        if age:
            entities["age"] = {"value": age, "confidence": calculate_confidence(str(age), clean_text)}
    elif "dob" not in entities:
        # Add empty dob entry if not found
        entities["dob"] = {"value": "", "confidence": 0.0}
    
    # Extract Gender (always try to extract)
    gender = extract_gender(clean_text)
    if gender:
        entities["gender"] = {"value": gender, "confidence": calculate_confidence(gender, clean_text)}
    elif "gender" not in entities:
        # Add empty gender entry if not found
        entities["gender"] = {"value": "", "confidence": 0.0}
    
    # Extract Address (always try to extract)
    address = extract_address(clean_text)
    if address and "address" not in entities:
        entities["address"] = {"value": address, "confidence": calculate_confidence(address, clean_text)}
    elif "address" not in entities:
        # Add empty address entry if not found
        entities["address"] = {"value": "", "confidence": 0.0}
    
    # Extract Aadhaar Number (always try to extract)
    aadhaar = extract_aadhaar_number(clean_text)
    if aadhaar:
        entities["aadhaar"] = {"value": aadhaar, "confidence": calculate_confidence(aadhaar, clean_text)}
    elif "aadhaar" not in entities:
        # Add empty aadhaar entry if not found
        entities["aadhaar"] = {"value": "", "confidence": 0.0}
    
    # Extract PAN Number (context-aware extraction)
    pan = extract_pan_number(clean_text)
    if pan:
        # Adjust confidence based on document type
        base_confidence = calculate_confidence(pan, clean_text)
        if document_type == "pan":
            # Higher confidence if we're processing a PAN card
            entities["pan"] = {"value": pan, "confidence": min(0.95, base_confidence + 0.15)}
        elif document_type == "aadhaar" or document_type == "voter":
            # Lower confidence if we're processing other document types
            entities["pan"] = {"value": pan, "confidence": max(0.3, base_confidence - 0.2)}
        else:
            # Default confidence
            entities["pan"] = {"value": pan, "confidence": base_confidence}
    elif "pan" not in entities:
        # Add empty pan entry if not found
        entities["pan"] = {"value": "", "confidence": 0.0}
    
    # Extract Voter ID
    voter_id = extract_voter_id(clean_text)
    if voter_id:
        entities["voter_id"] = {"value": voter_id, "confidence": calculate_confidence(voter_id, clean_text)}
    
    # Extract Parent/Guardian Name
    parent_name = extract_parent_name(clean_text)
    if parent_name:
        entities["parent_name"] = {"value": parent_name, "confidence": calculate_confidence(parent_name, clean_text)}
    
    return entities

def extract_name(text: str) -> str:
    """Extract name using pattern matching and NLP"""
    # Look for common name indicators in Indian documents
    patterns = [
        r'name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'nama[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'full\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'father[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'mother[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'spouse[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'husband[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'wife[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'candidate[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'applicant[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'surname[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'given\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'first\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'last\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'holder\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'cardholder\s+name[:\s]+([A-Z][a-zA-Z\s.\-]+)',
        r'holder[:\s]+([A-Z][a-zA-Z\s.\-]+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Return the first match that looks like a name (not too long, has spaces)
            for match in matches:
                # Clean the match by removing extra punctuation at the end
                clean_match = match.strip().rstrip(':.,;').strip()
                if 3 <= len(clean_match) <= 100 and len(clean_match.split()) >= 1:
                    return clean_match
    
    # If pattern matching fails, try looking for sequences of words with capital letters
    # that might represent names
    # Look for capitalized words that could be names
    potential_names = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z.\-]*)+)\b', text)
    if potential_names:
        # Return the most likely name (longest or most structured)
        return max(potential_names, key=len).strip()
    
    # If pattern matching fails, try NLP approach
    if nlp:
        doc = nlp(text)
        # Look for person entities
        person_entities = []
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text) > 2:
                person_entities.append(ent.text)
        
        # Return the most likely person entity (longest one)
        if person_entities:
            return max(person_entities, key=len)
    
    return ""

def extract_date_of_birth(text: str) -> str:
    """Extract date of birth using regex patterns"""
    # Common date patterns in Indian documents
    patterns = [
        r'date of birth[:\s]+(\d{2}[-/]\d{2}[-/]\d{4})',
        r'dob[:\s]+(\d{2}[-/]\d{2}[-/]\d{4})',
        r'birth[:\s]+date[:\s]+(\d{2}[-/]\d{2}[-/]\d{4})',
        r'date[:\s]+of[:\s]+birth[:\s]+(\d{2}[-/]\d{2}[-/]\d{4})',
        r'birth[:\s]+(\d{2}[-/]\d{2}[-/]\d{4})',
        r'(\d{2}[-/]\d{2}[-/]\d{4})',  # General date pattern
        r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})',  # Less strict date pattern
        r'(\d{2}-\d{2}-\d{2})',  # DD-MM-YY format
        r'(\d{4}[-/]\d{2}[-/]\d{2})',  # YYYY-MM-DD format
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Validate if it's a reasonable date of birth
            for match in matches:
                try:
                    # Handle different date formats
                    date_str = match.replace('/', '-').replace(' ', '').strip()
                    if len(date_str.split('-')[-1]) == 2:  # YY format
                        date_obj = datetime.strptime(date_str, '%d-%m-%y')
                    else:  # YYYY or DD-MM-YYYY format
                        if len(date_str) == 10 and date_str[2] == '-':
                            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                        elif len(date_str) == 10 and date_str[4] == '-':
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        else:
                            continue
                    
                    # Check if the date is reasonable (not in the future, not too old)
                    current_year = datetime.now().year
                    if 1900 <= date_obj.year <= current_year:
                        return match
                except ValueError:
                    continue
    
    return ""

def extract_gender(text: str) -> str:
    """Extract gender"""
    # More comprehensive gender patterns for Indian documents
    gender_patterns = {
        'male': [
            r'\bmale\b',
            r'\bm\.?\b',  # 'M' or 'M.' for male
            r'\bgentleman\b',
            r'\bman\b',
            r'\bboy\b',
            r'\bhusband\b',
            r'\bson\b',
            r'\bhe\b',
            r'\bmasculine\b',
            r'\bmales\b'
        ],
        'female': [
            r'\bfemale\b',
            r'\bf\.?\b',  # 'F' or 'F.' for female
            r'\bwomen\b',
            r'\bgirl\b',
            r'\bwife\b',
            r'\bdaughter\b',
            r'\bshe\b',
            r'\bfemales\b',
            r'\bwoman\b',
            r'\bfem\b'
        ],
        'other': [
            r'\bother\b',
            r'\btransgender\b',
            r'\btrans\b'
        ]
    }
    
    # Check for gender indicators in order of priority
    text_lower = text.lower()
    
    # Look for explicit gender labels first
    for gender, patterns in gender_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                # Additional validation: make sure it's not part of a larger word or context
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    # Check if the match is a complete word and not part of another word
                    start, end = match.span()
                    # Check if it's surrounded by word boundaries or common delimiters
                    before_char = text_lower[start-1] if start > 0 else ' '
                    after_char = text_lower[end] if end < len(text_lower) else ' '
                    
                    if (before_char in ' \t\n:,-' or before_char.isalpha() == False) and \
                       (after_char in ' \t\n:,-' or after_char.isalpha() == False):
                        return gender.capitalize()
    
    return ""

def extract_address(text: str) -> str:
    """Extract address"""
    # Look for address indicators
    address_indicators = [
        r'address[:\s]+([A-Za-z0-9\s,.\-]+?)(?:\n|$)',
        r'permanent address[:\s]+([A-Za-z0-9\s,.-]+?)(?:\n|$)',
        r'current address[:\s]+([A-Za-z0-9\s,.-]+?)(?:\n|$)',
        r'residential address[:\s]+([A-Za-z0-9\s,.-]+?)(?:\n|$)',
        r'addr[:\s]+([A-Za-z0-9\s,.-]+?)(?:\n|$)',
        r'location[:\s]+([A-Za-z0-9\s,.-]+?)(?:\n|$)',
        r'place[:\s]+([A-Za-z0-9\s,.-]+?)(?:\n|$)',
    ]
    
    for pattern in address_indicators:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        if matches:
            # Return the longest address match
            return max(matches, key=len).strip()
    
    # Look for postal code patterns followed by addresses
    postal_patterns = [
        r'(\d{6})[\s\n]+([A-Za-z\s,.-]+?)',  # 6-digit postal code followed by location
        r'([A-Za-z\s,.-]+?)[\s\n]+(\d{6})',  # Location followed by 6-digit postal code
    ]
    
    for pattern in postal_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    # Combine both parts if it's a tuple
                    combined = " ".join(match).strip()
                    if len(combined) > 10:  # Only return if it's a substantial address
                        return combined
                else:
                    if len(match) > 10:
                        return match
    
    # If specific patterns don't work, look for Indian city/state patterns
    indian_cities_states = r'(?:mumbai|delhi|bangalore|kolkata|chennai|hyderabad|pune|ahmedabad|jaipur|lucknow|patna|bhopal|chandigarh|nagpur|indore|thane|bhubaneswar|vadodara|nashik|agra|kanpur|noida|gurgaon|faridabad|meerut|varanasi|allahabad|amritsar|srinagar|jodhpur|raipur|vizag|coimbatore|mysore|ludhiana|aurangabad|gwalior|jalandhar|madurai|thane|mira bhayandar|kalyan|dombivli|bareilly|jammu|gulbarga|dhanbad|hubli|rohtak|kollam|thiruvananthapuram|kochi|kozhikode|tiruchirappalli|salem|warangal|guntur|vijayawada|rajahmundry|tiruppur|davanagere|bikaner|kakinada|nellore|bijapur|kota|tumkur|kharagpur|bhatpara|kulti|kamarhati|durgapur|siliguri|berhampur|rourkela|baharampur|mathura|amravati|nanded|nandyal|khammam|mahbubnagar|raichur|adoni|tadepalligudem|tirunelveli|danapur|bally|ahmednagar|cuddalore|tiruvannamalai|chittoor|karnal|bhagalpur|tirupati|saharanpur|eluru|bhavnagar|maharashtra|tamil nadu|karnataka|kerala|telangana|andhra pradesh|uttar pradesh|madhya pradesh|rajasthan|west bengal|bihar|gujarat|jharkhand|odisha|assam|haryana|punjab|himachal pradesh|uttarakhand|chhattisgarh|jammu and kashmir|ladakh|andaman and nicobar|dadra and nagar haveli|daman and diu|lakshadweep|puducherry)'
    
    # Look for text blocks that contain Indian locations
    paragraphs = text.split('\n')
    for para in paragraphs:
        if re.search(indian_cities_states, para, re.IGNORECASE):
            return para.strip()
    
    # Look for blocks that might be addresses (contain numbers and Indian location indicators)
    potential_addresses = re.findall(r'([A-Za-z0-9\s,.#\-\n]{20,})', text)
    for addr in potential_addresses:
        if re.search(indian_cities_states, addr, re.IGNORECASE) or len(re.findall(r'\d+', addr)) > 0:
            return addr.strip()
    
    return ""

def extract_aadhaar_number(text: str) -> str:
    """Extract Aadhaar number"""
    # Aadhaar patterns: 12 digits with or without spaces/dashes
    patterns = [
        r'(\d{4}[\s-]?\d{4}[\s-]?\d{4})',  # 12-digit pattern
        r'(\d{12})',  # 12 consecutive digits
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            for match in matches:
                # Validate Aadhaar format (basic validation)
                clean_match = re.sub(r'[\s-]', '', match)
                if len(clean_match) == 12 and clean_match.isdigit():
                    # Format with spaces for readability
                    formatted = f"{clean_match[:4]} {clean_match[4:8]} {clean_match[8:]}"
                    return formatted
    
    return ""

def extract_pan_number(text: str) -> str:
    """Extract PAN number"""
    # PAN pattern: 5 letters + 4 digits + 1 letter
    pattern = r'([A-Z]{5}[0-9]{4}[A-Z])'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if matches:
        # Validate that this is actually a PAN by looking for PAN indicators in the text
        pan_indicators = ["pan", "permanent account number", "pan card", "income tax"]
        text_lower = text.lower()
        has_pan_indicator = any(indicator in text_lower for indicator in pan_indicators)
        
        # If we found a potential PAN and there are PAN indicators in the text, return it
        if has_pan_indicator:
            return matches[0].upper()
        # If no PAN indicators but we still found a pattern, check if it's in a context that suggests it's a PAN
        else:
            # Look for context around the potential PAN
            for match in matches:
                # Find the match in the text and check surrounding context
                match_upper = match.upper()
                text_upper = text.upper()
                start_idx = text_upper.find(match_upper)
                if start_idx != -1:
                    # Get context around the match
                    context_start = max(0, start_idx - 50)
                    context_end = min(len(text_upper), start_idx + len(match_upper) + 50)
                    context = text_upper[context_start:context_end]
                    
                    # Check if context contains PAN-related terms
                    pan_context_indicators = ["pan", "card", "number", "income", "tax", "govt", "government"]
                    if any(indicator.upper() in context for indicator in pan_context_indicators):
                        return match_upper
    
    return ""

def extract_voter_id(text: str) -> str:
    """Extract Voter ID"""
    # Voter ID patterns: various formats
    patterns = [
        r'([A-Z]{3}[0-9]{7})',  # Standard format: 3 letters + 7 digits
        r'(VOTER-[A-Z]{3}[0-9]{7})',  # With prefix
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0].upper()
    
    return ""

def extract_parent_name(text: str) -> str:
    """Extract parent/guardian name"""
    patterns = [
        r'father[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s]+)',
        r'mother[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s]+)',
        r'guardian[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s]+)',
        r'parent[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s]+)',
        r'husband[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s]+)',
        r'wife[\'\s]*s?\s+name[:\s]+([A-Z][a-zA-Z\s]+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Return the first match that looks like a name
            for match in matches:
                if 3 <= len(match.strip()) <= 100 and len(match.split()) >= 1:
                    return match.strip()
    
    return ""

def calculate_age_from_dob(dob_str: str) -> int:
    """
    Calculate age from date of birth string
    """
    if not dob_str:
        return None
    
    try:
        # Handle different date formats
        date_formats = [
            '%d-%m-%Y',  # DD-MM-YYYY
            '%d/%m/%Y',  # DD/MM/YYYY
            '%d-%m-%y',  # DD-MM-YY
            '%d/%m/%y',  # DD/MM/YY
            '%Y-%m-%d',  # YYYY-MM-DD
            '%Y/%m/%d',  # YYYY/MM/DD
        ]
        
        dob_str = dob_str.strip()
        
        for fmt in date_formats:
            try:
                dob = datetime.strptime(dob_str, fmt)
                today = datetime.now()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                return age
            except ValueError:
                continue
        
        return None
    except Exception:
        return None

def clean_extracted_text(text: str) -> str:
    """
    Clean and improve the extracted text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    import re
    text = re.sub(r'\\s+', ' ', text)
    text = text.strip()
    
    # Fix common OCR errors
    replacements = {
        r'\\b\\dO\\b': 'DO',    # Fix 'DO' that might be read as 'dO'
        r'\\b\\dOB\\b': 'DOB',  # Fix 'DOB' that might be read as 'dOB'
        r'\\b\\date\\bof\\bbirth\\b': 'date of birth',  # Fix spacing issues
        r'\\b\\fathcr\\b': 'father',  # Common OCR error
        r'\\b\\mothcr\\b': 'mother',  # Common OCR error
        r'\\b\\sposc\\b': 'spouse',  # Common OCR error
    }
    
    for pattern, replacement in replacements.items():
        try:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        except re.error as e:
            print(f"Regex error in clean_extracted_text: {e}")
            continue  # Skip this replacement if there's an error
    
    return text

def calculate_confidence(entity_value: str, text: str) -> float:
    """
    Calculate a basic confidence score based on entity characteristics
    """
    if not entity_value:
        return 0.0
    
    # Base confidence
    confidence = 0.7
    
    # Increase confidence based on entity validation
    if entity_value in text:
        confidence += 0.2
    
    # For dates, validate format
    if re.match(r'\d{2}[-/]\d{2}[-/]\d{4}', entity_value):
        confidence = min(0.95, confidence + 0.15)
    
    # For Aadhaar numbers
    if re.match(r'\d{4}\s\d{4}\s\d{4}', entity_value):
        confidence = min(0.95, confidence + 0.2)
    
    # For PAN numbers
    if re.match(r'[A-Z]{5}[0-9]{4}[A-Z]', entity_value):
        confidence = min(0.95, confidence + 0.2)
    
    # Ensure confidence is within bounds
    return min(0.99, max(0.1, confidence))

# Additional helper functions for Indian language processing
def detect_language(text: str) -> str:
    """
    Detect language in text (basic implementation)
    """
    # Simple heuristic based on common Hindi/Indian language characters
    hindi_chars = set('ँंःऄअआइईउऊऋऌएऐऑऒओऔकखगघङचछजझञटठडढणतथदधनऩपफबभमयरऱलळऴवशषसह़ािीुूृॄेैॉॊोौ्ॐ॒।॥')
    
    text_chars = set(text)
    common_hindi = hindi_chars.intersection(text_chars)
    
    if len(common_hindi) > 0:
        return 'hi'
    else:
        return 'en'

def translate_text(text: str, target_lang: str = 'en') -> str:
    """
    Translate text (mock implementation - would use actual translation service in production)
    """
    # In a real implementation, this would call a translation API
    # For now, return the original text
    return text