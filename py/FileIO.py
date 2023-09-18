# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:23:46 2023

@author: COnnor.gibbs
"""

import os
import chardet
import io
import numpy as np
import pandas as pd
import msoffcrypto
from PyPDF2 import PdfReader, PdfWriter

def absolute_file_paths_with_extension(directory, extensions=None, recursive=True):
    """Generate absolute file paths with specified extensions in a directory."""
    for root, _, filenames in os.walk(directory):
        if not recursive and root != directory:
            continue
        for filename in filenames:
            file_path = os.path.join(root, filename)
            _, ext = os.path.splitext(filename)
            if not extensions or ext.lower() in extensions and os.path.isfile(file_path):
                yield os.path.abspath(file_path)

def read_txt_lines(txt_path):
    """read lines of a text file to a list"""
    with open(txt_path, 'rb') as my_file:
        raw_data = my_file.read()

    # Use chardet to detect the encoding
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    # Open the file again with the detected encoding
    with open(txt_path, 'r', encoding=encoding) as my_file:
        data = my_file.read()
        data_into_list = data.split("\n")
    
    # Remove empty strings
    data_into_list = [x for x in data_into_list if x != '']
    
    # Split by tab
    data_into_list = [x.split('\t') for x in data_into_list]
    data_into_list = [[elem for elem in inner_list if elem != ''] for inner_list in data_into_list]
    
    return data_into_list

def read_encrypted_xlsx(file_path, password, header = None):
    decrypted_workbook = io.BytesIO()
    with open(file_path, 'rb') as file:
        office_file = msoffcrypto.OfficeFile(file)
        office_file.load_key(password=password)
        office_file.decrypt(decrypted_workbook)    
    df = pd.read_excel(decrypted_workbook, header = header)
    return df

def decrypt_pdf(file_path, password, file_suffix = "_decrypted"):
    filename = os.path.splitext(file_path)[0]
    output_path = f"{filename}{file_suffix}.pdf"
    with open(file_path, "rb") as input_file:
        pdf_reader = PdfReader(input_file)

        if pdf_reader.decrypt(password):
            pdf_writer = PdfWriter()

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
            
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)