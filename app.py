from flask import Flask, request, jsonify, render_template
import pandas as pd
import re

app = Flask(_name_)

def is_valid_email(email):
    # Simple email validation regex
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
      return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_csv(file)
        if 'email' not in df.columns:
            return jsonify({'error': 'CSV must contain an "email" column'}), 400

        emails = df['email'].tolist()
        valid_emails = [email for email in emails if is_valid_email(email)]
        invalid_emails = [email for email in emails if not is_valid_email(email)]

        return jsonify({
            'valid_emails': valid_emails,
            'invalid_emails': invalid_emails
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)
