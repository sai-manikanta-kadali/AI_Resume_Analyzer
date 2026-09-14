def score_analysis(resume_skills, job_skills, resume_keywords, job_keywords, sections, semantic):
    resume_names = {item['name'].lower() for item in resume_skills}
    job_names = {item['name'].lower() for item in job_skills}
    matched = sorted([item['name'] for item in job_skills if item['name'].lower() in resume_names])
    missing = sorted([item for item in job_skills if item['name'].lower() not in resume_names], key=lambda item: item['name'])
    skill_match = round((len(matched) / len(job_names)) * 100, 1) if job_names else 0
    matched_keywords = sorted(set(job_keywords) & set(resume_keywords))
    keyword_match = round((len(matched_keywords) / len(set(job_keywords))) * 100, 1) if job_keywords else 0
    expected = ['Contact', 'Education', 'Skills', 'Projects', 'Experience', 'Certifications']
    completeness = round(sum(sections.get(item, False) for item in expected) / len(expected) * 100, 1)
    formatting = min(100, round(55 + min(len(resume_keywords), 25) * 1.8 + sum(sections.values()) * 2, 1))
    final = round(skill_match * .4 + keyword_match * .25 + semantic * .2 + completeness * .1 + formatting * .05, 1)
    return {
        'final_score': final, 'skill_match': skill_match, 'keyword_match': keyword_match,
        'semantic_similarity': semantic, 'completeness': completeness, 'formatting': formatting,
        'matched_skills': matched, 'missing_skills': missing, 'matched_keywords': matched_keywords,
        'missing_keywords': sorted(set(job_keywords) - set(resume_keywords)),
        'score_explanation': f'{len(matched)} of {len(job_names)} detected role skills are present; {len(matched_keywords)} of {len(set(job_keywords))} job terms overlap; {sum(sections.get(item, False) for item in expected)} of {len(expected)} expected sections were detected.'
    }
