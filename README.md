# Email Campaign Manager

A production-ready Django application using Django REST Framework to manage email campaigns, subscribers, and parallelized email dispatch.

## Features

- **Subscribers API**: Endpoints to add and deactivate subscribers.
- **Campaign Administration**: Manage email campaigns through the Django Admin interface.
- **Parallel Dispatcher**: Utilizes Python's `ThreadPoolExecutor` to dispatch emails concurrently for high throughput.
- **Email Utilities**: Sends multi-part (HTML and plaintext) emails dynamically rendered from templates.

## Architecture & Parallel Dispatching

The `CampaignDispatcher` (`campaigns/services/dispatcher.py`) uses a Publish-Subscribe style pattern where campaigns act as publishers and active subscribers as receivers.
To prevent IO blocking during SMTP communication, we use a thread pool to dispatch emails:
1. Fetch all `is_active=True` subscribers.
2. Spin up a `ThreadPoolExecutor` with a configurable pool size (default: 10 worker threads).
3. Distribute email sending tasks among worker threads, allowing parallel network requests.
4. Each thread logs the result (Success/Fail) independently to the `CampaignLog` database model.

*Note: For even higher production volume, a distributed task queue like **Celery** along with Redis/RabbitMQ is recommended (commented within `requirements.txt`).*

## Setup Instructions

### 1. Requirements

Ensure you have Python 3.10+ installed.

### 2. Environment Variables

Create a `.env` file in the root directory (alongside `manage.py`) using the template provided below:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=testuser
EMAIL_HOST_PASSWORD=testpass
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

### 3. Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

### 4. Creating a Superuser

To access the Django Admin panel for managing campaigns:
```bash
python manage.py createsuperuser
```
Follow the prompts to set your username, email, and password. Log into `http://localhost:8000/admin`.

## Running the Application

Start the local server:
```bash
python manage.py runserver
```

### API Endpoints

- **`GET /api/subscribers/`**: List active subscribers.
- **`POST /api/subscribers/`**: Add a subscriber.
  - Body: `{"email": "user@example.com", "first_name": "John"}`
- **`POST /api/unsubscribe/`**: Deactivate a subscriber.
  - Body: `{"email": "user@example.com"}`

### Sending Daily Campaigns

Run the custom management command manually or using a cronjob/scheduler (e.g., Celery beat):

```bash
python manage.py send_daily_campaign
```
This script queries campaigns scheduled for publication today and uses the multithreaded dispatcher to dispatch them. Check console output for a dispatch summary.
