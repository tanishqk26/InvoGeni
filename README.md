

# InvoGeni

## Project Overview
InvoGeni is a powerful tool designed to extract structured data from invoices. Whether the invoice is in a PDF or image format (JPG, PNG, JPEG), the tool uses tesseract and artificial intelligence (AI) to extract key information such as:

- Invoice Number
- Date
- Total Amount

This tool leverages **Tesseract OCR** to convert PDFs and images into text, and **Google Gemini AI** (Generative AI) to intelligently extract relevant fields from the text.

## Features

- **Multi-format Support**: Extract data from PDF, JPG, PNG, and JPEG invoice files.
- **Automatic Data Extraction**: Using AI, the tool extracts Invoice Number, Date, and Total Amount from the invoice text.
- **Excel Export**: The extracted data can be saved into an Excel file for further processing and analysis.
- **Easy-to-Use Interface**: Built with **Streamlit**, the web interface allows users to upload invoices, view extracted data, and save it to an Excel sheet with a click.

## Technologies Used
- **Streamlit**: For building the interactive web interface.
- **Pytesseract**: OCR library for extracting text from PDF and image files.
- **pdf2image**: To convert PDF pages to images, which are then processed using OCR.
- **Google Gemini AI**: Used to extract structured invoice data (Invoice Number, Date, Total Amount) from the recognized text.
- **Pandas**: For handling data and saving extracted data to Excel files.

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- `pip` or `conda` for managing Python packages

### Installation Steps
1. **Clone the repository:**
   ```
   git clone https://github.com/your-repository/invoice-data-extractor.git
   cd invoice-data-extractor
   ```

2. **Install dependencies:**
   - Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
   - The `requirements.txt` file should contain the following dependencies:
     ```
     streamlit
     pytesseract
     pdf2image
     pillow
     pandas
     google-generativeai
     python-dotenv
     ```

3. **Install Poppler for PDF Processing (required by `pdf2image`):**
   - Download and install Poppler for your platform from [here](https://github.com/Belval/pdf2image#windows).
   - Add Poppler's `bin` directory to your system's PATH.

4. **Install Tesseract OCR:**
   - Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
   - Add the path to Tesseract to your system's PATH or update it directly in the script.

### Set up API Key
1. Create a `.env` file in the root directory of the project.
2. Add the following line with your **Google Gemini AI API Key**:
   ```
   GENAI_API_KEY=your_api_key_here
   ```
3. The tool will automatically read the API key from the `.env` file using the `python-dotenv` package.

### Run the Application
To run the Streamlit app, use the following command:
```
streamlit run app.py
```

The app will open in your default web browser where you can upload invoices and extract data.

## Usage
1. **Upload an Invoice**: Use the file uploader to choose a PDF or image file (JPG, PNG, JPEG).
2. **View Extracted Data**: After processing, the extracted text and structured invoice data will be displayed on the screen.
3. **Save Data**: Once the invoice data is successfully extracted, click the "Save to Excel" button to save the data to an Excel file.

The data will be saved in the `extracted_data/invoice_data.xlsx` file in the following format:
- Invoice Number
- Date
- Total Amount

## Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add feature'`).
4. Push to your fork (`git push origin feature-branch`).
5. Create a pull request.

## License
This project is licensed under the MIT License.

---

This `README` should give users clear instructions on how to set up and use your **Invoice Data Extractor** tool.
