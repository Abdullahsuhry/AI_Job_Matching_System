import os
import json
from flask import Blueprint, current_app, request, jsonify
from werkzeug.utils import secure_filename
from .utils.parser import extract_text_from_file
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .utils.skills import extract_skills, recommend_courses
import requests
from . import config

bp = Blueprint('api', __name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'jobs.json')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_jobs():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_jobs(jobs):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)


@bp.route('/jobs', methods=['POST'])
def add_job():
    """Add a job description. Accepts JSON {"title":..., "description":...}"""
    data = request.get_json(force=True)
    if not data or 'description' not in data:
        return jsonify({'error': 'Missing description'}), 400

    jobs = load_jobs()
    job = {
        'id': len(jobs) + 1,
        'title': data.get('title', f'Job {len(jobs)+1}'),
        'description': data['description']
    }
    jobs.append(job)
    save_jobs(jobs)
    return jsonify(job), 201


@bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload resume file and return extracted text."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, filename)
        file.save(path)
        text = extract_text_from_file(path)
        return jsonify({'text': text}), 200
    return jsonify({'error': 'Unsupported file type'}), 400


@bp.route('/match', methods=['POST'])
def match_resume():
    """Match resume text (or uploaded file) against stored jobs and return similarity scores."""
    payload = request.get_json(force=True)
    resume_text = payload.get('text')
    if not resume_text:
        return jsonify({'error': 'Missing resume text'}), 400

    jobs = load_jobs()
    if not jobs:
        return jsonify({'error': 'No jobs available for matching'}), 400

    docs = [job['description'] for job in jobs]
    vectorizer = TfidfVectorizer(stop_words='english')
    docs_tfidf = vectorizer.fit_transform(docs + [resume_text])
    resume_vec = docs_tfidf[-1]
    job_vecs = docs_tfidf[:-1]
    sims = cosine_similarity(job_vecs, resume_vec).flatten()

    results = []
    for job, score in zip(jobs, sims):
        results.append({'id': job['id'], 'title': job['title'], 'score': float(score)})

    results = sorted(results, key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results}), 200


@bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume text and optionally compare against a job to find skill gaps.

    JSON payload:
      { "text": "...", "job_id": 1 }
    or
      { "text": "...", "job_description": "..." }
    """
    payload = request.get_json(force=True)
    text = payload.get('text')
    if not text:
        return jsonify({'error': 'Missing text to analyze'}), 400

    # Extract skills from resume
    resume_skills = extract_skills(text)

    # Determine job skills (from job_id or direct description)
    job_skills = []
    if 'job_id' in payload:
        try:
            jid = int(payload['job_id'])
            jobs = load_jobs()
            job = next((j for j in jobs if j.get('id') == jid), None)
            if job:
                job_skills = extract_skills(job.get('description', ''))
        except Exception:
            job_skills = []
    elif 'job_description' in payload:
        job_skills = extract_skills(payload.get('job_description', ''))

    missing = [s for s in job_skills if s not in resume_skills]
    recommendations = recommend_courses(missing)

    return jsonify({
        'resume_skills': resume_skills,
        'job_skills': job_skills,
        'missing_skills': missing,
        'course_recommendations': recommendations
    }), 200



@bp.route('/chat', methods=['POST'])
def chat_proxy():
    """Simple proxy endpoint to forward chat/LLM requests to configured LLM API.

    Expects JSON body and forwards it to `LLM_API_URL`. If `LLM_API_KEY` is set,
    it will be sent in `Authorization: Bearer <key>` header. This keeps the
    real key out of frontend code; set the env var locally or in your deploy.
    """
    if not config.LLM_API_URL:
        return jsonify({'error': 'LLM API not configured on server'}), 501

    payload = request.get_json(force=True)
    headers = {'Content-Type': 'application/json'}
    if config.LLM_API_KEY:
        headers['Authorization'] = f'Bearer {config.LLM_API_KEY}'

    try:
        resp = requests.post(config.LLM_API_URL, json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to reach LLM provider', 'details': str(e)}), 502

    try:
        return jsonify(resp.json()), resp.status_code
    except ValueError:
        # Not JSON response; return raw text
        return resp.text, resp.status_code
