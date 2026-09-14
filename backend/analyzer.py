from nlp import extract_skills, role_baseline_skills, detect_sections, keywords, semantic_similarity
from scoring import score_analysis
import re

def _candidate_name(resume_text):
    for line in resume_text.splitlines()[:5]:
        candidate = line.strip()
        if (candidate and len(candidate) <= 60 and '@' not in candidate and
                not re.search(r'\d', candidate) and
                candidate.lower() not in {'resume', 'curriculum vitae'}):
            return candidate
    return 'Candidate'

def _target_role(job_description):
    lines = [line.strip() for line in job_description.splitlines() if line.strip()]
    for line in lines:
        match = re.search(r'(?:role|position|title)\s*[:\-]\s*(.+)', line, re.IGNORECASE)
        if match:
            return re.split(r'[.!?]', match.group(1))[0].strip()[:90]
    first_sentence = re.split(r'[.!?]', lines[0])[0] if lines else 'Target role'
    return first_sentence[:90]

def analyze_documents(resume_text, job_description, metadata):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    baseline_skills = role_baseline_skills(job_description)
    known_job_skills = {skill['name'].lower() for skill in job_skills}
    job_skills += [skill for skill in baseline_skills if skill['name'].lower() not in known_job_skills]
    resume_keywords = keywords(resume_text)
    job_keywords = keywords(job_description)
    sections = detect_sections(resume_text)
    semantic, model = semantic_similarity(resume_text, job_description)
    scores = score_analysis(resume_skills, job_skills, resume_keywords, job_keywords, sections, semantic)
    top_match = scores['matched_skills'][0] if scores['matched_skills'] else 'the available evidence'
    gap = scores['missing_skills'][0]['name'] if scores['missing_skills'] else 'no single skill gap'
    strengths = []
    if scores['matched_skills']:
        strengths.append(f"Your resume contains {len(scores['matched_skills'])} skills relevant to this role, led by {top_match}.")
    if sections.get('Projects'):
        strengths.append('A projects section was detected, giving the reviewer evidence of applied work.')
    if scores['semantic_similarity'] >= 60:
        strengths.append('The resume language has strong topical alignment with the target description.')
    improvements = []
    if scores['missing_skills']:
        improvements.append(f"{gap} was detected in the job description but not in the resume. Add it only if it reflects genuine experience.")
    elif not job_skills:
        improvements.append('Add a clearer job description with required technologies so the match can be more specific.')
    if not sections.get('Experience'):
        improvements.append('Experience was not detected. Add internships, work, or relevant responsibilities if applicable.')
    improvements.append('Use action verbs and measurable outcomes where you can truthfully support them.')
    learning_plan = []
    for skill in scores['missing_skills']:
        learning_plan.append({
            'skill': skill['name'],
            'category': skill['category'],
            'why': f"{skill['name']} appears in the target role but was not detected in the resume.",
            'proof': f"Build one small project using {skill['name']} and add the truthful project evidence after completing it."
        })
    resume_rewrite = [
        'Keep the skills you can support with real coursework or projects.',
        'Add missing role skills only after you have genuine project or coursework evidence to discuss.',
        'Rewrite project bullets around what you built, which tools you used, and the result you can verify.'
    ]
    role_name = _target_role(job_description)
    role_skill_names = [skill['name'] for skill in job_skills]
    tailored_resume = {
        'notice': 'This is a role-specific resume template. Replace placeholders with your real education, projects, and results.',
        'headline': f'{role_name} | Python | Machine Learning',
        'summary': f'Computer science candidate targeting a {role_name} role, with hands-on evidence in [add your verified tools and projects].',
        'skills': role_skill_names,
        'project_title': f'{role_name} Project | [Your Project Name]',
        'project_bullets': [
            f'Built [what you built] using [verified technologies relevant to {role_name}].',
            'Implemented [specific feature or responsibility] and documented the approach.',
            'Measured [truthful result, evaluation, or learning outcome] where applicable.'
        ],
        'next_step': f'Build one project that demonstrates {scores["missing_skills"][0]["name"] if scores["missing_skills"] else "the role requirements"}, then replace the placeholders with your real evidence.'
    }
    return {
        'metadata': metadata, 'target_role': _target_role(job_description),
        'candidate_name': _candidate_name(resume_text),
        'sections': sections, 'resume_skills': resume_skills, 'job_skills': job_skills,
        'resume_keywords': resume_keywords, 'job_keywords': job_keywords, 'embedding_model': model,
        'strengths': strengths, 'improvements': improvements,
        'learning_plan': learning_plan, 'resume_rewrite': resume_rewrite,
        'tailored_resume': tailored_resume,
        'insight': f"Your strongest detected alignment is {top_match}. The largest detected gap is {gap}.",
        **scores
    }
