# devboard-email

Email microservice for the Devboard platform. Handles sending transactional emails using SMTP and Jinja2 HTML templates. Protected by a shared secret key — not exposed publicly.

## Stack

- **FastAPI** — web framework
- **aiosmtplib** — async SMTP client
- **Jinja2** — HTML email templates

## Environment Variables

Copy `.env.example` to `.env` and fill in the values.

| Variable | Description |
|---|---|
| `SMTP_HOST` | SMTP server host |
| `SMTP_PORT` | SMTP server port |
| `SMTP_USER` | SMTP username |
| `SMTP_PASSWORD` | SMTP password |
| `MAIL_FROM` | Sender email address |
| `EMAIL_SERVICE_SECRET_KEY` | Shared secret key — must match `EMAIL_SERVICE_SECRET_KEY` in devboard-auth |

## Running with Docker

```bash
# Build the image
docker compose up --build -d

# Stop containers
docker compose down
```

## API

Base path: `/email`

All routes (except `/health`) require the header:
```
X-Service-Key: <EMAIL_SERVICE_SECRET_KEY>
```

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/email/send` | Send an email using a template |
| `GET` | `/health` | Health check |

### POST /email/send

**Request body:**

```json
{
  "to": "user@example.com",
  "subject": "Your subject",
  "template": "verification",
  "variables": {
    "key": "value"
  }
}
```

**Available templates:**

| Template | Variables |
|---|---|
| `verification` | `verification_link` |
| `password_reset` | `reset_link` |
