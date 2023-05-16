import os
import subprocess
import streamlit as st
from streamlit_javascript import st_javascript
from typing import Tuple
import webbrowser
import utility.menu as menu
import utility.pdf2html as p2h
import shutil
import zipfile

def pdf_to_html(pdf_file: str) -> Tuple[str, str]:
    html_file = os.path.splitext(pdf_file)[0] + ".html"
    html_file_path = os.getcwd()+'/html_file'
    cmd = f"pdf2htmlEX --zoom 1.3 --embed cfijo --dest-dir {html_file_path} {pdf_file} {html_file}"
    st.write(cmd)
    st.write(html_file)
    
    #st.write(os.listdir())  # prints the list of files and directories in the current working directory
    subprocess.call(cmd, shell=True)
    return html_file, html_file_path

def scanpdf():
    # Streamlit app code
    menu_out = menu.menu()
    if menu_out == "PDF2HTML":

        st.title("PDF to HTML Converter")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        if uploaded_file:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
            st.write(file_details)

            # Convert PDF to HTML
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            html_file, html_file_path = pdf_to_html(uploaded_file.name)
            
            # Display HTML file
            st.write(f"Converted HTML file: {html_file_path} {html_file}")
    elif menu_out == 'OPEN-HTML':
        st.title("DOWNLOAD LANDING PAGE HTML")
        html_file_path = os.getcwd()+'/html_file'
        files = os.listdir(html_file_path)
        url = st_javascript("await fetch('').then(r => window.parent.location.href)")
        if st.button("Zip html file"):
            # Create a temporary zip file
            zip_path = os.getcwd() + '/temp/temp.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add all files in the folder to the zip file
                for root, dirs, files in os.walk(zip_path):
                    for file in files:
                        st.write(file)
                        zip_file.write(os.path.join(root, file))

            # Serve the zip file for download
            with open(zip_path, 'rb') as f:
                zipped_file = f.read()
                st.download_button('Download Zip File', data=zipped_file, file_name='html_file.zip')
        
