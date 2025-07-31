# ☕ Coffee Counter

A simple yet feature-rich coffee consumption tracker with both CLI and web interfaces.

## Features

- **CLI Interface**: Simple command-line tool for quick coffee logging
- **Web Interface**: Modern web dashboard with authentication
- **Data Visualization**: Charts, heatmaps, and statistics
- **Data Management**: Export/import functionality (CSV)
- **Session Tracking**: Track coffee consumption per session
- **Docker Support**: Easy deployment with containerization
- **Security**: Authentication, CSRF protection, and rate limiting

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ColorfulCookie/coffee-counter.git
   cd coffee-counter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # For development
   pip install -r requirements-dev.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

4. **Run the CLI tool**
   ```bash
   python coffee.py
   ```

5. **Run the web server**
   ```bash
   python coffee_server.py
   ```
   Navigate to `http://localhost:5000` in your browser.

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t coffee-counter .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     -p 5000:5000 \
     -e COFFEE_USERNAME=your-username \
     -e COFFEE_PASSWORD=your-secure-password \
     -e FLASK_SECRET_KEY=your-secret-key \
     -v coffee_data:/data \
     coffee-counter
   ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `COFFEE_USERNAME` | Web interface username | `admin` | No |
| `COFFEE_PASSWORD` | Web interface password | `password` | No |
| `FLASK_SECRET_KEY` | Flask session secret | Auto-generated | Recommended |
| `COFFEE_DB_NAME` | Database filename | `coffee_log.db` | No |
| `DATABASE_PATH` | Full database path | `./coffee_log.db` | No |
| `FLASK_DEBUG` | Enable debug mode | `false` | No |

### Security Considerations

⚠️ **Important**: Change the default credentials in production!

- Set `COFFEE_USERNAME` and `COFFEE_PASSWORD` environment variables
- Set a strong `FLASK_SECRET_KEY` (32+ random characters)
- Use HTTPS in production
- Consider setting up a reverse proxy with additional security headers

## API Documentation

The web interface provides a REST API for coffee tracking:

### Authentication
All API endpoints require authentication via the web interface login.

### Endpoints

- `GET /api/coffees` - Retrieve all coffee entries
- `POST /api/coffees` - Log a new coffee entry
- `PUT /api/coffees/<id>` - Update a coffee entry
- `DELETE /api/coffees/<id>` - Delete a coffee entry
- `GET /api/session-counter` - Get current session counter
- `POST /api/session-counter` - Reset session counter
- `GET /api/export` - Export data as CSV
- `POST /api/import` - Import data from CSV

## Development

### Running Tests

```bash
python test_coffee.py
# or with pytest
pytest
```

### Code Quality

```bash
# Linting
flake8 .

# Code formatting
black .
```

### Project Structure

```
coffee-counter/
├── coffee.py              # CLI interface
├── coffee_server.py       # Web server and API
├── templates/             # HTML templates
│   ├── coffee.html       # Main dashboard
│   └── login.html        # Login page
├── test_coffee.py        # Unit tests
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── Dockerfile           # Container configuration
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Database Schema

The application uses SQLite with the following tables:

### `coffee_entries`
- `id` (INTEGER PRIMARY KEY) - Unique entry identifier
- `timestamp` (TEXT) - When the coffee was logged (YYYY-MM-DD HH:MM:SS)

### `session_counter`
- `id` (INTEGER PRIMARY KEY) - Always 1
- `count` (INTEGER) - Current session counter value

## Windows Usage

For Windows users, you can use the included batch file:

```cmd
coffee.bat
```

This will run the CLI tool with proper directory handling.

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Install dependencies: `pip install -r requirements.txt`

2. **Database permission errors**
   - Ensure the application has write permissions to the database directory
   - Check the `DATABASE_PATH` environment variable

3. **Web interface not accessible**
   - Check if the Flask server is running on the correct port
   - Verify firewall settings for port 5000

4. **Default credentials warning**
   - Set `COFFEE_USERNAME` and `COFFEE_PASSWORD` environment variables

### Getting Help

If you encounter issues:
1. Check the application logs
2. Verify your environment variables
3. Ensure all dependencies are installed
4. Check the GitHub Issues page

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source. Please check the repository for license information.

## Changelog

### Latest Improvements
- ✅ Added comprehensive security features (CSRF, rate limiting)
- ✅ Improved environment variable configuration
- ✅ Enhanced Docker setup with health checks
- ✅ Added proper dependency management
- ✅ Implemented automated testing
- ✅ Added code quality tools
- ✅ Improved error handling and logging
- ✅ Created comprehensive documentation