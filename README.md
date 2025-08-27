# Smart Content Moderator

A FastAPI-based web application for moderating user-generated text and image content using Sightengine and integrated with automated notification workflows (SendGrid). This project was developed as a hands-on internship assignment and demonstrates backend moderation, background task processing, and email alerts.

---

## Features

- **Text Moderation:** Analyze text to detect harmful or inappropriate language using Sightengine.
- **Image Moderation:** Detect nudity, violence, weapons, alcohol, and drugs in image uploads.
- **Automated Email Alerts:** Notify users or moderators via SendGrid when flagged content is detected.
- **Background Processing:** Asynchronous email sending so moderation actions are not delayed.
- **Usage Analytics:** Track moderation requests and outcomes for each user.
- **Security:** Sensitive environment variables, database files, and cache artifacts excluded from version control with `.gitignore`.
- **OpenAPI Docs:** Interactive API docs available via FastAPI.

---

## Setup Instructions

### 1. Clone the Repo

```
git clone https://github.com/YOURUSERNAME/smart-content-moderator.git
cd smart-content-moderator
```

### 2. Create `.gitignore` in the Project Root

```
# Python
__pycache__/
.env
.venv/
venv/
database.db

# Editors
.vscode/

# Misc
*.log
*.pid
*.seed
*.pid.lock
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with:

```
SIGHTENGINE_USER=your_sightengine_user
SIGHTENGINE_SECRET=your_sightengine_secret
SENDGRID_API_KEY=your_sendgrid_api_key
```

**Do not commit `.env`!**

### 5. Run the Application

```
uvicorn app.main:app --reload
```

Visit [http://localhost:8000](http://localhost:8000)

### 6. Access the API Docs

Go to [http://localhost:8000/docs](http://localhost:8000/docs)

---

## How It Works

- Users POST text or image files to the moderation API endpoint.
- Moderation is handled by Sightengine (text/image models).
- Results are logged in the database.
- If content is flagged, an email alert is sent using SendGrid (runs as a FastAPI background task).
- Moderation activity is available through analytics endpoints.

---

## Project Structure

```
app/
  ├── main.py           # FastAPI app and endpoints
  ├── database.py       # DB models & session
  ├── notifications.py  # Email notifications
  ├── moderation.py     # Sightengine integration
  └── ...
.gitignore
.env
requirements.txt
README.md
```

---
## Running with Docker

This project can be run inside a Docker container for easier setup and deployment.

### Build the Docker Image

### Run the Container


### Access the API

Once running, visit [http://localhost:8000](http://localhost:8000) in your browser.

---

Make sure your `.env` file exists with required secrets and is included via `--env-file` to provide environment variables inside the container.

---
## License

This project is for educational and internship demonstration purposes.

---

**Contact:**  
For questions or suggestions, open an issue or contact dku3132@gmail.com .
```

