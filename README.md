# devboard-email

**The mail sender.** Other services send it a template name and some values. It builds the HTML email and sends it over SMTP.

- **Port:** `8002`
- **Stack:** FastAPI, aiosmtplib, Jinja2
- **Private:** never expose it to the public internet. Only other DevBoard services call it.

---

## Start here (about 3 minutes)

1. Copy `.env.example` to `.env`.
2. Fill in the SMTP values (see Settings below).
3. Run:

```bash
docker compose up --build -d
```

4. Open `http://localhost:8002/health`. You should see `{"status": "ok"}`.

Or start the whole stack with `setup.bat` in `devboard-infra`.

---

## Send a test email

```bash
curl -X POST http://localhost:8002/email/send/ \
  -H "X-Service-Key: <INTERNAL_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"to":"you@example.com","subject":"Hi","template":"verification","variables":{"verification_link":"http://localhost"}}'
```

---

## Who calls it

| Caller | When | Template |
|---|---|---|
| devboard-auth | A user signs up or asks for a new verify mail | `verification` |
| devboard-auth | A user forgets the password | `password_reset` |
| devboard-work | Someone is added to a team | `team_invitation` |

---

## API

Every route except `/health` needs the header `X-Service-Key: <INTERNAL_API_KEY>`. A wrong key gives `403`.

| Method | Path | What it does |
|---|---|---|
| `POST` | `/email/send/` | Send one email. |
| `GET` | `/health` | Is the service up? |

Body for `POST /email/send/`:

```json
{
  "to": "user@example.com",
  "subject": "Your subject",
  "template": "verification",
  "variables": { "verification_link": "https://..." }
}
```

### Templates

Files live in `app/templates/`. `base.html` is the shared layout.

| Template | Variables you must send |
|---|---|
| `verification` | `verification_link` |
| `password_reset` | `reset_link` |
| `team_invitation` | `team_name`, `inviter_name` |

`app_url` is added automatically from `APP_URL`.

To add a template: put a new `<name>.html` file in `app/templates/`. Nothing else to change.

### Errors

| Problem | What you get |
|---|---|
| Wrong or missing `X-Service-Key` | `403` |
| Template name does not exist | Template-not-found error |
| SMTP server refuses the recipient | Recipient-refused error |
| SMTP server fails | Delivery error |

---

## Settings

Copy `.env.example` to `.env`.

| Variable | What it is |
|---|---|
| `SMTP_HOST` `SMTP_PORT` | Your mail server. Uses STARTTLS. |
| `SMTP_USER` `SMTP_PASSWORD` | Mail server login. |
| `MAIL_FROM` | The "From" address. |
| `INTERNAL_API_KEY` | Shared key. Must match the other services. |
| `APP_URL` | Base URL of the web app, used inside templates. |

---

## Good to know

- **No queue.** If SMTP fails, the caller gets the error. There is no retry inside this service. devboard-work retries team invitations itself, up to 5 times.
- **No database.** Nothing is stored.
