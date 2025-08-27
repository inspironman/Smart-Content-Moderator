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
git clone https://github.com/inspironman/Smart-Content-Moderator.git
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

# API Endpoint: Moderate Text

**Method:** POST  
**URL:** [http://127.0.0.1:8000/api/v1/moderate/text](http://127.0.0.1:8000/api/v1/moderate/text)  

---

### Description

This endpoint is designed to classify and moderate text content submitted by users. It accepts a JSON payload containing an email address and the text to be analyzed.

---

### Request Parameters

The request body must be in JSON format and include the following parameters:

| Parameter | Type   | Description                         |
|-----------|--------|-------------------------------------|
| email     | string | The email address of the user submitting the text. |
| text      | string | The text content that needs to be moderated.       |

---

### Example Request Body
{
"email": "user@example.com",
"text": "Sample text to moderate."
}


---

### Expected Response

Upon successful processing, the API will return a JSON response with the following structure:

| Field          | Type    | Description                                  |
|----------------|---------|----------------------------------------------|
| classification | string  | The classification result of the moderated text. |
| confidence     | number  | A confidence score indicating the reliability of the classification. |
| reasoning      | string  | An explanation of the classification result. |

---

### Example Response

{
"classification": "profanity",
"confidence": 0.95,
"reasoning": "Content flagged as profanity with confidence 0.95"
}

# API Endpoint: Moderate Image

**Method:** POST  
**URL:** [http://127.0.0.1:8000/api/v1/moderate/image](http://127.0.0.1:8000/api/v1/moderate/image)  

---

### Description

This endpoint accepts an image file uploaded by users and analyzes it for inappropriate content such as nudity, weapons, alcohol, or drugs. The image is processed and classified accordingly.

---

### Request Parameters

The request body should be sent as multipart/form-data and include the following parameters:

| Parameter | Type | Description                          |
|-----------|------|------------------------------------|
| email     | string | The email address of the user submitting the image. |
| file      | file  | The image file to be moderated (e.g., PNG, JPEG). |

---

### Example Request (multipart/form-data)

| Key   | Value                     | Type  |
|-------|---------------------------|-------|
| email | user@example.com          | Text  |
| file  | [Select image file here]  | File  |

---

### Expected Response

Upon successful processing, the API will return a JSON response with the following structure:

| Field          | Type    | Description                                  |
|----------------|---------|----------------------------------------------|
| classification | string  | The classification result of the moderated image. |
| confidence     | number  | A confidence score indicating the reliability of the classification. |
| reasoning      | string  | An explanation of the classification result. |

---

### Example Response

{
"classification": "inappropriate",
"confidence": 0.87,
"reasoning": "Nudity detected with confidence 0.87"
}

# API Endpoint: Analytics Summary

**Method:** GET  
**URL:** [http://127.0.0.1:8000/api/v1/analytics/summary](http://127.0.0.1:8000/api/v1/analytics/summary)  

---

### Description

This endpoint provides a summary of moderation analytics for a specified user. It returns counts of different classification categories and the total number of moderation requests made by the user.

---

### Query Parameters

| Parameter | Type   | Description                 |
|-----------|--------|-----------------------------|
| user      | string | The email address of the user for whom the analytics are requested. |

---

### Example Request

GET /api/v1/analytics/summary?user=pacoke5840@namestal.com


---

### Expected Response

Upon successful processing, the API will return a JSON response summarizing the user’s moderation activity.

| Field                | Type    | Description                                    |
|----------------------|---------|------------------------------------------------|
| email                | string  | The email address of the user.                 |
| total_requests       | integer | Total number of moderation requests made.      |
| classification_counts | object  | Count of moderation requests by classification category. |

---

### Example Response

{
"email": "pacoke5840@namestal.com",
"total_requests": 37,
"classification_counts": {
"drug": 1,
"profanity": 15,
"safe": 21
}
}

### Status Codes

| Code               | Description                                                                                                         |
|--------------------|---------------------------------------------------------------------------------------------------------------------|
| **200 OK**         | The request was successful, and the response contains the requested data or confirmation.                          |
| **400 Bad Request** | The request could not be understood or was missing required parameters (e.g., missing or invalid user parameter).    |
| **401 Unauthorized**| Authentication failed or the user does not have permission for the requested action (e.g., missing or invalid API key).|
| **403 Forbidden**   | The request is valid but the server is refusing to fulfill it, often due to insufficient permissions.               |
| **404 Not Found**   | The requested resource or endpoint does not exist.                                                                  |
| **429 Too Many Requests** | The user has sent too many requests in a given amount of time (rate limiting).                                  |
| **500 Internal Server Error** | An unexpected error occurred on the server. Client should retry later or contact support.                    |
| **503 Service Unavailable**  | The server is currently unavailable due to maintenance or overload.                                             |

---

## License

This project is for educational and internship demonstration purposes.

---

**Contact:**  
For questions or suggestions, open an issue or contact dku3132@gmail.com .
```

