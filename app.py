import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import io


def extract_table_content(table):
    rows = table.find_all('tr')
    table_data = []

    for row in rows:
        cells = row.find_all(['td', 'th'])
        row_data = [cell.get_text().strip() for cell in cells]

        if not any("* GPA" in cell or "* CGPA" in cell for cell in row_data):
            row_data = [cell for cell in row_data if cell.strip()]
            if row_data:
                table_data.append(row_data)

    return table_data

def get_php_output(url, roll_number, dob):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        roll_number_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'regno')))
        roll_number_field.send_keys(roll_number)

        dob_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'input-popup')))
        dob_field.send_keys(dob)

        dob_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'content')))

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        tables = soup.find_all('table')

        table_data = []
        for index, table in enumerate(tables[:3], start=1):
            table_content = extract_table_content(table)
            table_data.append(table_content)

        return table_data

    finally:
        driver.quit()

def get_download_link(df, filename, file_type='txt'):
    if file_type == 'txt':
        output = df.to_string(index=False)
        mime_type = 'text/plain'
    elif file_type == 'csv':
        output = df.to_csv(index=False)
        mime_type = 'text/csv'
    elif file_type == 'xlsx':
        output = df.to_excel(index=False)
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        raise ValueError("Invalid file type. Choose from 'txt', 'csv', or 'xlsx'.")

    b64 = base64.b64encode(output.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def main():
    st.title("KEC result viewer")
    st.write("Enter the URL of the result page:")
    url = st.text_input("URL")

    st.write("Upload an Excel file with Roll number and DOB columns.")
    uploaded_file = st.file_uploader("Choose a file")

    output_format = st.radio("Select Output Format:", ('Text (TXT)', 'CSV'))

    if uploaded_file is not None:
        input_data = pd.read_excel(uploaded_file)
        all_table_data = []
        progress_bar = st.progress(0)  
        progress_text = st.empty()  
        with st.spinner("Processing data..."):
            total_rows = len(input_data)
            processed_rows = 0

            for index, row in input_data.iterrows():
                roll_number = row['Roll number']
                dob = row['DOB']

                progress_text.text(f"Processing {processed_rows + 1} out of {total_rows} records")

                table_data = get_php_output(url, roll_number, dob)
                all_table_data.extend(table_data)

                processed_rows += 1
                progress_bar.progress(processed_rows / total_rows)  

        all_results = []
        for table_data in all_table_data:
            all_results.extend(table_data)

        df = pd.DataFrame(all_results)

        
        file_extension = ''
        if output_format == 'Text (TXT)':
            file_extension = 'txt'
        elif output_format == 'CSV':
            file_extension = 'csv'

        if file_extension:
            st.markdown(get_download_link(df, f'output_data.{file_extension}', file_type=file_extension), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
