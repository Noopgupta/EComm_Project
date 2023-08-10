from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file from the request
        uploaded_file = request.files['file']

        if uploaded_file:
            # Save the uploaded file to a desired location (e.g., "uploads" folder)
            uploaded_file.save("uploads/" + uploaded_file.filename)
            return jsonify({"message": "File upload successful"})
        else:
            return jsonify({"error": "No file uploaded"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('file_upload.html')

if __name__ == '__main__':
    app.run(debug=True)
