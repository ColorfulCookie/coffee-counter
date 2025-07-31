# ☕ Coffee Counter

A simple coffee consumption tracker with CLI and web interfaces.

## Features

- **CLI tool** for quick coffee logging
- **Web dashboard** with authentication and data visualization  
- **Export/import** functionality (CSV)
- **Docker support** for easy deployment
- **Security features** including rate limiting and CSRF protection

## Quick Start

### Local Setup

```bash
# Clone and install
git clone https://github.com/ColorfulCookie/coffee-counter.git
cd coffee-counter
pip install -r requirements.txt

# Run CLI tool
python coffee.py

# Run web server (http://localhost:5000)
python coffee_server.py
```

### Docker

```bash
docker build -t coffee-counter .
docker run -d -p 5000:5000 \
  -e COFFEE_USERNAME=your-username \
  -e COFFEE_PASSWORD=your-secure-password \
  coffee-counter
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `COFFEE_USERNAME` | `admin` | Web interface username |
| `COFFEE_PASSWORD` | `password` | Web interface password |
| `FLASK_SECRET_KEY` | Auto-generated | Flask session secret |
| `DATABASE_PATH` | `./coffee_log.db` | Database file location |

### Security

⚠️ **Production Security**: Change default credentials and set a strong `FLASK_SECRET_KEY`

## API Endpoints

All endpoints require web authentication:

- `GET /api/coffees` - Get all entries
- `POST /api/coffees` - Log new coffee
- `GET /api/export` - Export data as CSV
- `POST /api/import` - Import CSV data

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python test_coffee.py

# Lint code  
flake8 .
```