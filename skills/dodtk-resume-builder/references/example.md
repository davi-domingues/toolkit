# Example: TAILOR for an early-career backend role

## Input

```json
{
  "mode": "TAILOR",
  "candidate": {
    "professional_title": "Junior Backend Developer",
    "skills": ["Java", "Spring Boot", "REST APIs", "SQL"],
    "experience": [],
    "projects": [
      {
        "name": "Academic Management System",
        "description": "A system developed for an academic project",
        "technologies": ["Java", "Spring Boot", "SQL"],
        "contributions": ["Implemented REST endpoints"],
        "results": []
      }
    ],
    "education": ["Information Systems undergraduate"]
  },
  "job": {
    "title": "Junior Backend Developer",
    "description": "Develop backend services, APIs, business rules, and database integrations."
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

## Expected behavior

- Highlight Java, Spring Boot, REST APIs and SQL.
- Emphasize the academic project's backend implementation and move Projects above Education.
- Align the summary with the target backend role.
- Do not invent professional employment or quantified results.
- Produce a concise, single-column resume.
- Flag important requirements without candidate evidence (for example "business rules" or "database integrations" beyond SQL usage) as gaps or questions.
- Return the complete resume and the validation results.

## Bullet rewrite

Weak:

- Responsible for generating reports.

Improved (only when the tool and the number come from the candidate):

- Automated recurring reports using Python, reducing manual reporting work by 5 hours per week.
