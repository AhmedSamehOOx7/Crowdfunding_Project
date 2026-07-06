# Crowdfunding Platform

A modern, professional crowdfunding platform built with Django 6, featuring campaign creation, donation system, and responsive design.

## Features

- **User Authentication & Profiles**: Register, login, logout, edit profiles with avatars
- **Campaign Management**: Create, edit, delete campaigns with categories
- **Donation System**: Donate to campaigns with real-time progress updates
- **Search & Filtering**: Search campaigns, filter by category, sort by newest/most funded/ending soon
- **Dashboard**: User dashboard to manage own campaigns and view donation history
- **Responsive Design**: Bootstrap 5 interface, mobile-friendly
- **Admin Panel**: Django admin for managing users, campaigns, donations, and categories

## Technology Stack

- **Backend**: Django 6
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production-ready configuration included)
- **File Storage**: Local file storage (development), Cloudinary integration (production-ready)
- **Authentication**: Django Authentication System
- **APIs**: REST Framework + SimpleJWT (configured and ready)

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd crowdfunding
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Seed initial categories**:
   ```bash
   python manage.py seed_categories
   ```

5. **Create a superuser (optional, for admin access)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Open your browser** and visit `http://127.0.0.1:8000/`

## Usage

### For Fundraisers
1. Register and login
2. Click "Start Campaign" to create a new fundraising campaign
3. Fill in campaign details, add a cover image, and set funding goal and duration
4. Manage your campaigns from the dashboard

### For Donors
1. Browse campaigns on the homepage or campaigns page
2. Use search and filters to find campaigns you care about
3. Click on a campaign to view details and make a donation

## Project Structure

```
crowdfunding/
├── accounts/                 # User authentication and profiles
│   ├── models.py             # Custom User model
│   ├── forms.py              # Registration and profile forms
│   ├── views.py              # Authentication and profile views
│   └── urls.py               # Account URLs
├── projects/                 # Campaign and donation functionality
│   ├── models.py             # Campaign, Donation, Category models
│   ├── forms.py              # Campaign and donation forms
│   ├── views.py              # Campaign and home views
│   ├── urls.py               # Project URLs
│   └── management/           # Custom management commands (seed_categories)
├── crowdfunding/             # Project configuration
│   ├── settings.py           # Main settings file
│   └── urls.py               # Main URL configuration
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   ├── accounts/             # Account templates
│   └── projects/             # Campaign templates
├── static/                   # Static files (CSS, JS, images)
└── manage.py                 # Django management script
```

## Database Models

### User
- `first_name`, `last_name`, `email`, `password`
- `mobile_phone` (validated Egyptian phone number format)
- `avatar` (profile picture)
- `created_at`

### Category
- `name`
- `slug`
- `icon` (Font Awesome icon class)

### Campaign
- `owner` (ForeignKey to User)
- `title`
- `short_description`
- `story`
- `category` (ForeignKey to Category)
- `goal_amount`
- `raised_amount`
- `start_date`, `end_date`
- `cover_image`
- `is_featured`
- `created_at`, `updated_at`

### Donation
- `donor` (ForeignKey to User)
- `campaign` (ForeignKey to Campaign)
- `amount`
- `donated_at`

## Configuration (for Production)

1. **Environment Variables**: Copy `.env.example` to `.env` and fill in your values
2. **Database**: Configure PostgreSQL settings in `settings.py`
3. **File Storage**: Set up Cloudinary for media storage
4. **Secret Key**: Use a strong, unique secret key
5. **Debug**: Set `DEBUG=False` in production

## Deployment Guide (Railway/Render)

1. **Push your code to a GitHub repository**
2. **Create an account on Railway/Render**
3. **Create a new web service**
4. **Connect your GitHub repo**
5. **Configure environment variables**:
   - `DATABASE_URL` (from Railway/Render Postgres)
   - `SECRET_KEY`
   - `DEBUG=False`
6. **Add a build command**:
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py seed_categories
   ```
7. **Add a start command**:
   ```bash
   gunicorn crowdfunding.wsgi
   ```
8. **Deploy!**

## License

MIT
