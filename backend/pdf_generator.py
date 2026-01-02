from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os
from typing import Dict, Any

def generate_pdf_form(form_data: Dict[str, Any], form_type: str, output_path: str) -> str:
    """
    Generate a PDF form with the filled data
    
    Args:
        form_data: Dictionary containing form field data
        form_type: Type of form (income_certificate, birth_certificate, ration_card)
        output_path: Path where the PDF should be saved
        
    Returns:
        Path to the generated PDF
    """
    # Register fonts for Indian languages (optional)
    try:
        # Try to register common fonts
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        pdfmetrics.registerFont(TTFont('ArialBold', 'arialbd.ttf'))
    except:
        # If custom fonts are not available, use default fonts
        pass
    
    # Create the PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkred
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    # Add title based on form type
    if form_type == "income_certificate":
        title = "Income Certificate Application"
        dept = "Revenue Department"
    elif form_type == "birth_certificate":
        title = "Birth Certificate Application"
        dept = "Municipal Corporation / Revenue Department"
    elif form_type == "ration_card":
        title = "Ration Card Application"
        dept = "Food and Civil Supplies Department"
    else:
        title = "Government Form Application"
        dept = "Government Department"
    
    # Title
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Department: {dept}", normal_style))
    elements.append(Spacer(1, 12))
    
    # Add form data as a table
    form_table_data = []
    
    for field_name, field_value in form_data.items():
        if field_value:  # Only include fields that have values
            label = format_field_label(field_name)
            value = str(field_value) if field_value is not None else ""
            
            # Format long text values
            if len(value) > 100:
                # Split long text into multiple lines for better readability
                lines = [value[i:i+60] for i in range(0, len(value), 60)]
                value = "<br/>".join(lines)
            
            form_table_data.append([
                Paragraph(f"<b>{label}:</b>", normal_style),
                Paragraph(value, normal_style)
            ])
    
    # Create table with form data
    if form_table_data:
        form_table = Table(form_table_data, colWidths=[2*inch, 4*inch])
        form_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(form_table)
        elements.append(Spacer(1, 20))
    
    # Add instructions if available
    instructions = get_form_instructions(form_type)
    if instructions:
        elements.append(Paragraph("Instructions:", heading_style))
        for instruction in instructions:
            elements.append(Paragraph(f"• {instruction}", normal_style))
        elements.append(Spacer(1, 12))
    
    # Add required documents if available
    required_docs = get_required_documents(form_type)
    if required_docs:
        elements.append(Paragraph("Required Documents:", heading_style))
        for doc in required_docs:
            elements.append(Paragraph(f"• {doc}", normal_style))
        elements.append(Spacer(1, 20))
    
    # Add signature area
    signature_data = [
        ["Applicant's Signature", "Date", "Place"],
        ["", "", ""]
    ]
    
    signature_table = Table(signature_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    signature_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    
    elements.append(signature_table)
    
    # Build the PDF
    doc.build(elements)
    
    return output_path

def format_field_label(field_name: str) -> str:
    """
    Format field name for display in PDF
    """
    label_map = {
        'applicant_name': 'Applicant Name',
        'father_or_husband_name': "Father's / Husband's Name",
        'date_of_birth': 'Date of Birth',
        'gender': 'Gender',
        'permanent_address': 'Permanent Address',
        'address': 'Address',
        'aadhaar_number': 'Aadhaar Number',
        'financial_year': 'Financial Year',
        'annual_income': 'Annual Income',
        'occupation': 'Occupation',
        'signature': "Applicant's Signature",
        'date': 'Date',
        'place': 'Place',
        'person_name': 'Person Name',
        'place_of_birth': 'Place of Birth',
        'father_name': "Father's Name",
        'mother_name': "Mother's Name",
        'present_address': 'Present Address',
        'ration_card_number': 'Ration Card Number',
        'applicant_relation': 'Applicant Relationship',
        'application_date': 'Application Date',
        'purpose': 'Purpose',
        'head_of_family': 'Head of Family',
        'card_type': 'Card Type',
        'family_members': 'Family Members Details',
        'total_family_members': 'Total Family Members',
        'mobile_number': 'Mobile Number',
        'email': 'Email Address',
        'religion': 'Religion',
        'category': 'Category'
    }
    
    return label_map.get(field_name, field_name.replace('_', ' ').title())

def get_form_instructions(form_type: str) -> list:
    """
    Get form-specific instructions
    """
    instructions_map = {
        "income_certificate": [
            "All fields marked with * are mandatory",
            "Provide authentic information as per your documents",
            "Attach required documents as mentioned in the checklist",
            "Submit with proper signature and date"
        ],
        "birth_certificate": [
            "All fields marked with * are mandatory",
            "Provide authentic information as per birth records",
            "Attach required documents as mentioned in the checklist",
            "Submit with proper signature and date"
        ],
        "ration_card": [
            "All fields marked with * are mandatory",
            "Provide authentic information as per your documents",
            "Attach required documents as mentioned in the checklist",
            "Submit with proper signature and date"
        ]
    }
    
    return instructions_map.get(form_type, [])

def get_required_documents(form_type: str) -> list:
    """
    Get form-specific required documents
    """
    docs_map = {
        "income_certificate": [
            "Aadhaar Card (Aadhaar number)",
            "Address Proof",
            "Income Proof (if available)",
            "Passport Size Photo"
        ],
        "birth_certificate": [
            "Hospital Birth Record",
            "Parent's ID Proof (Aadhaar, Voter ID, etc.)",
            "Address Proof",
            "Early School Certificate (if available)",
            "Ration Card (if available)"
        ],
        "ration_card": [
            "Aadhaar Card (for all family members)",
            "Address Proof",
            "Income Certificate (if applicable)",
            "Caste Certificate (if applicable)",
            "Passport Size Photos (2 for new card, 1 for update)",
            "Bank Passbook (first page copy)"
        ]
    }
    
    return docs_map.get(form_type, [])

def create_downloadable_pdf(form_data: Dict[str, Any], form_type: str) -> str:
    """
    Create a PDF that can be downloaded by the user
    """
    import uuid
    filename = f"form_{form_type}_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join("temp", filename)
    
    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)
    
    return generate_pdf_form(form_data, form_type, output_path)