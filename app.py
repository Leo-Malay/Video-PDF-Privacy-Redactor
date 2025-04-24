import streamlit as st
import os
import tempfile
import base64
from pdf_privacy_redactor import PDF_Privacy_Redactor

# Set page configuration
st.set_page_config(
    page_title="PDF Privacy Redactor",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for tokens
if 'tokens' not in st.session_state:
    st.session_state.tokens = ["security"]  # Default token

# Custom CSS for a beautiful UI
st.markdown("""
<style>
    /* Global styling */
    .main {
        background-color: #0e1117;
        color: white;
        padding: 0 !important;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, rgba(0,0,0,0.8) 0%, rgba(33,33,33,0.8) 100%);
        border-bottom: 1px solid #333;
        margin-bottom: 1.5rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #aaa;
        font-weight: 400;
    }
    
    /* Upload area styling */
    .upload-container {
        background-color: #1a1f29;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #333;
    }
    
    .upload-header {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Token management styling */
    .token-container {
        background-color: #1a1f29;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #333;
    }
    
    .token-header {
        font-size: 1.3rem;
        color: white;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    
    .token-item {
        display: flex;
        align-items: center;
        background-color: rgba(0,0,0,0.2);
        padding: 0.6rem;
        border-radius: 5px;
        margin-bottom: 0.4rem;
    }
    
    .token-text {
        flex: 1;
        color: #ddd;
        font-size: 0.9rem;
    }
    
    /* Preview container styling */
    .preview-container {
        background-color: #1a1f29;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #333;
    }
    
    .preview-header {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Download section styling */
    .download-container {
        background-color: #1a1f29;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #333;
        text-align: center;
    }
    
    .download-header {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Success message styling */
    .success-message {
        background-color: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    
    /* Error message styling */
    .error-message {
        background-color: rgba(244, 67, 54, 0.2);
        color: #F44336;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #F44336;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .redact-button {
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        color: white;
        font-weight: 600;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        border: none;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
        margin: 1rem 0;
        text-align: center;
        width: 100%;
        box-shadow: 0 4px 10px rgba(33, 150, 243, 0.3);
    }
    
    .redact-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(33, 150, 243, 0.4);
    }
    
    /* Features section styling */
    .features-container {
        background-color: #1a1f29;
        border-radius: 10px;
        padding: 1.5rem;
        height: 100%;
        border: 1px solid #333;
    }
    
    .features-header {
        font-size: 2rem;
        color: white;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-align: center;
    }
    
    .feature-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        background-color: rgba(0,0,0,0.2);
        padding: 1rem;
        border-radius: 8px;
    }
    
    .feature-icon {
        color: #4CAF50;
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    
    .feature-text {
        flex: 1;
    }
    
    .feature-title {
        font-weight: 600;
        color: white;
        margin-bottom: 0.3rem;
    }
    
    .feature-description {
        color: #aaa;
        font-size: 0.9rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #aaa;
        font-size: 0.9rem;
        border-top: 1px solid #333;
        margin-top: 2rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #2196F3, #4CAF50);
        color: white !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        border-radius: 30px !important;
        border: none !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 10px rgba(33, 150, 243, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(33, 150, 243, 0.4) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f29;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2196F3 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Function to display PDF
def display_pdf(file_path):
    # Opening file and encoding
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Embedding PDF in HTML
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>
    """
    
    # Displaying PDF
    st.markdown(pdf_display, unsafe_allow_html=True)

# Header
st.markdown('<div class="header-container"><h1 class="main-title">PDF Privacy Redactor</h1><p class="subtitle">Secure your documents by redacting sensitive information</p></div>', unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # File upload section
    st.markdown('<h2 class="upload-header">Choose a PDF file</h2>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("", type="pdf")
    
    # Variables to store file paths
    temp_file_path = None
    output_path = None
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name
        
        st.markdown(f'<div class="success-message">File uploaded successfully: {uploaded_file.name}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Token management section (SMALLER)
    st.markdown('<div class="token-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="token-header">Manage Redaction Tokens</h2>', unsafe_allow_html=True)
    
    # Display current tokens in a more compact way - FIXED NESTING ISSUE
    if st.session_state.tokens:
        for i, token in enumerate(st.session_state.tokens):
            # Use HTML for layout instead of nested columns
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        background-color: rgba(0,0,0,0.2); padding: 0.6rem; 
                        border-radius: 5px; margin-bottom: 0.4rem;">
                <div style="flex: 1; color: #ddd; font-size: 0.9rem;">{token}</div>
                <div id="delete_btn_{i}" style="color: #F44336; cursor: pointer;"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Handle delete with a separate button outside the HTML
            if st.button("Delete", key=f"delete_{i}", help="Remove this token"):
                st.session_state.tokens.pop(i)
                st.rerun()
    else:
        st.markdown('<div class="error-message">No tokens added yet. Add at least one token to redact.</div>', unsafe_allow_html=True)
    
    # Add new token - more compact
    col_input, col_button = st.columns([3, 1])
    with col_input:
        new_token = st.text_input("Add new token:", key="new_token", placeholder="Enter text to redact")
    with col_button:
        st.write("")  # For vertical alignment
        st.write("")  # For vertical alignment
        if st.button("Add", help="Add this token to the redaction list"):
            if new_token and new_token not in st.session_state.tokens:
                st.session_state.tokens.append(new_token)
                st.rerun()
            elif not new_token:
                st.error("Please enter a token")
            else:
                st.error("Token already exists")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Redact button (only show if file is uploaded)
    if uploaded_file is not None:
        # Create redactor instance
        redactor = PDF_Privacy_Redactor()
        
        # Process button
        if st.button("Redact Document", key="redact_button"):
            with st.spinner("Processing document..."):
                try:
                    # Load the document
                    redactor.loadDocument(temp_file_path)
                    
                    # Add patterns from session state
                    for token in st.session_state.tokens:
                        redactor.addPattern(token)
                    
                    # Identify patterns
                    identified = redactor.identify()
                    
                    # Redact all matches - use the correct method from test.py
                    redactor.redact()
                    
                    # Save the document
                    output_path = os.path.splitext(temp_file_path)[0] + "_redacted.pdf"
                    redactor.saveDocument(output_path)
                    
                    # Display success message
                    st.markdown(f'<div class="success-message">Document successfully redacted!</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f'<div class="error-message">Error: {str(e)}</div>', unsafe_allow_html=True)
    
    # PDF Preview section (only show if file is uploaded)
    if uploaded_file is not None:
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="preview-header">Document Preview</h2>', unsafe_allow_html=True)
        
        # Create tabs for original and redacted versions
        tabs = st.tabs(["Original Document", "Redacted Document"])
        
        with tabs[0]:
            # Display original PDF
            if temp_file_path:
                display_pdf(temp_file_path)
        
        with tabs[1]:
            # Display redacted PDF if available
            if output_path and os.path.exists(output_path):
                display_pdf(output_path)
            else:
                st.info("Redacted document will appear here after processing")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download section - MOVED AFTER PREVIEW
        if output_path and os.path.exists(output_path):
            st.markdown('<div class="download-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="download-header">Download Redacted Document</h2>', unsafe_allow_html=True)
            
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download Redacted PDF",
                    data=file,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}_redacted.pdf",
                    mime="application/pdf",
                    help="Download your redacted document"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h2 class="features-header">Features</h2>', unsafe_allow_html=True)
    
    # Feature 1
    st.markdown('''
    <div class="feature-item">
        <div class="feature-icon">✅</div>
        <div class="feature-text">
            <div class="feature-title">Automatic detection of sensitive information</div>
            <div class="feature-description">Our advanced algorithms identify and protect your confidential data.</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Feature 2
    st.markdown('''
    <div class="feature-item">
        <div class="feature-icon">✅</div>
        <div class="feature-text">
            <div class="feature-title">Secure redaction that cannot be reversed</div>
            <div class="feature-description">Once redacted, information cannot be recovered by any means.</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Feature 3
    st.markdown('''
    <div class="feature-item">
        <div class="feature-icon">✅</div>
        <div class="feature-text">
            <div class="feature-title">Fast processing of large documents</div>
            <div class="feature-description">Efficiently handle documents of all sizes with optimal performance.</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Feature 4
    st.markdown('''
    <div class="feature-item">
        <div class="feature-icon">✅</div>
        <div class="feature-text">
            <div class="feature-title">Privacy-first approach - no data stored</div>
            <div class="feature-description">Your documents are processed locally and never stored on our servers.</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">© 2025 PDF Privacy Redactor | Secure your documents with confidence</div>', unsafe_allow_html=True)

# Clean up temporary files when the app is done
def cleanup():
    if 'temp_file_path' in locals() and temp_file_path and os.path.exists(temp_file_path):
        os.unlink(temp_file_path)
    if 'output_path' in locals() and output_path and os.path.exists(output_path):
        os.unlink(output_path)

# Register the cleanup function to run when the app is done
import atexit
atexit.register(cleanup)

