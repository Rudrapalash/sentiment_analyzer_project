import os
import pandas as pd
from flask import Flask, render_template, request, send_file, redirect, url_for
from sentiment_analysis import get_sentiment

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.csv'):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            df = pd.read_csv(file_path)
            df = df[df['text'].str.strip().str.len() > 10]
            df['sentiment'] = df['text'].apply(get_sentiment)

            output_path = os.path.join(OUTPUT_FOLDER, 'sentiment_results.csv')
            df.to_csv(output_path, index=False)

            results = df.to_dict(orient='records')
            return render_template('index.html', results=results, show_table=True)

    return render_template('index.html', results=None, show_table=False)

@app.route('/download')
def download():
    output_path = os.path.join(OUTPUT_FOLDER, 'sentiment_results.csv')
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

