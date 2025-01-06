import streamlit as st
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
import os
from io import BytesIO
import tempfile
import google.generativeai as genai  # Import the Gemini AI library
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now, securely fetch the API key
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini AI with the loaded API key
import google.generativeai as genai
genai.configure(api_key=api_key)

# Set Tesseract command (update the path if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler path for PDF processing
poppler_path = r'C:\Program Files\poppler-24.08.0\Library\bin'



# Function to extract text from file
def extract_text(file):
    try:
        if file.name.endswith(".pdf"):
            # Save Streamlit UploadedFile to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                tmpfile.write(file.read())
                tmpfile.flush()
                # Convert PDF to images
                images = convert_from_path(tmpfile.name, poppler_path=poppler_path)
                text = ""
                for img in images:
                    text += pytesseract.image_to_string(img)
                return text
        elif file.name.endswith((".jpg", ".jpeg", ".png")):
            # Extract text from image
            img = Image.open(file)
            return pytesseract.image_to_string(img)
        else:
            st.error("Unsupported file format. Use PDF or image files.")
            return None
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None
    
# Function to save invoice data to Excel and update the file
def save_to_excel(invoice_data):
    output_path = "extracted_data/invoice_data.xlsx"
    # Create the directory if it doesn't exist
    os.makedirs("extracted_data", exist_ok=True)

    # Ensure invoice_data is a dictionary with specific keys for the columns
    expected_columns = ['Invoice Number', 'Date', 'Total Amount']

    # If any key is missing from the invoice_data, show an error
    if not all(key in invoice_data for key in expected_columns):
        st.error("Missing required keys in invoice data")
        return

    # Create a DataFrame from the invoice data dictionary
    new_df = pd.DataFrame([invoice_data])

    # If the file doesn't exist, create a new one, else load the existing file
    if not os.path.exists(output_path):
        # If file does not exist, create it
        new_df.to_excel(output_path, index=False)
    else:
        # Load the existing Excel file
        df = pd.read_excel(output_path)

        # Append the new invoice data to the existing DataFrame
        df = pd.concat([df, new_df], ignore_index=True)

        # Save the updated DataFrame back to the Excel file
        df.to_excel(output_path, index=False)

    # Notify the user that the data has been saved
    st.success(f"Data saved to {output_path}")


# Function to extract invoice data using Gemini AI
def extract_invoice_data_with_ai(text):
    prompt = """
    Extract the following fields from the invoice text: 
    - Invoice Number (this may be labeled as Invoice No, Bill Number, or similar).
    - Date (this may be labeled as Invoice Date, Bill Date, or similar).
    - Total Amount (or Amount), which may also appear as Total, Grand Total, Subtotal, or Due Amount.

    Only return the specified fields (Invoice Number, Date, Total Amount) in a structured format. Ignore any additional information and ensure that each field is clearly labeled.

    Invoice Text: 
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([text, prompt])
    
    # Print the raw response for debugging
    st.write("AI Response: ", response.text)
    
    extracted_data = {}

    # Parse the response carefully, considering variations in format
    for line in response.text.split('\n'):
        if "Invoice Number" in line:
            extracted_data["Invoice Number"] = line.split(":")[1].strip()
        elif "Date" in line:
            extracted_data["Date"] = line.split(":")[1].strip()
        elif "Total Amount" in line or "Amount" in line:
            extracted_data["Total Amount"] = line.split(":")[1].strip()

    return extracted_data



# Streamlit app
def main():
    st.title("Invoice Data Extractor")
    st.write("Upload an invoice (PDF or image) to extract structured data.")

    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "jpeg", "png"])

    if uploaded_file:
        st.write("Processing file...")

        # Extract text from the file
        text = extract_text(uploaded_file)

        if text:
            st.subheader("Extracted Text:")
            st.text_area("Text Output", text, height=300)

            # Use AI to extract invoice data
            invoice_data = extract_invoice_data_with_ai(text)

            # Ensure we have all required fields
            if invoice_data.get("Invoice Number") and invoice_data.get("Date") and invoice_data.get("Total Amount"):
                st.subheader("Extracted Invoice Data:")
                st.write(invoice_data)

                # Streamlit button for saving the data
                if st.button("Save to Excel"):
                    save_to_excel(invoice_data)
            else:
                st.error("Could not extract all required invoice fields.")

if __name__ == "__main__":
    main()
