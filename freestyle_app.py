# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 22:28:52 2025

@author: Lenovo
"""

import streamlit as st
import os
import tempfile

# Set page title
st.set_page_config(page_title="Renaming messy files", layout="wide")

# Sidebar Menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Messy files"])

# ------------------ v3 -------------------
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("file_renamer.log"),
        logging.StreamHandler()
    ]
)

logging.info(f"\n***************PROCESSING - DATA***************")

if menu == "Messy files":
    st.title("Sorting out messy files")
    uploaded_files = st.file_uploader("Upload messy files", accept_multiple_files=True)
    
    # Function to normalize file names
    def normalize_filename(filename):
        try:
            name, ext = os.path.splitext(filename)
            logging.info(f"Processing file: {filename}")
            for sep in ["_", "-", ";", "!", "@", "&", ",", "."]:
                name = name.replace(sep, " ")
            logging.debug(f"After replacing separators: {name}")
    
            parts = name.split()
            logging.debug(f"Parts after splitting: {parts}")
            year = None
            for part in parts:
                if part.isdigit() and len(part) == 4:
                    year = part
                    logging.warning(f"No valid year found for file: {filename}")
                    break
    
            if not year:
                print(f"Skipping: {filename} (no valid year found)")
                return None
    
            title_parts = parts[:parts.index(year)]
            movie_title = " ".join(title_parts).strip().title()
            director_parts = parts[parts.index(year) + 1:]
            director = " ".join(director_parts).strip().title() if director_parts else "Unknown"
            new_name = f"{movie_title} ({year}) - {director}{ext}"
            logging.info(f"New name generated: {new_name}")
            return new_name
    
        except Exception as e:
            logging.error(f"Error processing file {filename}: {e}")
            return None
        
    # Process uploaded files
    if uploaded_files:
        renamed_files = {}
        temp_dir = tempfile.mkdtemp()  # Temporary directory for storing files
    
        for uploaded_file in uploaded_files:
            new_name = normalize_filename(uploaded_file.name)
            if new_name:
                file_path = os.path.join(temp_dir, new_name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                renamed_files[new_name] = file_path
    
        # Show renamed files
        st.write("### Renamed Files")
        for old, new in renamed_files.items():
            st.write(f"✅ `{old}`")

        # Allow users to download renamed files
        for new_name, file_path in renamed_files.items():
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"Download {new_name}",
                    data=f,
                    file_name=new_name,
                    mime="application/octet-stream"
                )














