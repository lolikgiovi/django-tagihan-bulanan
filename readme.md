# Tagihan Bulanan (Monthly Bill Tracker)

A Django-based monthly bill tracking application that helps users manage their recurring bills, set payment reminders, and track payment history.

## Features

- **User Authentication**: Secure login system
- **Bill Management**: Add, edit, and delete monthly bills
- **Payment Tracking**: Mark bills as paid and view payment history
- **Automatic Scheduling**: System automatically schedules the next payment after one is marked as paid
- **Reminder System**: Asynchronous notification system using Huey task queue
- **Responsive UI**: Clean, intuitive interface built with Tailwind CSS

## Tech Stack

- **Backend**: Django 5.2
- **Database**: PostgreSQL
- **Task Queue**: Huey for asynchronous task processing
- **Frontend**: HTML, Tailwind CSS 4.1

## Project Structure

The application consists of three main Django apps:

1. **authentications**: Handles user authentication
2. **bills**: Manages bill information and CRUD operations
3. **transactions**: Tracks payment transactions and manages notifications

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Node.js and npm (for Tailwind CSS)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lolikgiovi/tagihan-bulanan.git
   cd tagihan-bulanan
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating a `.env` file:
   ```
   PG_NAME=your_db_name
   PG_USER=your_db_user
   PG_PASSWORD=your_db_password
   PG_HOST=localhost
   PG_PORT=5432
   ```

4. Install frontend dependencies:
   ```bash
   npm install tailwindcss @tailwindcss/cli
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. In a separate terminal, compile and watch CSS:
   ```bash
   npm run tw
   ```

8. In another terminal, start the Huey worker process:
   ```bash
   python manage.py run_huey
   ```

### Demo Login

You can test the application using these credentials:

```
Username: testuser
Password: test12345
```