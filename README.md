# PocketSmart AI

PocketSmart AI is a FastAPI-based generative AI budget recommendation application.

The application provides three major planners:

1. Home Interior Planner
2. Party Budget Planner
3. Jewelry Planner

It includes:

- User registration
- User login
- JWT authentication
- SQLite database
- Recommendation history
- Gemini AI integration
- Jewelry outfit image upload
- Local fallback recommendation engine
- Responsive web interface
- FastAPI Swagger documentation
- Automated API tests

---

## Project Structure

```text
PocketSmart-AI/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
│
├── tests/
├── uploads/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py