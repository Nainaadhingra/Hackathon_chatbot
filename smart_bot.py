import os
import re
import textract
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/')
def index():
    return 'Welcome to the Smart Bot!'

# Temporary data store for documents (in-memory dictionary).
documents = {}

# Directory to store uploaded documents.
UPLOAD_FOLDER = 'uploads'

# Ensure the upload directory exists.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to extract text from documents using textract.
def extract_text_from_document(file_path):
    try:
        text = textract.process(file_path).decode('utf-8')
        return text
    except Exception as e:
        print(f"Error extracting text from document: {str(e)}")
        return None

# Route to upload a document.
@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        
        # Extract text from the uploaded document.
        text = extract_text_from_document(filename)
        
        if text:
            # Store the document in memory.
            documents[file.filename] = text
            return jsonify({'message': 'Document uploaded successfully'})
        else:
            return jsonify({'error': 'Failed to extract text from the document'})

# Route to search within documents.
@app.route('/search', methods=['GET'])
def search_documents():
    query = request.args.get('query')
    results = {}
    
    if query:
        # Perform a simple text search within documents.
        for filename, text in documents.items():
            matches = re.findall(query, text, re.IGNORECASE)
            if matches:
                results[filename] = matches

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
