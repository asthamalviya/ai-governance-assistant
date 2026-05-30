# AI Governance & Knowledge Assistant

A cloud-based AI assistant that enables document upload, AI-powered summarisation, and contextual question-answering — with built-in governance, auditing, and secure architecture.

## Features

- **Document Upload** — Upload PDF, TXT, and DOCX files to secure S3 storage with server-side encryption
- **AI Summarisation** — Generate concise summaries of uploaded documents using OpenAI
- **Contextual Q&A** — Ask questions about your documents and get answers grounded in the content
- **Audit Logging** — All interactions are logged for governance and compliance
- **Infrastructure as Code** — Full AWS infrastructure defined in Terraform
- **CI/CD Pipeline** — Automated testing, linting, and Docker builds via GitHub Actions

## Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Backend        | Python, FastAPI, Uvicorn            |
| AI             | OpenAI GPT (gpt-3.5-turbo)         |
| Storage        | AWS S3 (encrypted, versioned)       |
| Infrastructure | Terraform, AWS (S3, IAM, CloudWatch)|
| Frontend       | HTML, CSS, JavaScript               |
| CI/CD          | GitHub Actions, Docker              |
| Testing        | Pytest, HTTPX                       |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── routes/              # API endpoints (upload, summarise, ask, health)
│   │   ├── services/            # AI and storage service layers
│   │   └── utils/               # Configuration and logging
│   ├── tests/                   # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html               # Web UI
│   ├── styles.css
│   └── app.js
├── infrastructure/
│   └── terraform/               # AWS infrastructure definitions
└── .github/
    └── workflows/ci.yml         # CI pipeline
```

## Getting Started

### Prerequisites

- Python 3.12+
- AWS account with S3 access
- OpenAI API key
- Terraform (for infrastructure provisioning)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/asthamalviya/ai-governance-assistant.git
   cd ai-governance-assistant
   ```

2. **Set up the backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your values:
   #   OPENAI_API_KEY=your-key
   #   S3_BUCKET_NAME=your-bucket
   #   AWS_REGION=eu-west-1
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open the frontend:**
   Open `frontend/index.html` in your browser.

### Running Tests

```bash
pip install pytest httpx
pytest backend/tests/ -v
```

### Docker

```bash
docker build -t ai-governance-assistant ./backend
docker run -p 8000:8000 --env-file backend/.env ai-governance-assistant
```

## API Endpoints

| Method | Endpoint       | Description                     |
|--------|----------------|---------------------------------|
| GET    | `/health`      | Health check                    |
| POST   | `/upload`      | Upload a document to S3         |
| POST   | `/summarise`   | Generate AI summary of document |
| POST   | `/ask`         | Ask a question about a document |

## Infrastructure

The Terraform configuration provisions:

- **S3 Bucket** — Encrypted, versioned, with public access blocked
- **IAM Roles** — Least-privilege access policies
- **CloudWatch** — Monitoring and logging

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

## CI/CD

The GitHub Actions pipeline runs on every push and PR to `main`:

1. Lints the backend with Ruff
2. Runs the test suite with Pytest
3. Builds and verifies the Docker image

## License

This project is for educational and demonstration purposes.
