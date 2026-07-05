from io import BytesIO

import pandas as pd
import streamlit as st
from openpyxl import Workbook

from excel_writer import COLUMNS, build_row
from extract import detect_media_type, extract_invoice_data
from validate import validate_invoice

st.title("Multi-Language Invoice Extractor")
st.write("Upload invoice images in any language and extract structured data automatically.")

if "results" not in st.session_state:
    st.session_state.results = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

uploaded_files = st.file_uploader(
    "Upload invoice images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

if st.button("Process Invoices"):
    for uploaded_file in uploaded_files:
        if uploaded_file.name in st.session_state.processed_files:
            continue

        with st.spinner(f"Processing {uploaded_file.name}..."):
            image_bytes = uploaded_file.getvalue()
            media_type = detect_media_type(uploaded_file.name)

            result = extract_invoice_data(image_bytes, media_type)
            result = validate_invoice(result)

            row = build_row(result, uploaded_file.name)

        st.session_state.processed_files.add(uploaded_file.name)
        st.session_state.results.append(row)

if st.session_state.results:
    total = len(st.session_state.results)
    needs_review_count = sum(
        1 for row in st.session_state.results if row["Needs Review"] == "Y"
    )
    st.write(f"**{total}** invoice(s) processed — **{needs_review_count}** need review.")

    df = pd.DataFrame(st.session_state.results, columns=COLUMNS)
    st.dataframe(df)

    workbook = Workbook()
    sheet = workbook.active
    sheet.append(COLUMNS)
    for row in st.session_state.results:
        sheet.append([row[column] for column in COLUMNS])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="Download Excel",
        data=buffer,
        file_name="extracted_invoices.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.info("Upload one or more invoice images above and click \"Process Invoices\" to get started.")
