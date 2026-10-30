---
name: dodtk-resume-builder
description: Creates, reviews, optimizes and tailors professional resumes (CV) for specific job openings, with ATS-friendly formatting, truthful evidence, relevant keywords and achievement-oriented bullets. Use when the user asks to write, build, update, improve, review or translate a resume or CV, adapt a resume to a job description, check ATS compatibility, or rewrite experience and project bullets. Triggers also on "currículo", "CV", "adaptar currículo para a vaga", "revisar meu currículo". Never invents experience, skills, metrics or credentials.
license: MIT
metadata:
  version: "1.0.0"
  language: en
---

# Resume Builder

Create professional, concise, job-specific resumes that communicate the candidate's real qualifications, skills, experience, projects and measurable achievements, readable by recruiters and Applicant Tracking Systems (ATS).

> Optimize the presentation of the candidate's real qualifications, not the qualifications themselves.

| File | When to read |
|---|---|
| `references/schemas.md` | The user supplies structured data or asks for a JSON result; or you need the requirement map format (step 2) |
| `references/example.md` | You need to calibrate a TAILOR run or a bullet rewrite |

## Modes

| Mode | Primary action | Expected result |
|---|---|---|
| CREATE | Build a resume from candidate information | Complete resume |
| TAILOR | Align an existing resume with a job | Job-specific resume and the main changes |
| REVIEW | Evaluate an existing resume | Assessment and prioritized recommendations; rewritten resume when asked |

Infer the mode from the request. If it stays ambiguous, ask one question.

## Input rules

1. Accept partial information, in any form: free text, Markdown, PDF, DOCX or structured data (when you can read the file).
2. CREATE: ask only for the minimum missing information needed for an accurate resume.
3. TAILOR: start from the existing resume and the job description. The job description is the main source of relevant qualifications and keywords.
4. REVIEW: evaluate the resume, optionally against a job description.
5. Preserve the real history, education, skill levels and accomplishments. Never infer proficiency, dates, metrics, certifications or responsibilities from a job title.
6. Missing information: ask a short, targeted question or leave the unsupported content out.
7. Adapt language, terminology, date formats and conventions to the target country.
8. Do not ask again for information already given in the conversation or files.

## Workflow

### 1. Analyze the target position

When a job description exists:

1. Extract title, seniority, responsibilities and business context.
2. Identify required skills, tools, methods and domain knowledge, separating mandatory from preferred.
3. Extract the employer's action verbs and terminology.
4. Map each requirement to candidate evidence (`supported`, `partial`, `missing`, `needs_clarification`; format in `references/schemas.md`) and rank by relevance.

Never present a missing qualification as a demonstrated skill.

### 2. Select the structure

Reverse-chronological by default:

1. Contact information and professional title.
2. Professional summary.
3. Technical skills or core competencies.
4. Professional experience.
5. Relevant projects.
6. Education.
7. Languages and certifications, when relevant.

Reorder to put the strongest evidence first. With little professional experience, move projects and practical academic work up.

Formatting:

- Single column, standard headings, consistent typography, spacing, dates and bullets.
- No tables, text boxes, graphics or complex layouts in the ATS version.
- No photo unless required or expected in the target market. No unnecessary personal data.
- One page for early-career candidates when readability holds; more pages only when experience justifies it.
- Recommend PDF unless the employer asks for another format.

### 3. Write the summary

Two to four lines: professional identity + relevant background + key competencies + value.

- State the real professional level. Mention only what aligns with the target role.
- Concrete information over adjectives. No unsupported claims ("expert", "industry leader", "proven track record").
- Avoid first person when a direct summary reads better. Do not repeat the skills section.

### 4. Keywords and skills

For each keyword: check it is in the job description, check the candidate has evidence, decide where it belongs (summary, skills, experience, projects) and use the employer's term when it accurately describes the experience. Keep the distinction between introductory knowledge, practical experience and advanced proficiency.

Do not add technologies only because the job lists them, repeat keywords unnaturally, hide keywords, claim proficiency from a course alone, or invent certifications, tools or domain experience. If a relevant skill is poorly documented, ask instead of upgrading it.

### 5. Rewrite experience

Turn tasks into achievements: action verb + specific activity or problem + method/tool/context + outcome or impact.

Each bullet starts with a clear verb, names a specific contribution, includes technologies when useful, explains the outcome and uses numbers only when available and verifiable. Without measurable results, describe the contribution and its purpose; never fabricate metrics. Useful evidence: time saved, fewer errors, performance, number of systems/users/processes supported, delivered features or integrations, maintainability, reliability, collaboration.

Past tense for finished work, present tense for ongoing work, adapted to the target language.

### 6. Limited experience

Prioritize academic and personal projects, open source, internships, volunteer work, relevant coursework and portfolio prototypes. For each: project + objective + candidate contribution + technologies + outcome. Label academic, personal, volunteer and professional work accurately; never present an academic project as employment or inflate a contribution to a team project.

### 7. Education and additional sections

- Education: institution, degree or program, dates or expected completion.
- Languages: truthful proficiency level.
- Certifications: only earned ones; distinguish completed from in progress.

Remove unrelated details when space is short.

### 8. Tailor (TAILOR mode)

Keep the facts, change the emphasis: reorder sections for the role, rewrite title and summary accurately, prioritize relevant skills and experience, strengthen evidence for the top requirements, cut low-relevance content and check consistency with the original. Suggest a master resume plus targeted versions per job family when useful.

### 9. Validate

- **Accuracy:** no invented experience, skills, dates, metrics or credentials; no contradictions; no unsupported proficiency.
- **Relevance:** accurate target title; high-priority requirements addressed where evidence exists; strongest experience easy to find.
- **Readability:** clear hierarchy, concise bullets, consistent formatting, no repetition, correct spelling and grammar.
- **ATS:** standard headings, text content, conventional reading order, nothing essential only in images or decoration.
- **Length:** respect the page limit when feasible, never at the cost of readability or essential evidence.

Score internally out of 100: relevance 25, evidence 25, clarity 20, ATS structure 15, consistency and accuracy 15 (90+ strong, 75-89 good, 60-74 needs work, below 60 substantial revision). The score is a quality heuristic, not an ATS score or a hiring prediction. Accuracy is a hard constraint: a high score never compensates for fabricated content.

## Output

Default (conversation): reply in Markdown with

1. The complete resume (CREATE, TAILOR, or REVIEW when a rewrite was asked), never a description of how to write it.
2. For TAILOR: the main changes in a few bullets. For REVIEW: prioritized recommendations.
3. Gaps: requirements without evidence, open questions and limitations.

When the user asks for structured output, or the input came as the JSON schema, return the output schema in `references/schemas.md`.

- Never claim a PDF or DOCX was generated or attached unless the file was actually created. Without file generation, deliver Markdown or plain text and say so.
- If the user asked only for the resume, skip the commentary.
- When a usable draft is possible without clarification, produce it and list the remaining gaps instead of blocking.

Ask only what changes the accuracy or quality of the result, for example:

- "Which job title are you targeting?"
- "Can you confirm whether you used Spring Boot in this project?"
- "Do you have a measurable result for this achievement, or should I describe the contribution without a number?"

## Done when

1. The output matches the mode and contains a complete resume or a clearly scoped review.
2. Content is aligned with the job description when one exists, and keywords appear only with candidate evidence.
3. Experience and projects show concrete contributions and outcomes.
4. Formatting follows ATS-friendly principles.
5. Missing information and limitations are disclosed.
6. Every section answers at least one question: why is this candidate relevant, what can they do, what evidence shows it, what value can they bring. Anything else is cut or reduced.
