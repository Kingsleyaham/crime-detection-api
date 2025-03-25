# Crime Detection App

An Api for a crime detection app

## 🚀 Project Structure
```
.
├── app/
│   ├── main.py          # FastAPI entry point
│   └── ...             # Other modules
├── Dockerfile           # Docker image definition
├── compose.yaml         # Docker Compose configuration
├── .dockerignore        # Files to ignore in Docker build
└── README.md            # Project documentation
```

## 🛠️ Prerequisites
- Docker
- Docker Compose

## 📦 Setup and Run
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <project_folder>
   ```

2. Create a `.env` file for environment variables (e.g., database credentials):
   ```bash
   cp .env.example .env
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Access the FastAPI app at:
   ```
   http://localhost:8000
   ```

## 📊 Useful Commands
- Stop containers: `docker-compose down`
- View logs: `docker-compose logs -f`
- Rebuild: `docker-compose up --build`

## 📄 Environment Variables
Ensure your `.env` file contains:
```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
HOST_PORT=8000
HOST_POSTGRES_PORT=5432
```

## 🧪 Running Tests
If you have tests configured, run them inside the container:
```bash
docker-compose exec web pytest
```

## 📚 Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

---

Happy coding! ✨
