# Cryptocurrency Block Tracker

A FastAPI application mounted on Django that tracks the latest blocks for Bitcoin and Ethereum using BlockChair API.

## Architecture

The application uses FastAPI for the API layer while leveraging Django's ORM and admin interface. This hybrid approach provides:
- Fast API responses with FastAPI
- Robust data management with Django ORM
- Built-in admin interface
- JWT-based authentication

## Tech Stack

- Python 3.10+
- FastAPI
- Django
- Celery (for periodic block fetching)
- Redis (for Celery broker)
- PostgreSQL
- Docker & Docker Compose

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd crypto-block-tracker
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. Create a superuser for Django admin:
```bash
docker-compose run web python manage.py createsuperuser
```

The application will be available at:
- API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/v1/docs

## API Endpoints

### Authentication
- `POST /api/v1/users/register/` - Register new user
- `POST /api/v1/users/login/` - Login and get JWT token
- `POST /api/v1/users/approve/{user_id}/` - Approve user registration
- `GET /api/v1/users/me/` - Get current user info

### Blocks
- `GET /api/v1/blocks/` - List all blocks with pagination
  - Query params:
    - `limit`: Number of results (default: 10)
    - `offset`: Offset for pagination
    - `currency`: Filter by currency name
- `GET /api/v1/blocks/{block_id}/` - Get block by ID
- `GET /api/v1/blocks/search/` - Search blocks by block number
  - Query params:
    - `block_number`: Block number to search
    - `currency`: Filter by currency name
    - `provider`: Filter by block provider

## Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Register a user
2. Approve the user
3. Login to get JWT token
4. Include token in requests:
```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/api/v1/blocks/
```

## Block Fetching

Blocks are fetched automatically every 2 minutes using Celery. The task:
- Fetches latest BTC block from ~~CoinMarketCap~~ BlockChair
- Fetches latest ETH block from BlockChair
- Stores block data with timestamps
- Avoids duplicates

## Project Structure

```
crypto-block-tracker/
├── api/                    # FastAPI application
│   ├── routes/             # API endpoints
│   └── schemas.py          # Pydantic models
├── apps/                   # Django applications
│   └── blocks/             # Blocks app with models
├── core/                   # Django project settings
├── docker/                 # Docker configurations
├── docker-compose.yml
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT

