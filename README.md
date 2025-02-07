# KEC Result View Automation

KEC Result View Automation is a tool designed to simplify the process of retrieving student semester results. Teachers can upload a CSV file containing student details, and the application automatically fetches the results and generates a CSV file with the retrieved data in minutes.

## Features
- Automates the retrieval of student results from the official results website.
- Processes CSV files containing roll numbers and dates of birth.
- Generates a CSV file with the fetched semester results quickly and efficiently.

## Requirements
- Python 3.x
- Required Python libraries (specified in `requirements.txt`)
- Internet connection for accessing the results website

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Jayasurya5454/Kec-Result-View-Automation.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Kec-Result-View-Automation
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Prepare a CSV file with the following columns:
   - Roll Number
   - Date of Birth (in the required format)

2. Run the application:
   ```bash
   python app.py
   ```

3. Upload the CSV file when prompted.

4. The application will fetch the results and generate an output CSV file with the semester results.

## Output
The output CSV file will contain the following columns:
- Roll Number
- Semester Results (and other relevant details fetched from the website)

## Benefits
- Saves time by automating the manual process.
- Reduces the effort required to collect results for multiple students.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

