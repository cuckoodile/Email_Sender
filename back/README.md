# Emailer System

This is a Django-based emailer system that allows staff members to send email campaigns to registered members. The system includes features for scheduling emails, tracking delivery status, and handling errors.

## Features

- User registration and management
- Email burst campaigns with multiple recipients
- Email delivery status tracking (sent, failed, not found, connection errors, etc.)
- Asynchronous email sending using Celery
- Scheduled email sending functionality
- Delivery statistics and reporting

## Setup

1. **Environment Variables**: Create a `.env` file in the root directory with the following variables:
   ```
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```
   python manage.py runserver
   ```

6. **Start Redis server** (for Celery):
   - Download and install Redis from https://redis.io/download
   - Start the Redis server (typically runs on localhost:6379)

7. **Start Celery worker** (in a separate terminal):
   ```
   celery -A core worker -l info
   ```

8. **Start Celery beat scheduler** (in another terminal):
   ```
   celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

## API Endpoints

### Authentication
- `POST /api/login/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

### Members (Users)
- `GET /api/members/` - List all members
- `POST /api/members/` - Create a new member
- `GET /api/members/{id}/` - Get specific member
- `PUT /api/members/{id}/` - Update specific member
- `DELETE /api/members/{id}/` - Delete specific member

### Staff Users
- `GET /api/staff/` - List all staff users
- `GET /api/staff/{id}/` - Get specific staff user
- `PUT /api/staff/{id}/` - Update specific staff user
- `DELETE /api/staff/{id}/` - Delete specific staff user

### Non-Staff Members
- `GET /api/non-staff/` - List all non-staff members
- `POST /api/non-staff/` - Create a new non-staff member
- `GET /api/non-staff/{id}/` - Get specific non-staff member
- `PUT /api/non-staff/{id}/` - Update specific non-staff member
- `DELETE /api/non-staff/{id}/` - Delete specific non-staff member

### Email Bursts
- `GET /api/email-burst/` - List all email bursts
- `POST /api/email-burst/` - Create a new email burst
- `GET /api/email-burst/{id}/` - Get specific email burst
- `PUT /api/email-burst/{id}/` - Update specific email burst
- `DELETE /api/email-burst/{id}/` - Delete specific email burst
- `POST /api/email-burst/{id}/send/` - Send the email burst to all recipients
- `POST /api/email-burst/{id}/schedule/` - Schedule an email burst
- `GET /api/email-burst/{id}/stats/` - Get delivery statistics for an email burst

### Test Endpoint
- `GET /api/test/emailer/` - Test if the emailer is properly configured

## Usage

1. Register members/users through the API
2. Create an email burst with subject, body, and select recipients
3. Send the email burst immediately using `POST /api/email-burst/{id}/send/`
4. Or schedule the email burst for later using `POST /api/email-burst/{id}/schedule/`
5. Check delivery statistics using `GET /api/email-burst/{id}/stats/`

## Sample Data

To create sample data for testing:
```
python manage.py create_sample_data
```

To seed the database with initial data (2 staff users, 10 members, 2 emails):
```
python manage.py seed_database
```

To view the seeded data:
```
python manage.py show_seeded_data
```

## Error Handling

The system tracks various delivery statuses:
- `sent`: Email was successfully sent
- `failed`: General failure
- `not_found`: Recipient email not found
- `connection_error`: Connection to SMTP server failed
- `other_error`: Other errors occurred

## Security

- JWT authentication is required for most endpoints
- Sensitive information (email credentials) is stored in environment variables
- Access to email sending is restricted to authenticated users