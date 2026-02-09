import re
from typing import List, Set

try:
    import spacy
    _HAS_SPACY = True
except Exception:
    spacy = None
    _HAS_SPACY = False

# Minimal skill vocabulary — extend as needed
SKILLS = [
    'python', 'java', 'c++', 'c#', 'javascript', 'react', 'vue', 'angular',
    'django', 'flask', 'sql', 'mysql', 'postgresql', 'mongodb', 'git',
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'nlp', 'tensorflow',
    'pytorch', 'scikit-learn', 'data analysis', 'pandas', 'numpy', 'spark',
    'excel', 'communication', 'problem solving', 'rest api', 'api development'
]

# Simple mapping from skill -> course recommendation (example)
COURSE_RECOMMENDATIONS = {
    'python': ['Complete Python Bootcamp (Udemy)', 'Python for Everybody (Coursera)'],
    'nlp': ['Natural Language Processing with Deep Learning (Coursera)', 'spaCy 101 (spaCy.io)'],
    'react': ['React - The Complete Guide (Udemy)', 'Front-End Web Development (Coursera)'],
    'docker': ['Docker Mastery (Udemy)'],
    'aws': ['AWS Certified Cloud Practitioner (A Cloud Guru)'],
}

# Precompile regex patterns for performance
_SKILL_PATTERNS = [(skill, re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)) for skill in SKILLS]


def _get_spacy_nlp():
    """Lazily load spaCy model if available. Caller must handle None."""
    if not _HAS_SPACY:
        return None
    try:
        # prefer installed small model; if not present, try to load generic 'en'
        try:
            return spacy.load('en_core_web_sm')
        except Exception:
            return spacy.load('en_core_web_sm')
    except Exception:
        return None


def extract_skills(text: str) -> List[str]:
    """Return a sorted list of detected skills from text.

    Uses spaCy (if installed and model available) to extract noun chunks and tokens
    for more robust matching; falls back to regex vocabulary matching.
    """
    found: Set[str] = set()
    if not text:
        return []

    nlp = _get_spacy_nlp()
    if nlp is not None:
        try:
            doc = nlp(text)
            # check tokens and noun chunks against known skills
            for token in doc:
                tok = token.text.lower()
                for skill in SKILLS:
                    if skill in tok or tok in skill:
                        found.add(skill)
            for chunk in doc.noun_chunks:
                ch = chunk.text.lower()
                for skill in SKILLS:
                    if skill in ch:
                        found.add(skill)
            # also check entities
            for ent in doc.ents:
                entt = ent.text.lower()
                for skill in SKILLS:
                    if skill in entt:
                        found.add(skill)
            return sorted(found)
        except Exception:
            # fall through to regex fallback
            pass

    # regex fallback
    for skill, pattern in _SKILL_PATTERNS:
        if pattern.search(text):
            found.add(skill)
    return sorted(found)


def recommend_courses(missing_skills: List[str]) -> dict:
    """Return course recommendations for each missing skill if available."""
    recs = {}
    for s in missing_skills:
        recs[s] = COURSE_RECOMMENDATIONS.get(s, [])
    return recs
