from typing import Dict, Any, Tuple
import json

def map_entities_to_form(entities: Dict[str, Any], form_type: str) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Map extracted entities to form fields based on form type
    
    Args:
        entities: Dictionary containing extracted entities with confidence scores
        form_type: Type of form to map to (e.g., "income_certificate", "birth_certificate")
        
    Returns:
        Tuple of (filled_form_data, confidence_scores)
    """
    if form_type == "income_certificate":
        return map_to_income_certificate(entities)
    elif form_type == "birth_certificate":
        return map_to_birth_certificate(entities)
    elif form_type == "ration_card":
        return map_to_ration_card(entities)
    else:
        # Default mapping for unknown form types
        return map_to_generic_form(entities)

def map_to_income_certificate(entities: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Map entities to Income Certificate form fields
    """
    filled_form = {}
    confidence_scores = {}
    
    # Map name
    if "name" in entities:
        filled_form["applicant_name"] = entities["name"]["value"]
        confidence_scores["applicant_name"] = entities["name"]["confidence"]
    else:
        filled_form["applicant_name"] = ""
        confidence_scores["applicant_name"] = 0.0
    
    # Map father's/husband's name
    if "parent_name" in entities:
        filled_form["father_or_husband_name"] = entities["parent_name"]["value"]
        confidence_scores["father_or_husband_name"] = entities["parent_name"]["confidence"]
    else:
        filled_form["father_or_husband_name"] = ""
        confidence_scores["father_or_husband_name"] = 0.0
    
    # Map date of birth
    if "dob" in entities:
        filled_form["date_of_birth"] = entities["dob"]["value"]
        confidence_scores["date_of_birth"] = entities["dob"]["confidence"]
    else:
        filled_form["date_of_birth"] = ""
        confidence_scores["date_of_birth"] = 0.0
    
    # Map address
    if "address" in entities:
        filled_form["permanent_address"] = entities["address"]["value"]
        confidence_scores["permanent_address"] = entities["address"]["confidence"]
    else:
        filled_form["permanent_address"] = ""
        confidence_scores["permanent_address"] = 0.0
    
    # Map gender
    if "gender" in entities:
        filled_form["gender"] = entities["gender"]["value"]
        confidence_scores["gender"] = entities["gender"]["confidence"]
    else:
        filled_form["gender"] = ""
        confidence_scores["gender"] = 0.0
    
    # Map Aadhaar number
    if "aadhaar" in entities:
        filled_form["aadhaar_number"] = entities["aadhaar"]["value"]
        confidence_scores["aadhaar_number"] = entities["aadhaar"]["confidence"]
    else:
        filled_form["aadhaar_number"] = ""
        confidence_scores["aadhaar_number"] = 0.0
    
    # Additional fields for income certificate
    filled_form["financial_year"] = ""  # This would be entered by user
    filled_form["annual_income"] = ""   # This would be entered by user
    filled_form["occupation"] = ""      # This would be entered by user
    filled_form["signature"] = ""       # This would be added by user
    filled_form["date"] = ""           # This would be added by user
    
    # Set confidence for user-entered fields to 0
    confidence_scores["financial_year"] = 0.0
    confidence_scores["annual_income"] = 0.0
    confidence_scores["occupation"] = 0.0
    confidence_scores["signature"] = 0.0
    confidence_scores["date"] = 0.0
    
    return filled_form, confidence_scores

def map_to_birth_certificate(entities: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Map entities to Birth Certificate form fields
    """
    filled_form = {}
    confidence_scores = {}
    
    # Map name
    if "name" in entities:
        filled_form["person_name"] = entities["name"]["value"]
        confidence_scores["person_name"] = entities["name"]["confidence"]
    else:
        filled_form["person_name"] = ""
        confidence_scores["person_name"] = 0.0
    
    # Map date of birth
    if "dob" in entities:
        filled_form["date_of_birth"] = entities["dob"]["value"]
        confidence_scores["date_of_birth"] = entities["dob"]["confidence"]
    else:
        filled_form["date_of_birth"] = ""
        confidence_scores["date_of_birth"] = 0.0
    
    # Map place of birth
    if "address" in entities:
        # Extract place from address if possible
        filled_form["place_of_birth"] = extract_place_from_address(entities["address"]["value"])
        confidence_scores["place_of_birth"] = entities["address"]["confidence"] * 0.8  # Lower confidence for place extraction
    else:
        filled_form["place_of_birth"] = ""
        confidence_scores["place_of_birth"] = 0.0
    
    # Map gender
    if "gender" in entities:
        filled_form["gender"] = entities["gender"]["value"]
        confidence_scores["gender"] = entities["gender"]["confidence"]
    else:
        filled_form["gender"] = ""
        confidence_scores["gender"] = 0.0
    
    # Map parents' names
    if "parent_name" in entities:
        filled_form["father_name"] = entities["parent_name"]["value"]
        confidence_scores["father_name"] = entities["parent_name"]["confidence"]
    else:
        filled_form["father_name"] = ""
        confidence_scores["father_name"] = 0.0
    
    # Mother's name is typically not in the extracted entities, so leave blank
    filled_form["mother_name"] = ""
    confidence_scores["mother_name"] = 0.0
    
    # Additional fields for birth certificate
    filled_form["registration_number"] = ""  # Would be assigned by authority
    filled_form["date_of_registration"] = ""  # Would be assigned by authority
    filled_form["signature_of_officer"] = ""  # Would be added by authority
    
    # Set confidence for authority-entered fields to 0
    confidence_scores["registration_number"] = 0.0
    confidence_scores["date_of_registration"] = 0.0
    confidence_scores["signature_of_officer"] = 0.0
    
    return filled_form, confidence_scores

def map_to_ration_card(entities: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Map entities to Ration Card form fields
    """
    filled_form = {}
    confidence_scores = {}
    
    # Map head of family name
    if "name" in entities:
        filled_form["head_of_family"] = entities["name"]["value"]
        confidence_scores["head_of_family"] = entities["name"]["confidence"]
    else:
        filled_form["head_of_family"] = ""
        confidence_scores["head_of_family"] = 0.0
    
    # Map father's/husband name
    if "parent_name" in entities:
        filled_form["father_or_husband_name"] = entities["parent_name"]["value"]
        confidence_scores["father_or_husband_name"] = entities["parent_name"]["confidence"]
    else:
        filled_form["father_or_husband_name"] = ""
        confidence_scores["father_or_husband_name"] = 0.0
    
    # Map date of birth
    if "dob" in entities:
        filled_form["date_of_birth"] = entities["dob"]["value"]
        confidence_scores["date_of_birth"] = entities["dob"]["confidence"]
    else:
        filled_form["date_of_birth"] = ""
        confidence_scores["date_of_birth"] = 0.0
    
    # Map address
    if "address" in entities:
        filled_form["address"] = entities["address"]["value"]
        confidence_scores["address"] = entities["address"]["confidence"]
    else:
        filled_form["address"] = ""
        confidence_scores["address"] = 0.0
    
    # Map gender
    if "gender" in entities:
        filled_form["gender"] = entities["gender"]["value"]
        confidence_scores["gender"] = entities["gender"]["confidence"]
    else:
        filled_form["gender"] = ""
        confidence_scores["gender"] = 0.0
    
    # Map Aadhaar number
    if "aadhaar" in entities:
        filled_form["aadhaar_number"] = entities["aadhaar"]["value"]
        confidence_scores["aadhaar_number"] = entities["aadhaar"]["confidence"]
    else:
        filled_form["aadhaar_number"] = ""
        confidence_scores["aadhaar_number"] = 0.0
    
    # Additional fields for ration card
    filled_form["ration_card_number"] = ""  # Would be assigned by authority
    filled_form["card_type"] = ""           # Would be selected by user
    filled_form["family_members"] = []      # Would be added by user
    filled_form["signature"] = ""           # Would be added by user
    
    # Set confidence for user/authority-entered fields to 0
    confidence_scores["ration_card_number"] = 0.0
    confidence_scores["card_type"] = 0.0
    confidence_scores["family_members"] = 0.0
    confidence_scores["signature"] = 0.0
    
    return filled_form, confidence_scores

def map_to_generic_form(entities: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Map entities to a generic form as fallback
    """
    filled_form = {}
    confidence_scores = {}
    
    # Map all available entities to generic fields
    for key, value in entities.items():
        field_name = f"field_{key}"
        filled_form[field_name] = value["value"]
        confidence_scores[field_name] = value["confidence"]
    
    return filled_form, confidence_scores

def extract_place_from_address(address: str) -> str:
    """
    Extract place/city from address string
    """
    # Simple heuristic: take the last significant part of the address
    # In a real implementation, this would be more sophisticated
    parts = address.split(',')
    if parts:
        # Return the last part which is likely to be the city/place
        return parts[-1].strip()
    return address

# Form templates for different government forms
FORM_TEMPLATES = {
    "income_certificate": {
        "title": "Income Certificate",
        "fields": [
            {"name": "applicant_name", "label": "Name of Applicant", "type": "text", "required": True},
            {"name": "father_or_husband_name", "label": "Father's/Husband's Name", "type": "text", "required": True},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "text", "required": False},
            {"name": "permanent_address", "label": "Permanent Address", "type": "textarea", "required": True},
            {"name": "gender", "label": "Gender", "type": "text", "required": False},
            {"name": "aadhaar_number", "label": "Aadhaar Number", "type": "text", "required": False},
            {"name": "financial_year", "label": "Financial Year", "type": "text", "required": True},
            {"name": "annual_income", "label": "Annual Income", "type": "text", "required": True},
            {"name": "occupation", "label": "Occupation", "type": "text", "required": True},
            {"name": "signature", "label": "Signature", "type": "text", "required": True},
            {"name": "date", "label": "Date", "type": "text", "required": True}
        ]
    },
    "birth_certificate": {
        "title": "Birth Certificate",
        "fields": [
            {"name": "person_name", "label": "Name of Person", "type": "text", "required": True},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "text", "required": True},
            {"name": "place_of_birth", "label": "Place of Birth", "type": "text", "required": True},
            {"name": "gender", "label": "Gender", "type": "text", "required": True},
            {"name": "father_name", "label": "Father's Name", "type": "text", "required": False},
            {"name": "mother_name", "label": "Mother's Name", "type": "text", "required": False},
            {"name": "registration_number", "label": "Registration Number", "type": "text", "required": False},
            {"name": "date_of_registration", "label": "Date of Registration", "type": "text", "required": False},
            {"name": "signature_of_officer", "label": "Signature of Officer", "type": "text", "required": False}
        ]
    },
    "ration_card": {
        "title": "Ration Card",
        "fields": [
            {"name": "head_of_family", "label": "Head of Family", "type": "text", "required": True},
            {"name": "father_or_husband_name", "label": "Father's/Husband's Name", "type": "text", "required": False},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "text", "required": False},
            {"name": "address", "label": "Address", "type": "textarea", "required": True},
            {"name": "gender", "label": "Gender", "type": "text", "required": False},
            {"name": "aadhaar_number", "label": "Aadhaar Number", "type": "text", "required": False},
            {"name": "ration_card_number", "label": "Ration Card Number", "type": "text", "required": False},
            {"name": "card_type", "label": "Card Type (APL/BPL)", "type": "text", "required": True},
            {"name": "family_members", "label": "Family Members", "type": "textarea", "required": True},
            {"name": "signature", "label": "Signature", "type": "text", "required": True}
        ]
    }
}