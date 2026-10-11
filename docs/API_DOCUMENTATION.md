# REST API Documentation

## Base URL
`/api`

### Authentication Endpoints
- `POST /api/auth/register` - Create user account (returns JWT token)
- `POST /api/auth/login` - Authenticate user credentials (returns JWT token)
- `GET /api/auth/me` - Get current user profile [Protected]
- `POST /api/auth/change-password` - Update password [Protected]

### Resume Endpoints
- `POST /api/resumes/upload` - Upload PDF/DOCX file & parse automatically [Protected]
- `GET /api/resumes` - List user uploaded resumes [Protected]
- `GET /api/resumes/{id}` - Fetch single resume detail [Protected]
- `DELETE /api/resumes/{id}` - Delete resume & clean storage [Protected]
- `POST /api/resumes/{id}/analyze` - Trigger/re-run NLP analysis [Protected]
- `GET /api/resumes/{id}/analysis` - Retrieve analysis scores & extracted sections [Protected]

### Job Matching & Recommendations
- `POST /api/job-match` - Compare resume against custom job title & description [Protected]
- `GET /api/job-match/history` - Retrieve candidate match history [Protected]
- `GET /api/recommendations` - Get recommended job roles with technical rationale [Protected]
- `GET /api/skill-gap?target_role={role}` - Retrieve skill gap comparison & project ideas [Protected]

### PDF Reports
- `POST /api/reports/{resume_id}/pdf` - Generate and download PDF analysis report [Protected]
