// Global variables
let currentDocumentId = null;
let currentDocumentType = null;
let extractedEntities = {};
let currentFormType = null;
let filledFormData = {};

// DOM Elements
const uploadSection = document.getElementById('upload-section');
const processingSection = document.getElementById('processing-section');
const reviewSection = document.getElementById('review-section');
const formSection = document.getElementById('form-section');
const fillSection = document.getElementById('fill-section');

const uploadBtn = document.getElementById('upload-btn');
const extractBtn = document.getElementById('extract-btn');
const editEntitiesBtn = document.getElementById('edit-entities-btn');
const continueBtn = document.getElementById('continue-btn');
const generatePdfBtn = document.getElementById('generate-pdf-btn');
const voiceInputBtn = document.getElementById('voice-input-btn');

const documentUpload = document.getElementById('document-upload');
const uploadStatus = document.getElementById('upload-status');
const extractionStatus = document.getElementById('extraction-status');
const entitiesDisplay = document.getElementById('entities-display');
const formSelection = document.getElementById('form-selection');
const formFields = document.getElementById('form-fields');
const formTitle = document.getElementById('form-title');

// Multilingual and TTS elements
const languageSelect = document.getElementById('language-select');
const ttsBtn = document.getElementById('tts-btn');

// Voice modal elements - REMOVED
// const voiceModal = document.getElementById('voice-modal');
// const closeVoiceModal = document.getElementById('close-voice-modal');
// const startVoiceBtn = document.getElementById('start-voice-btn');
// const voiceStatus = document.getElementById('voice-status');
    
// Dummy variables to avoid errors
const voiceModal = null;
const closeVoiceModal = null;
const startVoiceBtn = null;
const voiceStatus = null;

// Text-to-speech functionality
let isSpeaking = false;
let speechUtterance = null;

// Translation dictionary
const translations = {
    'en': {
        'upload_document': 'Upload Document',
        'processing_document': 'Processing Document',
        'extract_information': 'Extract Information',
        'review_extracted_information': 'Review Extracted Information',
        'edit_information': 'Edit Information',
        'continue_to_form': 'Continue to Form',
        'select_form_type': 'Select Form Type',
        'income_certificate': 'Income Certificate',
        'birth_certificate': 'Birth Certificate',
        'ration_card': 'Ration Card',
        'voice_input': 'Voice Input',
        'generate_pdf': 'Generate PDF',
        'start_speaking': 'Start Speaking',
        'form_title': 'Form Title',
        'upload_aadhaar_pan': 'Upload Aadhaar, PAN, Voter ID, or other government documents',
        'apply_income': 'Apply for income certificate for various purposes',
        'apply_birth': 'Apply for birth certificate or duplicate',
        'apply_ration': 'Apply for ration card or update details',
        'pdf_generated': 'PDF generated and download started successfully!',
        'voice_input_processed': 'Voice input functionality would update the form fields in a real implementation.',
        'speech_processed': 'Speech processed successfully!',
        'listening_now': 'Listening... Please speak now.',
        'processing_speech': 'Processing your speech...',
        'speech_recognition_not_supported': 'Speech recognition not supported in this browser.',
        'recognized': 'Recognized',
        'error_starting_recognition': 'Error starting recognition',
        'error': 'Error',
        'success': 'Success',
        'info': 'Info',
        'read_aloud': 'Read Aloud',
        'read_text': 'Read Text',
        // Status messages
        'no_document_selected': 'Please select a document to upload',
        'uploading_document': 'Uploading document...',
        'document_uploaded_successfully': 'Document uploaded successfully.',
        'upload_failed': 'Upload failed',
        // Extraction messages
        'extracting_information': 'Extracting information...',
        'information_extracted_successfully': 'Information extracted successfully',
        'extraction_failed': 'Extraction failed',
        'extraction_error': 'Extraction error',
        'upload_error': 'Upload error',
        'no_document_uploaded': 'No document uploaded',
        'document_id_or_form_type_not_set': 'Document ID or form type not set',
        'no_entities_extracted': 'No entities extracted',
        'no_content_available_to_read': 'No content available to read.',
        // Form field labels
        'applicant_name': 'Applicant Name',
        'father_or_husband_name': "Father's / Husband's Name",
        'date_of_birth': 'Date of Birth',
        'permanent_address': 'Permanent Address',
        'annual_income': 'Annual Income',
        'person_name': 'Person Name',
        'place_of_birth': 'Place of Birth',
        'head_of_family': 'Head of Family',
        // Entity labels
        'name': 'Full Name',
        'gender': 'Gender',
        'address': 'Address',
        'aadhaar': 'Aadhaar Number',
        'pan': 'PAN Number',
        'voter_id': 'Voter ID',
        'parent_name': 'Parent/Guardian Name',
        'select_document_type': 'Select Document Type',
        'aadhaar_card': 'Aadhaar Card',
        'pan_card': 'PAN Card',
        'voter_id': 'Voter ID',
        'upload_aadhaar': 'Upload your Aadhaar card for identity verification',
        'upload_pan': 'Upload your PAN card for tax identification',
        'upload_voter': 'Upload your Voter ID for electoral identification',
        'gov_forms_title': 'Important Government Forms',
        'gov_forms_desc': 'Quick access to important forms for elderly citizens',
        'pension_application': 'Pension Application',
        'pension_desc': 'Apply for various pension schemes',
        'healthcare_forms': 'Healthcare Forms',
        'healthcare_desc': 'Medical and health insurance forms',
        'ration_card': 'Ration Card',
        'ration_desc': 'Apply or update your ration card details',
        'voter_id': 'Voter ID',
        'voter_desc': 'Apply for voter ID or update details',
        'aadhaar_services': 'Aadhaar Services',
        'aadhaar_desc': 'Update or verify your Aadhaar details',
        'banking_forms': 'Banking Forms',
        'banking_desc': 'Senior citizen banking services',
        'back_to_form': 'Back to Form'
    },
    'hi': {
        'upload_document': 'दस्तावेज़ अपलोड करें',
        'processing_document': 'दस्तावेज़ प्रसंस्करण',
        'extract_information': 'जानकारी निकालें',
        'review_extracted_information': 'निकाली गई जानकारी की समीक्षा करें',
        'edit_information': 'जानकारी संपादित करें',
        'continue_to_form': 'फॉर्म पर जारी रखें',
        'select_form_type': 'फॉर्म प्रकार चुनें',
        'income_certificate': 'आय प्रमाण पत्र',
        'birth_certificate': 'जन्म प्रमाण पत्र',
        'ration_card': 'राशन कार्ड',
        'voice_input': 'ध्वनि आदान',
        'generate_pdf': 'पीडीएफ उत्पन्न करें',
        'start_speaking': 'बोलना शुरू करें',
        'form_title': 'फॉर्म शीर्षक',
        'upload_aadhaar_pan': 'आधार, पैन, मतदाता पहचान पत्र या अन्य सरकारी दस्तावेज़ अपलोड करें',
        'apply_income': 'विभिन्न उद्देश्यों के लिए आय प्रमाण पत्र के लिए आवेदन करें',
        'apply_birth': 'जन्म प्रमाण पत्र या डुप्लिकेट के लिए आवेदन करें',
        'apply_ration': 'राशन कार्ड के लिए आवेदन करें या विवरण अपडेट करें',
        'pdf_generated': 'पीडीएफ सफलतापूर्वक उत्पन्न हुआ और डाउनलोड शुरू हो गया!',
        'voice_input_processed': 'ध्वनि आदान कार्यक्षमता वास्तविक कार्यान्वयन में फॉर्म फ़ील्ड को अपडेट करेगी।',
        'speech_processed': 'भाषण सफलतापूर्वक संसोंस्कृत!',
        'listening_now': 'सुन रहे हैं... कृपया बोलें।',
        'processing_speech': 'आपके भाषण की प्रक्रिया की जा रही है...',
        'speech_recognition_not_supported': 'इस ब्राउज़र में भाषण पहचान समर्थित नहीं है।',
        'recognized': 'पहचाना गया',
        'error_starting_recognition': 'पहचान शुरू करने में त्रुटि',
        'error': 'त्रुटि',
        'success': 'सफलता',
        'info': 'जानकारी',
        'read_aloud': 'ज़ोर से पढ़ें',
        'read_text': 'पाठ पढ़ें',
        // Status messages
        'no_document_selected': 'कृपया अपलोड करने के लिए कोई दस्तावेज़ चुनें',
        'uploading_document': 'दस्तावेज़ अपलोड किया जा रहा है...',
        'document_uploaded_successfully': 'दस्तावेज़ सफलतापूर्वक अपलोड किया गया।',
        'upload_failed': 'अपलोड विफल रहा',
        // Extraction messages
        'extracting_information': 'जानकारी निकाली जा रही है...',
        'information_extracted_successfully': 'जानकारी सफलतापूर्वक निकाली गई',
        'extraction_failed': 'निष्कर्षण विफल रहा',
        'extraction_error': 'निष्कर्षण त्रुटि',
        'upload_error': 'अपलोड त्रुटि',
        'no_document_uploaded': 'कोई दस्तावेज़ अपलोड नहीं किया गया',
        'document_id_or_form_type_not_set': 'दस्तावेज़ आईडी या फॉर्म प्रकार सेट नहीं है',
        'no_entities_extracted': 'कोई एंटिटी निकाली नहीं गई',
        'no_content_available_to_read': 'पढ़ने के लिए कोई सामग्री उपलब्ध नहीं है।',
        // Form field labels
        'applicant_name': 'आवेदक का नाम',
        'father_or_husband_name': 'पिता / पति का नाम',
        'date_of_birth': 'जन्म तिथि',
        'permanent_address': 'स्थायी पता',
        'annual_income': 'वार्षिक आय',
        'person_name': 'व्यक्ति का नाम',
        'place_of_birth': 'जन्म स्थान',
        'head_of_family': 'परिवार का मुखिया',
        // Entity labels
        'name': 'पूरा नाम',
        'gender': 'लिंग',
        'address': 'पता',
        'aadhaar': 'आधार क्रमांक',
        'pan': 'पैन क्रमांक',
        'voter_id': 'मतदाता पहचान पत्र',
        'parent_name': 'माता-पिता / अभिभावक का नाम',
        'select_document_type': 'दस्तावेज़ प्रकार चुनें',
        'aadhaar_card': 'आधार कार्ड',
        'pan_card': 'पैन कार्ड',
        'voter_id': 'मतदाता पहचान पत्र',
        'upload_aadhaar': 'पहचान सत्यापन के लिए अपना आधार कार्ड अपलोड करें',
        'upload_pan': 'कर पहचान के लिए अपना पैन कार्ड अपलोड करें',
        'upload_voter': 'निर्वाचन पहचान के लिए अपना मतदाता पहचान पत्र अपलोड करें',
        'gov_forms_title': 'महत्वपूर्ण सरकारी फॉर्म',
        'gov_forms_desc': 'बुजुर्ग नागरिकों के लिए महत्वपूर्ण फॉर्म का त्वरित उपयोग',
        'pension_application': 'पेंशन आवेदन',
        'pension_desc': 'विभिन्न पेंशन योजनाओं के लिए आवेदन करें',
        'healthcare_forms': 'स्वास्थ्य देखभाल फॉर्म',
        'healthcare_desc': 'चिकित्सा और स्वास्थ्य बीमा फॉर्म',
        'ration_card': 'राशन कार्ड',
        'ration_desc': 'अपना राशन कार्ड विवरण अपलोड या अद्यतन करें',
        'voter_id': 'मतदाता पहचान पत्र',
        'voter_desc': 'मतदाता पहचान पत्र के लिए आवेदन करें या विवरण अपडेट करें',
        'aadhaar_services': 'आधार सेवाएं',
        'aadhaar_desc': 'अपना आधार विवरण अपडेट या सत्यापित करें',
        'banking_forms': 'बैंकिंग फॉर्म',
        'banking_desc': 'वरिष्ठ नागरिक बैंकिंग सेवाएं',
        'back_to_form': 'फॉर्म पर वापस जाएं'
    },
    'mr': {
        'upload_document': 'दस्तऐव अपलोड करा',
        'processing_document': 'दस्तऐव प्रक्रिया',
        'extract_information': 'माहिती काढा',
        'review_extracted_information': 'काढलेली माहितीची समीक्षा करा',
        'edit_information': 'माहिती संपादित करा',
        'continue_to_form': 'फॉर्मवर चालू ठेवा',
        'select_form_type': 'फॉर्म प्रकार निवडा',
        'income_certificate': 'उत्पन्न प्रमाणपत्र',
        'birth_certificate': 'जन्म प्रमाणपत्र',
        'ration_card': 'रेशन कार्ड',
        'voice_input': 'आवाज इनपुट',
        'generate_pdf': 'पीडीएफ तयार करा',
        'start_speaking': 'बोलणे सुरू करा',
        'form_title': 'फॉर्म शीर्षक',
        'upload_aadhaar_pan': 'आधार, पॅन, मतदार ओळखपत्र किंवा इतर सरकारी दस्तऐव अपलोड करा',
        'apply_income': 'विविध प्रयोजनांसाठी उत्पन्न प्रमाणपत्रासाठी अर्ज करा',
        'apply_birth': 'जन्म प्रमाणपत्र किंवा प्रत बनवा',
        'apply_ration': 'रेशन कार्डसाठी अर्ज करा किंवा तपशील अपडेट करा',
        'pdf_generated': 'पीडीएफ यशस्वीरित्या तयार झाला आणि डाउनलोड सुरू झाला!',
        'voice_input_processed': 'आवाज इनपुट कार्यक्षमता वास्तविक अंमलबजावणीमध्ये फॉर्म फील्ड अपडेट करेल.',
        'speech_processed': 'भाषण यशस्वीरित्या प्रक्रिया केली!',
        'listening_now': 'ऐकत आहे... कृपया बोला.',
        'processing_speech': 'आपल्या भाषणाची प्रक्रिया केली जात आहे...',
        'speech_recognition_not_supported': 'या ब्राउझरमध्ये भाषण ओळख समर्थित नाही.',
        'recognized': 'ओळखले',
        'error_starting_recognition': 'ओळख सुरू करताना त्रुटी',
        'error': 'त्रुटी',
        'success': 'यश',
        'info': 'माहिती',
        'read_aloud': 'जोरात वाचा',
        'read_text': 'मजकूर वाचा',
        // Status messages
        'no_document_selected': 'कृपया अपलोड करण्यासाठी काहीतरी दस्तऐव निवडा',
        'uploading_document': 'दस्तऐव अपलोड केले जात आहे...',
        'document_uploaded_successfully': 'दस्तऐव यशस्वीरित्या अपलोड झाले.',
        'upload_failed': 'अपलोड अयशस्वी झाले',
        // Extraction messages
        'extracting_information': 'माहिती काढली जात आहे...',
        'information_extracted_successfully': 'माहिती यशस्वीरित्या काढली गेली',
        'extraction_failed': 'माहिती काढणे अयशस्वी झाले',
        'extraction_error': 'माहिती काढताना त्रुटी',
        'upload_error': 'अपलोड त्रुटी',
        'no_document_uploaded': 'कोणतेही दस्तऐव अपलोड केलेले नाही',
        'document_id_or_form_type_not_set': 'दस्तऐव आयडी किंवा फॉर्म प्रकार सेट केलेला नाही',
        'no_entities_extracted': 'कोणतेही घटक काढलेले नाहीत',
        'no_content_available_to_read': 'वाचण्यासाठी कोणतीही सामग्री उपलब्ध नाही.',
        // Form field labels
        'applicant_name': 'अर्जदाराचे नाम',
        'father_or_husband_name': 'वडील / पतीचे नाम',
        'date_of_birth': 'जन्मतारीख',
        'permanent_address': 'स्थायी पत्ता',
        'annual_income': 'वार्षिक उत्पन्न',
        'person_name': 'व्यक्तीचे नाम',
        'place_of_birth': 'जन्माचे स्थान',
        'head_of_family': 'कुटुंबाचे माथेकरणी',
        // Entity labels
        'name': 'पूर्ण नाम',
        'gender': 'लिंग',
        'address': 'पत्ता',
        'aadhaar': 'आधार क्रमांक',
        'pan': 'पॅन क्रमांक',
        'voter_id': 'मतदार ओळखपत्र',
        'parent_name': 'पालक / प्रतिनिधीचे नाम',
        'select_document_type': 'दस्तावेज प्रकार निवडा',
        'aadhaar_card': 'आधार कार्ड',
        'pan_card': 'पॅन कार्ड',
        'voter_id': 'मतदार ओळखपत्र',
        'upload_aadhaar': 'ओळख पुष्टीसाठी आधार कार्ड अपलोड करा',
        'upload_pan': 'कर ओळखीसाठी पॅन कार्ड अपलोड करा',
        'upload_voter': 'निवडणूक ओळखीसाठी मतदार ओळखपत्र अपलोड करा',
        'gov_forms_title': 'महत्वाची सरकारी फॉर्म',
        'gov_forms_desc': 'वृद्ध नागरिकांसाठी महत्वाच्या फॉर्मचा जलद प्रवेश',
        'pension_application': 'पेन्शन अर्ज',
        'pension_desc': 'विविध पेन्शन योजनांसाठी अर्ज करा',
        'healthcare_forms': 'आरोग्य तपासणी फॉर्म',
        'healthcare_desc': 'मेडिकल आणि आरोग्य विमा फॉर्म',
        'ration_card': 'रेशन कार्ड',
        'ration_desc': 'रेशन कार्ड तपशील अपलोड किंवा अद्यतनित करा',
        'voter_id': 'मतदार ओळखपत्र',
        'voter_desc': 'मतदार ओळखपत्रासाठी अर्ज करा किंवा तपशील अपडेट करा',
        'aadhaar_services': 'आधार सेवा',
        'aadhaar_desc': 'आपले आधार तपशील अपडेट किंवा सत्यापित करा',
        'banking_forms': 'बँकिंग फॉर्म',
        'banking_desc': 'ज्येष्ठ नागरिक बँकिंग सेवा',
        'back_to_form': 'फॉर्मवर परत जा'
    }
};

// Get current language
function getCurrentLanguage() {
    return languageSelect.value || 'en';
}

// Translate text based on current language
function translate(key) {
    const lang = getCurrentLanguage();
    return translations[lang] && translations[lang][key] ? translations[lang][key] : translations['en'][key];
}

// Update UI text based on selected language
function updateUIText() {
    // Update document type selection section
    if (document.querySelector('#doctype-title')) document.querySelector('#doctype-title').textContent = translate('select_document_type');
    if (document.querySelector('[data-type="aadhaar"] h3')) document.querySelector('[data-type="aadhaar"] h3').textContent = translate('aadhaar_card');
    if (document.querySelector('[data-type="pan"] h3')) document.querySelector('[data-type="pan"] h3').textContent = translate('pan_card');
    if (document.querySelector('[data-type="voter"] h3')) document.querySelector('[data-type="voter"] h3').textContent = translate('voter_id');
    if (document.querySelector('[data-type="aadhaar"] p')) document.querySelector('[data-type="aadhaar"] p').textContent = translate('upload_aadhaar');
    if (document.querySelector('[data-type="pan"] p')) document.querySelector('[data-type="pan"] p').textContent = translate('upload_pan');
    if (document.querySelector('[data-type="voter"] p')) document.querySelector('[data-type="voter"] p').textContent = translate('upload_voter');
    
    // Update button texts
    if (document.querySelector('#upload-btn')) document.querySelector('#upload-btn').textContent = translate('upload_document');
    if (document.querySelector('#extract-btn')) document.querySelector('#extract-btn').textContent = translate('extract_information');
    if (document.querySelector('#edit-entities-btn')) document.querySelector('#edit-entities-btn').textContent = translate('edit_information');
    if (document.querySelector('#continue-btn')) document.querySelector('#continue-btn').textContent = translate('continue_to_form');
    if (document.querySelector('#voice-input-btn')) document.querySelector('#voice-input-btn').textContent = translate('voice_input');
    if (document.querySelector('#generate-pdf-btn')) document.querySelector('#generate-pdf-btn').textContent = translate('generate_pdf');
    if (document.querySelector('#start-voice-btn')) document.querySelector('#start-voice-btn').textContent = translate('start_speaking');
    
    // Update section headings
    if (document.querySelector('#upload-title')) document.querySelector('#upload-title').textContent = translate('upload_document');
    if (document.querySelector('#processing-title')) document.querySelector('#processing-title').textContent = translate('processing_document');
    if (document.querySelector('#review-title')) document.querySelector('#review-title').textContent = translate('review_extracted_information');
    if (document.querySelector('#form-select-title')) document.querySelector('#form-select-title').textContent = translate('select_form_type');
    
    // Update section descriptions
    if (document.querySelector('#upload-desc')) document.querySelector('#upload-desc').textContent = translate('upload_aadhaar_pan');
    if (document.querySelector('#processing-desc')) document.querySelector('#processing-desc').textContent = translate('extracting_information').replace('Extracting information...', 'Please wait while we extract information from your document...');
    if (document.querySelector('#review-desc')) document.querySelector('#review-desc').textContent = translate('edit_information').replace('Edit Information', 'If any information is incorrect, please click \'Edit Information\' to make changes');
    if (document.querySelector('#form-desc')) document.querySelector('#form-desc').textContent = translate('review_extracted_information').replace('Review Extracted Information', 'Please check all information below. You can make changes if needed.');
    
    // Update form option texts
    if (document.querySelector('[data-form="income_certificate"] h3')) document.querySelector('[data-form="income_certificate"] h3').textContent = translate('income_certificate');
    if (document.querySelector('[data-form="birth_certificate"] h3')) document.querySelector('[data-form="birth_certificate"] h3').textContent = translate('birth_certificate');
    if (document.querySelector('[data-form="ration_card"] h3')) document.querySelector('[data-form="ration_card"] h3').textContent = translate('ration_card');
    
    if (document.querySelector('[data-form="income_certificate"] p')) document.querySelector('[data-form="income_certificate"] p').textContent = translate('apply_income');
    if (document.querySelector('[data-form="birth_certificate"] p')) document.querySelector('[data-form="birth_certificate"] p').textContent = translate('apply_birth');
    if (document.querySelector('[data-form="ration_card"] p')) document.querySelector('[data-form="ration_card"] p').textContent = translate('apply_ration');
    
    // Update voice modal text
    if (document.querySelector('#voice-modal-title')) document.querySelector('#voice-modal-title').textContent = translate('voice_input');
    if (document.querySelector('#voice-modal-desc')) document.querySelector('#voice-modal-desc').textContent = translate('listening_now').replace('Listening... Please speak now.', 'Click the button below and speak to add information:');
    
    // Update TTS button text
    if (document.querySelector('#tts-btn')) document.querySelector('#tts-btn').innerHTML = '<span class="tts-icon">🔊</span> ' + translate('read_aloud');
    
    // Update government forms section
    if (document.querySelector('#gov-forms-title')) document.querySelector('#gov-forms-title').textContent = translate('gov_forms_title');
    if (document.querySelector('#gov-forms-desc')) document.querySelector('#gov-forms-desc').textContent = translate('gov_forms_desc');
    if (document.querySelector('[data-form="pension"] h3')) document.querySelector('[data-form="pension"] h3').textContent = translate('pension_application');
    if (document.querySelector('[data-form="pension"] p')) document.querySelector('[data-form="pension"] p').textContent = translate('pension_desc');
    if (document.querySelector('[data-form="health"] h3')) document.querySelector('[data-form="health"] h3').textContent = translate('healthcare_forms');
    if (document.querySelector('[data-form="health"] p')) document.querySelector('[data-form="health"] p').textContent = translate('healthcare_desc');
    if (document.querySelector('[data-form="ration"] h3')) document.querySelector('[data-form="ration"] h3').textContent = translate('ration_card');
    if (document.querySelector('[data-form="ration"] p')) document.querySelector('[data-form="ration"] p').textContent = translate('ration_desc');
    if (document.querySelector('[data-form="voter"] h3')) document.querySelector('[data-form="voter"] h3').textContent = translate('voter_id');
    if (document.querySelector('[data-form="voter"] p')) document.querySelector('[data-form="voter"] p').textContent = translate('voter_desc');
    if (document.querySelector('[data-form="aadhaar"] h3')) document.querySelector('[data-form="aadhaar"] h3').textContent = translate('aadhaar_services');
    if (document.querySelector('[data-form="aadhaar"] p')) document.querySelector('[data-form="aadhaar"] p').textContent = translate('aadhaar_desc');
    if (document.querySelector('[data-form="banking"] h3')) document.querySelector('[data-form="banking"] h3').textContent = translate('banking_forms');
    if (document.querySelector('[data-form="banking"] p')) document.querySelector('[data-form="banking"] p').textContent = translate('banking_desc');
    if (document.querySelector('#back-to-form-btn')) document.querySelector('#back-to-form-btn').textContent = translate('back_to_form');
}

// Text-to-speech function
function speakText(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        if (isSpeaking && speechUtterance) {
            window.speechSynthesis.cancel();
            isSpeaking = false;
            return;
        }
        
        // Set language based on selection
        const lang = getCurrentLanguage();
        
        // Function to actually speak the text with the selected voice
        const speakWithVoice = function() {
            // Create a new speech utterance
            speechUtterance = new SpeechSynthesisUtterance(text);
            
            // Try to find the best available voice for the selected language
            const voices = window.speechSynthesis.getVoices();
            let selectedVoice = null;
            
            if (lang === 'hi') {
                // Try to find a Hindi voice
                selectedVoice = voices.find(voice => voice.lang.includes('hi') || voice.lang.includes('hi-IN'));
            } else if (lang === 'mr') {
                // Try to find a Marathi voice
                selectedVoice = voices.find(voice => voice.lang.includes('mr') || voice.lang.includes('mr-IN'));
            } else {
                // Default to English
                selectedVoice = voices.find(voice => voice.lang.includes('en') || voice.lang.includes('en-US'));
            }
            
            // If no specific voice found for the language, try to find any available voice
            if (!selectedVoice) {
                selectedVoice = voices.find(voice => voice.default) || voices[0];
            }
            
            if (selectedVoice) {
                speechUtterance.voice = selectedVoice;
            }
            
            // Set speech properties
            speechUtterance.rate = 0.9; // Slightly slower rate for better clarity
            speechUtterance.pitch = 1.0;
            speechUtterance.volume = 1.0;
            
            // Event listeners
            speechUtterance.onstart = function() {
                isSpeaking = true;
                ttsBtn.innerHTML = '<span class="tts-icon">🔇</span> ' + translate('read_aloud').replace('Read Aloud', 'Stop Reading');
            };
            
            speechUtterance.onend = function() {
                isSpeaking = false;
                ttsBtn.innerHTML = '<span class="tts-icon">🔊</span> ' + translate('read_aloud');
            };
            
            speechUtterance.onerror = function(event) {
                console.error('Speech synthesis error:', event.error);
                isSpeaking = false;
                ttsBtn.innerHTML = '<span class="tts-icon">🔊</span> ' + translate('read_aloud');
            };
            
            // Speak the text
            window.speechSynthesis.speak(speechUtterance);
        };
        
        // Check if voices are already loaded
        if (window.speechSynthesis.getVoices().length > 0) {
            speakWithVoice();
        } else {
            // If voices are not loaded yet, wait for the voiceschanged event
            window.speechSynthesis.onvoiceschanged = function() {
                speakWithVoice();
                window.speechSynthesis.onvoiceschanged = null; // Remove the event listener after using it
            };
        }
    } else {
        // Fallback: alert the text if speech synthesis is not supported
        alert('Text-to-speech is not supported in your browser. Text: ' + text);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Document type selection events
    document.querySelectorAll('.doctype-option').forEach(option => {
        option.addEventListener('click', () => selectDocumentType(option.dataset.type));
    });
    
    // Upload button event
    uploadBtn.addEventListener('click', handleDocumentUpload);
    
    // Extract button event
    extractBtn.addEventListener('click', handleInformationExtraction);
    
    // Edit entities button event
    editEntitiesBtn.addEventListener('click', enableEditEntities);
    
    // Continue button event
    continueBtn.addEventListener('click', showFormSelection);
    
    // Form selection events
    document.querySelectorAll('.form-option').forEach(option => {
        option.addEventListener('click', () => selectFormType(option.dataset.form));
    });
    
    // Generate PDF button event
    generatePdfBtn.addEventListener('click', generatePdf);
    
    // Voice input button event - REMOVED
    // voiceInputBtn.addEventListener('click', openVoiceModal);
    
    // Close voice modal - REMOVED
    // closeVoiceModal.addEventListener('click', closeVoiceModalFunc);
    
    // Start voice input - REMOVED
    // startVoiceBtn.addEventListener('click', startVoiceInput);
    
    // Close modal when clicking outside - REMOVED
    // voiceModal.addEventListener('click', (event) => {
    //     // Close modal only if the click is directly on the modal background, not on its content
    //     if (event.target === voiceModal) {
    //         closeVoiceModalFunc();
    //     }
    // });
    
    
    // Language selection event
    languageSelect.addEventListener('change', updateUIText);
    
    // Text-to-speech button event
    ttsBtn.addEventListener('click', function() {
        if (isSpeaking) {
            // Stop speaking
            window.speechSynthesis.cancel();
            isSpeaking = false;
            ttsBtn.innerHTML = '<span class="tts-icon">🔊</span> ' + translate('read_aloud');
        } else {
            // Read page content
            const pageText = getPageText();
            speakText(pageText);
        }
    });
    
    // Government forms section events
    document.querySelectorAll('.gov-form-link').forEach(link => {
        link.addEventListener('click', () => handleGovFormSelection(link.dataset.form));
    });
    
    // Back to form button event
    document.getElementById('back-to-form-btn')?.addEventListener('click', () => {
        document.querySelector('#gov-forms-section').classList.add('hidden');
        document.querySelector('#fill-section').classList.remove('hidden');
    });
});

// Select document type and show upload section
function selectDocumentType(docType) {
    // Store the selected document type for later use
    currentDocumentType = docType;
    
    // Hide document type selection and show upload section
    document.querySelector('#doctype-section').classList.add('hidden');
    document.querySelector('#upload-section').classList.remove('hidden');
    
    // Update upload section based on document type
    const uploadTitle = document.querySelector('#upload-title');
    const uploadDesc = document.querySelector('#upload-desc');
    
    if (uploadTitle) {
        uploadTitle.textContent = translate('upload_document');
    }
    
    if (uploadDesc) {
        switch(docType) {
            case 'aadhaar':
                uploadDesc.textContent = translate('upload_aadhaar');
                break;
            case 'pan':
                uploadDesc.textContent = translate('upload_pan');
                break;
            case 'voter':
                uploadDesc.textContent = translate('upload_voter');
                break;
            default:
                uploadDesc.textContent = translate('upload_aadhaar_pan');
        }
    }
}

// Handle government form selection
function handleGovFormSelection(formType) {
    // This would normally redirect to the specific government form
    // For now, we'll just show an alert with the selected form type
    alert(`You selected: ${formType}. In a real implementation, this would redirect to the ${formType} form.`);
    
    // Or we could automatically fill the form with extracted data if available
    // For example, pre-fill with the extracted entities
    if (Object.keys(extractedEntities).length > 0) {
        console.log('Pre-filling form with extracted data:', extractedEntities);
        // In a real implementation, we would map the extracted entities to the specific form fields
    }
}

// Get all visible text content from the page
function getPageText() {
    const sections = document.querySelectorAll('.section:not(.hidden)');
    if (sections.length === 0) {
        // If no section is visible, read the main header
        return document.querySelector('header h1').textContent + '. ' + 
               document.querySelector('header p').textContent;
    }
    
    let text = '';
    sections.forEach(section => {
        const heading = section.querySelector('h2');
        if (heading) {
            text += heading.textContent + '. ';
        }
        
        const paragraphs = section.querySelectorAll('p');
        paragraphs.forEach(p => {
            text += p.textContent + ' ';
        });
        
        const buttons = section.querySelectorAll('button');
        buttons.forEach(button => {
            if (!button.closest('#voice-modal')) { // Don't read voice modal buttons when not in modal
                text += button.textContent + '. ';
            }
        });
        
        const inputs = section.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (input.type !== 'file') { // Skip file inputs
                text += input.placeholder || '';
            }
        });
    });
    
    // If no section-specific text, read form fields if visible
    if (!text.trim() && formFields && !formFields.classList.contains('hidden')) {
        const formFieldLabels = formFields.querySelectorAll('label');
        formFieldLabels.forEach(label => {
            text += label.textContent + ' ';
        });
    }
    
    // If we're in the entities display section, include entity values
    if (reviewSection && !reviewSection.classList.contains('hidden')) {
        const entityItems = document.querySelectorAll('#entities-display .entity-item');
        entityItems.forEach(item => {
            const label = item.querySelector('label');
            const value = item.querySelector('.entity-value');
            if (label && value) {
                text += `${label.textContent}: ${value.textContent}. `;
            }
        });
    }
    
    return text || translate('no_content_available_to_read');
}

// Handle document upload
async function handleDocumentUpload() {
    const files = documentUpload.files;
    if (files.length === 0) {
        showStatus(uploadStatus, translate('no_document_selected'), 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', files[0]); // For MVP, only process first file
    
    try {
        showStatus(uploadStatus, translate('uploading_document'), 'info');
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            currentDocumentId = result.document_id;
            showStatus(uploadStatus, `${translate('document_uploaded_successfully')} ID: ${currentDocumentId}`, 'success');
            
            // Show processing section
            uploadSection.classList.add('hidden');
            processingSection.classList.remove('hidden');
        } else {
            showStatus(uploadStatus, `${translate('upload_failed')}: ${result.detail}`, 'error');
        }
    } catch (error) {
        showStatus(uploadStatus, `${translate('upload_error')}: ${error.message}`, 'error');
    }
}

// Handle information extraction
async function handleInformationExtraction() {
    if (!currentDocumentId) {
        showStatus(extractionStatus, translate('no_document_uploaded'), 'error');
        return;
    }
    
    try {
        showStatus(extractionStatus, translate('extracting_information'), 'info');
        
        const response = await fetch('/extract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document_id: currentDocumentId
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            extractedEntities = result.entities;
            showStatus(extractionStatus, translate('information_extracted_successfully'), 'success');
            
            // Display entities
            displayEntities();
            
            // Show review section
            processingSection.classList.add('hidden');
            reviewSection.classList.remove('hidden');
        } else {
            showStatus(extractionStatus, `${translate('extraction_failed')}: ${result.detail}`, 'error');
        }
    } catch (error) {
        showStatus(extractionStatus, `${translate('extraction_error')}: ${error.message}`, 'error');
    }
}

// Display extracted entities
function displayEntities() {
    entitiesDisplay.innerHTML = '';
    
    if (Object.keys(extractedEntities).length === 0) {
        entitiesDisplay.innerHTML = `<p>${translate('no_entities_extracted')}</p>`;
        return;
    }
    
    const entities = Object.entries(extractedEntities);
    entities.forEach(([key, entity], index) => {
        const entityDiv = document.createElement('div');
        entityDiv.className = `entity-item ${entity.confidence < 0.8 ? 'low-confidence' : ''}`;
        entityDiv.style.setProperty('--item-index', index);
        
        const label = document.createElement('label');
        label.textContent = formatEntityLabel(key);
        
        const valueDiv = document.createElement('div');
        valueDiv.className = 'entity-value';
        valueDiv.textContent = entity.value;
        
        const confidenceDiv = document.createElement('div');
        confidenceDiv.className = 'entity-confidence';
        confidenceDiv.textContent = `Confidence: ${(entity.confidence * 100).toFixed(1)}%`;
        
        entityDiv.appendChild(label);
        entityDiv.appendChild(valueDiv);
        entityDiv.appendChild(confidenceDiv);
        
        entitiesDisplay.appendChild(entityDiv);
    });
}

// Format entity label for display
function formatEntityLabel(key) {
    // Use translations if available, otherwise fallback to formatting the key
    switch(key) {
        case 'name':
            return translate('name') || 'Full Name';
        case 'dob':
            return translate('date_of_birth') || 'Date of Birth';
        case 'gender':
            return translate('gender') || 'Gender';
        case 'address':
            return translate('address') || 'Address';
        case 'aadhaar':
            return translate('aadhaar') || 'Aadhaar Number';
        case 'pan':
            return translate('pan') || 'PAN Number';
        case 'voter_id':
            return translate('voter_id') || 'Voter ID';
        case 'parent_name':
            return translate('parent_name') || 'Parent/Guardian Name';
        default:
            return key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
}

// Enable edit mode for entities
function enableEditEntities() {
    const entityValues = document.querySelectorAll('.entity-value');
    
    entityValues.forEach((valueDiv, index) => {
        const parent = valueDiv.parentElement;
        const label = parent.querySelector('label').textContent.toLowerCase().replace(' ', '_').replace(/\s+/g, '_');
        const currentValue = valueDiv.textContent;
        
        // Create input field
        const input = document.createElement('input');
        input.type = 'text';
        input.value = currentValue;
        input.className = 'entity-input';
        
        // Replace value div with input
        valueDiv.style.display = 'none';
        parent.appendChild(input);
        
        // Add event to save changes
        input.addEventListener('blur', () => {
            const entityKey = Object.keys(extractedEntities)[index];
            if (entityKey) {
                extractedEntities[entityKey].value = input.value;
                valueDiv.textContent = input.value;
            }
        });
    });
    
    // Add save button
    const saveBtn = document.createElement('button');
    saveBtn.textContent = 'Save Changes';
    saveBtn.addEventListener('click', () => {
        // Update display values from inputs
        document.querySelectorAll('.entity-input').forEach((input, idx) => {
            const entityKey = Object.keys(extractedEntities)[idx];
            if (entityKey) {
                extractedEntities[entityKey].value = input.value;
                const valueDiv = input.previousElementSibling;
                if (valueDiv && valueDiv.className === 'entity-value') {
                    valueDiv.textContent = input.value;
                }
            }
        });
        
        // Switch back to display mode
        document.querySelectorAll('.entity-input').forEach(input => {
            input.remove();
        });
        document.querySelectorAll('.entity-value').forEach(value => {
            value.style.display = 'block';
        });
    });
    
    entitiesDisplay.appendChild(saveBtn);
}

// Show form selection
function showFormSelection() {
    reviewSection.classList.add('hidden');
    formSection.classList.remove('hidden');
    
    // Also provide access to government forms for elderly users
    // We'll add a link to the government forms section
    const govFormsLink = document.createElement('div');
    govFormsLink.id = 'gov-forms-link';
    govFormsLink.className = 'gov-forms-link';
    govFormsLink.innerHTML = `<p>Or access <a href="#" id="gov-forms-quick-link">important government forms for elderly citizens</a></p>`;
    
    // Add the link after the form selection options
    const formSelection = document.getElementById('form-selection');
    if (formSelection && !document.getElementById('gov-forms-link')) {
        formSelection.appendChild(govFormsLink);
        
        // Add event listener to the quick link
        document.getElementById('gov-forms-quick-link')?.addEventListener('click', (e) => {
            e.preventDefault();
            formSection.classList.add('hidden');
            document.querySelector('#gov-forms-section').classList.remove('hidden');
        });
    }
}

// Select form type
async function selectFormType(formType) {
    currentFormType = formType;
    
    try {
        // Call the fill-form endpoint to get the mapped data
        const response = await fetch('/fill-form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document_id: currentDocumentId,
                form_type: formType
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            filledFormData = result.filled_form_data;
            
            // Show form filling section
            formSection.classList.add('hidden');
            fillSection.classList.remove('hidden');
            
            // Populate form fields
            populateFormFields(formType, filledFormData);
        } else {
            alert(`${translate('error')}: ${result.detail}`);
        }
    } catch (error) {
        alert(`${translate('error')}: ${error.message}`);
    }
}

// Populate form fields based on form type
function populateFormFields(formType, data) {
    // Get form template from backend (in a real app, this would be fetched)
    // For now, we'll use a simplified approach
    formTitle.textContent = getFormTitle(formType);
    
    formFields.innerHTML = '';
    
    // Create form fields based on the form type
    for (const [fieldName, value] of Object.entries(data)) {
        const fieldDiv = document.createElement('div');
        fieldDiv.className = 'form-field';
        
        // Create label
        const label = document.createElement('label');
        label.textContent = formatFieldLabel(fieldName);
        if (isRequiredField(fieldName)) {
            label.innerHTML += '<span class="required">*</span>';
        }
        
        // Create input/textarea
        let input;
        if (fieldName.includes('address') || fieldName.includes('reason') || fieldName.includes('remarks')) {
            input = document.createElement('textarea');
        } else {
            input = document.createElement('input');
            input.type = 'text';
        }
        
        input.id = fieldName;
        input.value = value || '';
        
        fieldDiv.appendChild(label);
        fieldDiv.appendChild(input);
        
        formFields.appendChild(fieldDiv);
    }
}

// Format field label for display
function formatFieldLabel(fieldName) {
    return fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Check if field is required
function isRequiredField(fieldName) {
    const requiredFields = ['applicant_name', 'person_name', 'head_of_family', 'financial_year', 'annual_income'];
    return requiredFields.includes(fieldName);
}

// Get form title based on type
function getFormTitle(formType) {
    const titles = {
        'income_certificate': 'Income Certificate Application',
        'birth_certificate': 'Birth Certificate Application',
        'ration_card': 'Ration Card Application'
    };
    return titles[formType] || 'Government Form';
}

// Open voice input modal - REMOVED
// function openVoiceModal() {
//     voiceModal.classList.remove('hidden');
// }

// Close voice modal - REMOVED
// function closeVoiceModalFunc() {
//     if(voiceModal) {
//         voiceModal.classList.add('hidden');
//     }
//     // Reset voice status when closing
//     if(voiceStatus) {
//         voiceStatus.textContent = 'Ready to listen...';
//     }
// }

// Start voice input - REMOVED
// function startVoiceInput() {
//     voiceStatus.textContent = translate('listening_now');
//     
//     // Check if browser supports speech recognition
//     if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
//         voiceStatus.textContent = 'Speech recognition not supported in this browser.';
//         return;
//     }
//     
//     const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
//     const recognition = new SpeechRecognition();
//     
//     recognition.continuous = false;
//     recognition.interimResults = false;
//     const lang = getCurrentLanguage();
//     recognition.lang = lang === 'hi' ? 'hi-IN' : lang === 'mr' ? 'mr-IN' : 'en-IN'; // Language based on selection
//     
//     recognition.onresult = function(event) {
//         const transcript = event.results[0][0].transcript;
//         voiceStatus.textContent = `Recognized: ${transcript}`;
//         
//         // Process the recognized text
//         processVoiceInput(transcript);
//     };
//     
//     recognition.onerror = function(event) {
//         voiceStatus.textContent = `${translate('error')}: ${event.error}`;
//     };
//     
//     recognition.onend = function() {
//         console.log('Speech recognition ended');
//     };
//     
//     try {
//         recognition.start();
//     } catch (error) {
//         voiceStatus.textContent = `${translate('error_starting_recognition')}: ${error.message}`;
//     }
// }

// Process voice input and update form fields - REMOVED
// function processVoiceInput(transcript) {
//     // Simple NLP to extract information from speech
//     // In a real implementation, this would use more sophisticated NLP
//     
//     const transcriptLower = transcript.toLowerCase();
//     
//     // Example: "My name is John Doe"
//     const nameMatch = transcriptLower.match(/name is ([^.!?]+)/i);
//     if (nameMatch) {
//         const name = nameMatch[1].trim();
//         const nameField = document.getElementById('applicant_name') || 
//                          document.getElementById('person_name') || 
//                          document.getElementById('head_of_family');
//         if (nameField) {
//             nameField.value = name;
//         }
//     }
//     
//     // Example: "My date of birth is 12-05-2003"
//     const dobMatch = transcriptLower.match(/date of birth is ([^.!?]+)/i);
//     if (dobMatch) {
//         const dob = dobMatch[1].trim();
//         const dobField = document.getElementById('date_of_birth');
//         if (dobField) {
//             dobField.value = dob;
//         }
//     }
//     
//     // Example: "My address is Mumbai, Maharashtra"
//     const addressMatch = transcriptLower.match(/address is ([^.!?]+)/i);
//     if (addressMatch) {
//         const address = addressMatch[1].trim();
//         const addressField = document.getElementById('permanent_address') || 
//                             document.getElementById('address');
//         if (addressField) {
//             addressField.value = address;
//         }
//     }
//     
//     // Example: "My income is two lakh fifty thousand per year"
//     const incomeMatch = transcriptLower.match(/income is ([^.!?]+)/i);
//     if (incomeMatch) {
//         const income = incomeMatch[1].trim();
//         const incomeField = document.getElementById('annual_income');
//         if (incomeField) {
//             incomeField.value = income;
//         }
//     }
//     
//     // More sophisticated processing would go here
//     
//     // Update extracted entities if we're in the review phase
//     updateEntitiesFromVoice(transcript);
//     
//     voiceStatus.textContent = `Processed: ${transcript}`;
//     
//     // Show success message
//     setTimeout(() => {
//         voiceStatus.textContent = translate('speech_processed');
//     }, 2000);
// }
// 
// // Update entities from voice input - REMOVED
// function updateEntitiesFromVoice(transcript) {
//     const transcriptLower = transcript.toLowerCase();
//     
//     // Update name if mentioned
//     const nameMatch = transcriptLower.match(/name is ([^.!?]+)/i);
//     if (nameMatch) {
//         const name = nameMatch[1].trim();
//         if (extractedEntities.name) {
//             extractedEntities.name.value = name;
//         }
//     }
//     
//     // Update other entities as needed
//     // This would be expanded based on requirements
// }

// Generate PDF
async function generatePdf() {
    if (!currentDocumentId || !currentFormType) {
        alert(translate('document_id_or_form_type_not_set'));
        return;
    }
    
    try {
        // Collect form data
        const formData = {};
        document.querySelectorAll('#form-fields input, #form-fields textarea').forEach(field => {
            formData[field.id] = field.value;
        });
        
        // Call the backend to generate PDF
        const response = await fetch('/generate-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document_id: currentDocumentId,
                form_type: currentFormType
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Create a download link for the PDF
            const downloadUrl = `/${result.pdf_path}`;
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = `form_${currentFormType}_${new Date().getTime()}.pdf`;
            link.click();
            
            alert(translate('pdf_generated'));
        } else {
            alert(`${translate('error')}: ${result.detail}`);
        }
    } catch (error) {
        alert(`${translate('error')}: ${error.message}`);
    }
}

// Show status message
function showStatus(element, message, type) {
    element.textContent = message;
    element.className = `status ${type}`;
    
    // Add type-specific styling if needed (though CSS handles most of it now)
    switch (type) {
        case 'success':
            break;
        case 'error':
            break;
        case 'info':
            break;
    }
}

// Update the formatFieldLabel function to use translations where appropriate
function formatFieldLabel(fieldName) {
    // Use translations if available, otherwise fallback to formatting the field name
    switch(fieldName) {
        case 'applicant_name':
            return translate('applicant_name') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        case 'father_or_husband_name':
            return translate('father_or_husband_name') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        case 'date_of_birth':
            return translate('date_of_birth') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        case 'permanent_address':
            return translate('permanent_address') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        case 'annual_income':
            return translate('annual_income') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        case 'person_name':
            return translate('person_name') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        case 'place_of_birth':
            return translate('place_of_birth') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        case 'head_of_family':
            return translate('head_of_family') || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        default:
            return fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
}