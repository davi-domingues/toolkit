# Schemas

Use these schemas when the user supplies structured data or asks for a structured (JSON) result. In a normal conversation, accept free text, Markdown or files and reply in Markdown (see "Output" in `SKILL.md`).

## Input schema

Every field is optional except `mode`, which can also be inferred from the request.

```json
{
  "mode": "CREATE | TAILOR | REVIEW",
  "candidate": {
    "name": "Full name",
    "contact": {
      "email": "Professional email",
      "phone": "Phone number",
      "location": "City, State, Country",
      "linkedin": "LinkedIn URL",
      "portfolio": "Portfolio or GitHub URL"
    },
    "professional_title": "Target professional title",
    "summary": "Existing professional summary",
    "experience": [
      {
        "company": "Company name",
        "position": "Job title",
        "start_date": "YYYY-MM",
        "end_date": "YYYY-MM or Present",
        "responsibilities": [],
        "achievements": [],
        "technologies": []
      }
    ],
    "education": [],
    "skills": [],
    "projects": [
      {
        "name": "Project name",
        "description": "Project description",
        "technologies": [],
        "contributions": [],
        "results": []
      }
    ],
    "languages": [],
    "certifications": []
  },
  "job": {
    "title": "Target job title",
    "company": "Company name",
    "description": "Full job description",
    "requirements": [],
    "preferred_qualifications": []
  },
  "preferences": {
    "language": "en-US",
    "country": "US",
    "format": "PDF",
    "max_pages": 1,
    "style": "ATS-friendly",
    "output_type": "resume"
  }
}
```

## Requirement map (internal)

Built in step 2, one entry per job requirement:

```json
{
  "requirement": "REST API development",
  "priority": "high",
  "candidate_evidence": [
    "Developed REST endpoints in a documented project"
  ],
  "match_status": "supported",
  "resume_action": "Highlight relevant project or experience"
}
```

`match_status`:

- **supported:** explicitly supported by candidate information.
- **partial:** related experience exists, but the full requirement is not demonstrated.
- **missing:** no evidence was supplied.
- **needs_clarification:** available information is insufficient to decide.

## Output schema (structured mode)

```json
{
  "status": "success | needs_input | partial",
  "mode": "CREATE | TAILOR | REVIEW",
  "resume": {
    "professional_title": "Target title",
    "content": "Complete resume in Markdown or plain text",
    "language": "en-US",
    "format_recommendation": "PDF",
    "estimated_pages": 1
  },
  "job_alignment": {
    "strong_matches": [],
    "partial_matches": [],
    "missing_requirements": [],
    "keywords_included": []
  },
  "validation": {
    "factual_consistency": "passed | needs_review",
    "ats_readability": "passed | needs_review",
    "grammar": "passed | needs_review",
    "formatting": "passed | needs_review"
  },
  "clarification_questions": [],
  "recommendations": [],
  "limitations": []
}
```

- `needs_input`: essential information prevents an accurate result.
- `partial`: a useful draft exists but important details remain unresolved.
- `success`: the deliverable is complete and its validations were performed.
- `resume.content` holds the complete resume, never a description of how to write one.
