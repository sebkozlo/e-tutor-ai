
# e-Tutor AI – Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>
```

## 2. Create the `.env` file

Inside the project root directory (where the `manage.py` file is located), create a `.env` file.  
You can copy the structure from `.env.example` and fill in the required data such as API keys, secrets, etc.

```bash
cp .env.example .env
```

## 3. Build Docker images

```bash
docker-compose build
```

## 4. Start the containers

```bash
docker-compose up
```

The application will be available at: [http://localhost:8000](http://localhost:8000)  
API documentation: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

---

## 5. (Optional) Create a Django superuser inside the container

If you want to access the Django admin panel, you need to create a superuser:

1. Open a shell inside the running container:

```bash
docker exec -it backend_ai sh
```

2. Run the following command:

```bash
python manage.py createsuperuser
```

Follow the prompts to provide a username, email, and password.

After that, you can access the Django admin panel at:  
[http://localhost:8000/admin](http://localhost:8000/admin)
