import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_embedding_model = None

SKILL_CATALOG = {
    'Programming': ['Python', 'Java', 'C++', 'JavaScript', 'TypeScript'],
    'Web': ['HTML', 'CSS', 'React', 'Node.js', 'Flask', 'Django', 'REST APIs'],
    'Database': ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB'],
    'AI/ML': ['Machine Learning', 'Deep Learning', 'NLP', 'TensorFlow', 'PyTorch', 'scikit-learn'],
    'Cloud/DevOps': ['AWS', 'Azure', 'Docker', 'Kubernetes'],
    'Tools': ['Git', 'GitHub', 'Linux'],
    'Soft Skills': ['Communication', 'Leadership', 'Teamwork', 'Problem Solving']
}
SECTION_ALIASES = {
    'Contact': ['contact', 'email', 'phone'], 'Summary': ['summary', 'objective', 'profile'],
    'Education': ['education', 'academic'], 'Skills': ['skills', 'technical skills'],
    'Experience': ['experience', 'employment', 'internship'], 'Projects': ['projects', 'project'],
    'Certifications': ['certification', 'certifications'], 'Achievements': ['achievement', 'awards'],
    'Publications': ['publication', 'research'], 'Languages': ['languages']
}
STOPWORDS = {'with', 'this', 'that', 'from', 'your', 'have', 'will', 'into', 'for', 'and', 'the', 'are', 'our', 'you', 'job', 'role', 'using', 'looking'}
ROLE_BASELINES = {
    'ai engineer': ['Python', 'Machine Learning', 'Deep Learning', 'NLP', 'TensorFlow', 'PyTorch', 'SQL', 'Docker', 'REST APIs', 'Git'],
    'machine learning engineer': ['Python', 'Machine Learning', 'Deep Learning', 'scikit-learn', 'TensorFlow', 'PyTorch', 'SQL', 'Docker', 'Git'],
    'data scientist': ['Python', 'SQL', 'Machine Learning', 'scikit-learn', 'Git'],
    'backend developer': ['Python', 'REST APIs', 'SQL', 'Git', 'Docker', 'Linux'],
}

def _contains(text, phrase):
    return re.search(r'(?<![\w+#])' + re.escape(phrase.lower()) + r'(?![\w+#])', text.lower()) is not None

def extract_skills(text):
    found = []
    for category, skills in SKILL_CATALOG.items():
        for skill in skills:
            if _contains(text, skill):
                found.append({'name': skill, 'category': category})
    return found

def role_baseline_skills(text):
    lower = text.lower()
    for role, skill_names in ROLE_BASELINES.items():
        if role in lower:
            return [{'name': skill, 'category': next((category for category, skills in SKILL_CATALOG.items() if skill in skills), 'Role baseline')} for skill in skill_names]
    return []

def detect_sections(text):
    lower = text.lower()
    return {section: any(re.search(r'(^|\n|\s)' + re.escape(alias) + r'\s*[:\n]', lower) for alias in aliases) for section, aliases in SECTION_ALIASES.items()}

def keywords(text, limit=24):
    tokens = re.findall(r'[a-zA-Z][a-zA-Z+#.-]{2,}', text.lower())
    counts = Counter(token for token in tokens if token not in STOPWORDS)
    return [token for token, _ in counts.most_common(limit)]

def semantic_similarity(resume, job):
    global _embedding_model
    try:
        from sentence_transformers import SentenceTransformer
        if _embedding_model is None:
            _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = _embedding_model.encode([resume, job])
        return round(float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]) * 100, 1), 'all-MiniLM-L6-v2 sentence-transformer'
    except Exception:
        # Keep analysis usable when the optional model is not cached locally.
        pass
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
    matrix = vectorizer.fit_transform([resume, job])
    return round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100, 1), 'TF-IDF cosine similarity'
