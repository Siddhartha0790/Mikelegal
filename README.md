# email campaign manager

a simple django project for managing subscribers and simulating email campaigns.

## features
- manage subscribers (add/remove) via api
- manage and post email campaigns via api or django admin
- multithreaded dummy email sending (prints to console, no real emails sent)

## setup
1. make sure you have python 3.10+
2. create a `.env` file using this template (smtp settings aren't needed as sending is just simulated):
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```
3. create a venv and install the requirements:
```bash
python -m venv venv
source venv/bin/activate  # on windows: .\venv\Scripts\activate
pip install -r requirements.txt
```
4. run migrations and create an admin user:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## usage
start the local server:
```bash
python manage.py runserver
```

### api routes
- `GET /api/subscribers/` : list active subscribers
- `POST /api/subscribers/` : add a subscriber `{"email": "test@example.com", "first_name": "John"}`
- `POST /api/unsubscribe/` : deactivate a subscriber `{"email": "test@example.com"}`
- `GET /api/campaigns/` : list all campaigns (admin only)
- `POST /api/campaigns/` : create a new campaign (admin only)

### sending campaigns
run the management command to simulate sending out emails scheduled for today. the output will be printed directly to the console instead of sending real emails.
```bash
python manage.py send_daily_campaign
```
