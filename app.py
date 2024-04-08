import apt
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

# Function to install Google Chrome using python-apt
def install_chrome():
    # Create an instance of the apt Cache
    cache = apt.Cache()

    # Update the package lists
    cache.update()

    # Install Google Chrome
    chrome_pkg = cache['google-chrome-stable']
    if chrome_pkg.is_installed:
        print("Google Chrome is already installed.")
    else:
        chrome_pkg.mark_install()

    # Commit the changes
    cache.commit()

# Function to extract table content from HTML
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

# Function to fetch data from the website
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

# Function to generate download link
def get_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

# Streamlit app
def main():
    st.title("KEC result viewer")
    st.write("Enter the URL of the result page:")
    url = st.text_input("URL")
    
    st.write("Upload an Excel file with Roll number and DOB columns.")
    uploaded_file = st.file_uploader("Choose a file")
    
    if uploaded_file is not None:
        input_data = pd.read_excel(uploaded_file)
        all_table_data = []

        with st.spinner("Processing data..."):
            for index, row in input_data.iterrows():
                roll_number = row['Roll number']
                dob = row['DOB']

                st.write(f"Processing {index+1}  Person Result ...")
                table_data = get_php_output(url, roll_number, dob)
                all_table_data.extend(table_data)

        output_text = ""
        for table_data in all_table_data:
            for row_data in table_data:
                output_text += '\t'.join(row_data) + '\n'
            output_text += '\n'

        st.subheader("Output Text:")
        st.text_area("Output", value=output_text, height=600)

        st.markdown(get_download_link(output_text, 'output_data.txt'), unsafe_allow_html=True)

if __name__ == "__main__":
    install_chrome()  # Install Chrome before running the Streamlit app
    main()
