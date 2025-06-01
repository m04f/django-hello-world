# Fitness Colab - Backend API

A Django REST API backend for personalized workout management and AI-powered fitness coaching.

## 🎯 Purpose

Fitness Colab is a comprehensive fitness platform that provides:
- **Personalized Workout Generation**: AI-powered workout recommendations based on user preferences and fitness goals
- **Exercise Database Management**: Comprehensive catalog of exercises, muscles, and equipment
- **User Progress Tracking**: Record and monitor workout sessions and fitness progress
- **Real-time Chat Integration**: AI fitness coaching

## 🛠️ Tech Stack

- **Django 4.2.19** - Web framework
- **Django REST Framework** - REST API
- **Django Channels** - WebSocket support for real-time chat

See `requirements.txt` for complete list of dependencies.

## 🚀 How to Run the Program

### Prerequisites

- Python 3.12+
- Node.js and npm (for frontend integration)

### Option 1: Using Nix (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/m04f/FitTrack-AI
   cd fittrack-ai
   ```

2. **Enter the Nix shell environment**
   ```bash
   nix-shell
   ```
   This will automatically install all Python dependencies and set up the environment.

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

### Option 2: Using Python Virtual Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/m04f/FitTrack-AI
   cd fittrack-ai
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables

The application uses the following environment variables:

- `API_KEY`: OpenAI API key for AI-powered features
- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Django secret key (change for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts for production

### Frontend Integration

The frontend implementation can be found at [FitTrack-AI Frontend](https://github.com/m04f/fittrack-ai-frontend).
