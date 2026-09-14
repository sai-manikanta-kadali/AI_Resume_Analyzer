import io
import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from resume_parser import extract_text
from analyzer import analyze_documents
from database import init_db, save_analysis, list_analyses, get_analysis, delete_analysis
from report import build_report

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
DB_PATH = os.path.join(os.path.dirname(__file__), 'resumate.db')
init_db(DB_PATH)

@app.get('/')
def health():
    return jsonify({'status': 'ok', 'service': 'Resumate AI API', 'version': '1.0.0'})

@app.post('/api/analyze')
def analyze():
    resume = request.files.get('resume')
    job_description = request.form.get('job_description', '').strip()
    if not resume:
        return jsonify({'error': 'Please upload a PDF or DOCX resume.'}), 400
    if not job_description:
        return jsonify({'error': 'Please provide a job description.'}), 400
    try:
        resume_text, metadata = extract_text(resume.filename or '', resume.read())
        result = analyze_documents(resume_text, job_description, metadata)
        result['analysis_date'] = datetime.now(timezone.utc).isoformat()
        result['history_id'] = save_analysis(DB_PATH, result)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception:
        app.logger.exception('Analysis failed')
        return jsonify({'error': 'Analysis could not be completed. Check the file and NLP setup, then try again.'}), 500

@app.post('/api/demo')
def demo():
    payload = request.get_json(silent=True) or {}
    resume_text = payload.get('resume_text', '').strip()
    job_description = payload.get('job_description', '').strip()
    if not resume_text or not job_description:
        return jsonify({'error': 'Demo data is incomplete.'}), 400
    try:
        result = analyze_documents(resume_text, job_description, {
            'filename': 'resumate-demo-resume.txt', 'file_type': 'DEMO',
            'page_count': None, 'character_count': len(resume_text)
        })
        result['analysis_date'] = datetime.now(timezone.utc).isoformat()
        result['history_id'] = save_analysis(DB_PATH, result)
        return jsonify(result)
    except Exception:
        app.logger.exception('Demo analysis failed')
        return jsonify({'error': 'Demo analysis could not be completed.'}), 500

@app.post('/api/report')
def report():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({'error': 'Analysis data is required.'}), 400
    try:
        document = build_report(payload)
        return send_file(io.BytesIO(document), mimetype='application/pdf', as_attachment=True, download_name='resumate-analysis.pdf')
    except Exception:
        app.logger.exception('Report generation failed')
        return jsonify({'error': 'Report generation failed.'}), 500

@app.get('/api/history')
def history():
    return jsonify(list_analyses(DB_PATH))

@app.get('/api/history/<int:analysis_id>')
def history_item(analysis_id):
    item = get_analysis(DB_PATH, analysis_id)
    if not item:
        return jsonify({'error': 'Analysis not found.'}), 404
    return jsonify(item)

@app.delete('/api/history/<int:analysis_id>')
def history_delete(analysis_id):
    if not delete_analysis(DB_PATH, analysis_id):
        return jsonify({'error': 'Analysis not found.'}), 404
    return jsonify({'deleted': True})

@app.errorhandler(413)
def too_large(_error):
    return jsonify({'error': 'File is too large. The maximum size is 8 MB.'}), 413

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
