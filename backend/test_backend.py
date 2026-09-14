import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from analyzer import analyze_documents
from database import delete_analysis, get_analysis, init_db, list_analyses, save_analysis
from nlp import detect_sections, extract_skills
from resume_parser import extract_text


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.resume = '''Alex Morgan\nalex@example.com\n\nSUMMARY\nPython developer.\n\nEDUCATION\nB.Tech Computer Science\n\nSKILLS\nPython, Flask, SQL, Git\n\nPROJECTS\nBuilt a Flask API.'''
        self.job = 'Role: Python Developer. Looking for Flask, REST APIs, SQL, Git, and Docker.'

    def test_skills_and_sections_are_data_driven(self):
        self.assertIn({'name': 'Python', 'category': 'Programming'}, extract_skills(self.resume))
        sections = detect_sections(self.resume)
        self.assertTrue(sections['Education'])
        self.assertTrue(sections['Projects'])

    def test_analysis_extracts_identity_and_gaps(self):
        result = analyze_documents(self.resume, self.job, {'filename': 'resume.docx'})
        self.assertEqual(result['candidate_name'], 'Alex Morgan')
        self.assertEqual(result['target_role'], 'Python Developer')
        self.assertIn('Flask', result['matched_skills'])
        self.assertIn('Docker', [skill['name'] for skill in result['missing_skills']])
        self.assertGreaterEqual(result['final_score'], 0)
        self.assertLessEqual(result['final_score'], 100)

    def test_database_round_trip(self):
        with tempfile.NamedTemporaryFile(suffix='.db') as database:
            init_db(database.name)
            payload = analyze_documents(self.resume, self.job, {'filename': 'resume.pdf'})
            payload['analysis_date'] = '2026-09-11T00:00:00+00:00'
            analysis_id = save_analysis(database.name, payload)
            self.assertEqual(len(list_analyses(database.name)), 1)
            self.assertEqual(get_analysis(database.name, analysis_id)['candidate_name'], 'Alex Morgan')
            self.assertTrue(delete_analysis(database.name, analysis_id))


class ParserTests(unittest.TestCase):
    def test_unsupported_file_is_rejected(self):
        with self.assertRaises(ValueError):
            extract_text('resume.txt', io.BytesIO(b'plain text').read())


if __name__ == '__main__':
    unittest.main()