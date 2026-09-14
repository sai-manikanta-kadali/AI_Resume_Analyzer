# Resumate AI Viva Guide

1. **What is the project?** A local web application that compares a resume with a target job description and explains the alignment.
2. **Why build it?** Students often receive generic resume advice; this gives role-specific, evidence-based feedback.
3. **What is NLP?** Natural Language Processing is the analysis of human language by software.
4. **Why use NLP?** Resumes and job descriptions are text, so NLP can extract terms, sections, and relationships.
5. **What is semantic similarity?** A numerical estimate of how closely two pieces of text discuss related content.
6. **What are embeddings?** Numeric vector representations of text that make comparison possible.
7. **What is cosine similarity?** A vector-angle comparison. A value closer to 1 means the texts point in a more similar direction.
8. **Why sentence-transformers?** They provide strong sentence-level embeddings. This version keeps a TF-IDF baseline local and explainable.
9. **What is resume parsing?** Extracting readable text and structure from PDF or DOCX files.
10. **How are skills extracted?** A normalized, categorized catalog is matched against both documents using boundary-aware patterns.
11. **How is the score calculated?** Skill 40%, keywords 25%, semantic similarity 20%, completeness 10%, formatting 5%.
12. **Why is it explainable?** Every component has a visible percentage and a plain-language count or rule.
13. **Why Flask?** It is small, clear, and suitable for REST APIs in Python.
14. **Why React?** It makes the interactive workflow and result dashboard component-based.
15. **Why SQLite?** It is serverless, local, and enough for a college demonstration.
16. **Limitations?** Image-only files, unusual layouts, and skills outside the dictionary can reduce detection quality.
17. **Poor formatting?** Text extraction may be incomplete; the UI reports what was not detected rather than claiming it is absent.
18. **How improve it?** Add OCR, more aliases, a cached transformer model, and richer entity extraction.
19. **Is it an official ATS?** No. It is an ATS-style compatibility estimate, not an official vendor score.
20. **What makes it AI?** It processes natural language, extracts features, computes vector similarity, and generates data-dependent insights.
