# e-Tutor AI – Setup Instructions

## 1. Clone the repository
```bash
git clone <repository-url>
```

## 2. Create the `.env` file
Inside the `backend_ai` directory, create a `.env` file.  
You can copy the structure from `.env.example` and fill in the required data such as API keys, secrets, etc.
```bash
cd backend_ai
cp .env.example .env
```

## 3. Build and start the application
```bash
# Build Docker images and start containers
docker compose up --build
```

The application will be available at: [http://localhost:8000](http://localhost:8000)  
API documentation: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## 4. Additional services
- **Celery Worker**: Handles background tasks
- **Flower**: Celery monitoring dashboard at [http://localhost:5555](http://localhost:5555)
- **PostgreSQL**: Database running on port 5433
- **Redis**: Cache and message broker

---

## 5. Admin Access

### Default Admin Account
The application automatically creates a default admin account during startup:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `admin123`

You can customize these credentials by setting the following environment variables in your `.env` file:
```bash
DJANGO_SUPERUSER_USERNAME=your_admin_username
DJANGO_SUPERUSER_EMAIL=your_admin@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password
```

### Manual Superuser Creation
If you want to create additional admin users manually:
1. Open a shell inside the running container:
```bash
docker compose exec backend_ai python manage.py shell
```
2. Or create superuser directly:
```bash
docker compose exec backend_ai python manage.py createsuperuser
```

### Admin Panel Access
Access the Django admin panel at: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 6. Development Commands

```bash
# View logs
docker compose logs -f

# Access Django shell
docker compose exec backend_ai python manage.py shell

# Run migrations manually
docker compose exec backend_ai python manage.py migrate

# Stop all services
docker compose down

# Rebuild and restart
docker compose up --build
```

## 7. Environment Configuration

### Required Environment Variables
Copy `.env.example` to `.env` and update the values:

```bash
# Basic Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
ALLOWED_HOSTS=*

# Authentication
JWT_SECRET=your-jwt-secret

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=backend_ai_dev

# Flower monitoring
FLOWER_BASIC_AUTH=username:password

# Admin account
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

# Setup automation
RUN_MIGRATIONS=true
CREATE_SUPERUSER=true
```

**Important:** Change all secret keys and passwords for production deployment!