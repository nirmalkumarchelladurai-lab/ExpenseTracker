# Expense Tracker

A simple, robust expense tracker application built with Python (Flask) and Supabase.

## Features

- **User Authentication**: Secure email/password login and registration via Supabase Auth.
- **Expense Management**: Add, edit, and delete expenses.
- **Dashboard**: View all expenses in a list.
- **Filtering & Search**: Filter by category, date range, and search by description.
- **Summary**: View total expenses breakdown by category.
- **Responsive Design**: Works on mobile and desktop.

## Setup Instructions

### Prerequisites

- Python 3.8+
- A [Supabase](https://supabase.com/) account.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd expense_tracker
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and fill in your Supabase credentials:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SECRET_KEY=your_flask_secret_key
```

### 4. Database Setup

Run the following SQL in your Supabase SQL Editor to create the necessary table and policies:

```sql
-- Create a table for expenses
create table expenses (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users not null,
  amount numeric not null,
  category text not null,
  description text,
  date date not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable Row Level Security (RLS)
alter table expenses enable row level security;

-- Create policies
create policy "Users can view their own expenses" on expenses
  for select using (auth.uid() = user_id);

create policy "Users can insert their own expenses" on expenses
  for insert with check (auth.uid() = user_id);

create policy "Users can update their own expenses" on expenses
  for update using (auth.uid() = user_id);

create policy "Users can delete their own expenses" on expenses
  for delete using (auth.uid() = user_id);
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Deployment

### Heroku

1.  Create a `Procfile` (already included):
    ```
    web: gunicorn app:app
    ```
2.  Push to Heroku.
3.  Set environment variables in Heroku Dashboard.

### Render

1.  Create a `render.yaml` (already included) or connect your repo.
2.  Set environment variables in Render Dashboard.
