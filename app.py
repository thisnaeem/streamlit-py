import streamlit as st
import os
from PIL import Image
import tempfile
import io
import subprocess
import sys
import glob
import zipfile

# Set page configuration
st.set_page_config(
    page_title="EPS to JPG Converter",
    page_icon="🖼️",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .error-message {
        color: #ff0000;
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def get_ghostscript_path():
    """Get the path to the Ghostscript executable."""
    if sys.platform.startswith('win'):
        # Common installation paths for Windows
        possible_paths = [
            r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
            r"C:\Program Files (x86)\gs\gs*\bin\gswin32c.exe",
            r"C:\Program Files\gs\gs*\bin\gswin32c.exe",
            r"C:\Program Files (x86)\gs\gs*\bin\gswin64c.exe"
        ]
        
        # Check each possible path
        for path in possible_paths:
            matches = glob.glob(path)
            if matches:
                return matches[0]
        
        # If not found in common paths, try PATH
        try:
            result = subprocess.run(['where', 'gswin64c'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
            
        return None
    return "gswin64c"  # Fallback for non-Windows systems

def check_ghostscript_installation():
    """Check if Ghostscript is properly installed."""
    gs_path = get_ghostscript_path()
    if not gs_path:
        st.markdown("""
            <div class="error-message">
                <h3>⚠️ Ghostscript Not Found</h3>
                <p>Please install Ghostscript to use this application:</p>
                <ol>
                    <li>Download Ghostscript from <a href="https://www.ghostscript.com/releases/gsdnld.html" target="_blank">here</a></li>
                    <li>Choose the "AGPL Release" version</li>
                    <li>Download the Windows installer (64-bit)</li>
                    <li>Run the installer as Administrator</li>
                    <li>Make sure to check "Add Ghostscript to the system PATH" during installation</li>
                    <li>Restart your computer after installation</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        return False
    return True

def convert_eps_to_jpg(eps_file):
    try:
        # Create a temporary file for the output
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            output_path = tmp.name

        # Get Ghostscript path
        gs_path = get_ghostscript_path()
        if not gs_path:
            st.error("Ghostscript not found. Please install it first.")
            return None
        
        # Convert EPS to JPG using Ghostscript
        args = [
            gs_path,
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r300",  # Resolution
            "-dEPSFitPage",
            "-g1000x1000",  # Set the output size (width x height in pixels)
            f"-sOutputFile={output_path}",
            eps_file
        ]
        
        # Run Ghostscript
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            st.error(f"Ghostscript error: {result.stderr}")
            return None

        # Open the converted image
        with Image.open(output_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr.seek(0)
            
            # Clean up temporary file
            os.unlink(output_path)
            
            return img_byte_arr
    except subprocess.CalledProcessError as e:
        st.error(f"Ghostscript error: {e.stderr}")
        return None
    except Exception as e:
        st.error(f"Error during conversion: {str(e)}")
        return None

# App title and description
st.title("🖼️ EPS to JPG Converter")
st.markdown("""
    Convert your EPS (Encapsulated PostScript) files to JPG format easily.
    Upload one or more files below to get started.
""")

# Check Ghostscript installation
if not check_ghostscript_installation():
    st.stop()

# File uploader (allow multiple files)
uploaded_files = st.file_uploader("Choose EPS file(s)", type=['eps'], accept_multiple_files=True)

if uploaded_files:
    if st.button("Convert to JPG (Bulk Supported)"):
        jpg_files = []
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(suffix='.eps', delete=False) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    eps_path = tmp.name
                jpg_bytes = convert_eps_to_jpg(eps_path)
                os.unlink(eps_path)
                if jpg_bytes:
                    # Add to zip
                    jpg_filename = os.path.splitext(uploaded_file.name)[0] + ".jpg"
                    zipf.writestr(jpg_filename, jpg_bytes.getvalue())
                    # Optionally, show preview
                    st.image(jpg_bytes, caption=jpg_filename, use_column_width=True)
        zip_buffer.seek(0)
        st.download_button(
            label="Download All JPGs as ZIP",
            data=zip_buffer,
            file_name="converted_images.zip",
            mime="application/zip"
        )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit") 