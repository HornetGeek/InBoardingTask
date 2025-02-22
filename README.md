# Booking Management System

## Overview

This project is a comprehensive Booking Management System that integrates multiple services including Odoo, Directus, and a custom FastAPI-based backend. The system allows for creating and managing bookings across different platforms.

## Features

- Create bookings with customer and service details
- Integrate with Odoo for order and invoice management
- Store booking information in Directus
- Flexible booking status tracking
- RESTful API endpoints for booking operations

## Technology Stack

- **Backend**: FastAPI
- **Database**: 
  - Odoo (ERP System)
  - Directus (Headless CMS)
  - PostgreSQL
- **Containerization**: Docker

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app/
│   ├── api/
│   │   ├── models/
│   │   │   └── booking.py
│   │   └── routes/
│   ├── services/
│   │   ├── odoo/
│   │   ├── directus/
│   │   └── calcom/
│   └── core/
│       └── security.py
└── README.md
```

## Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd booking-management-system
   ```

2. Create a `.env` file (optional, docker-compose uses environment variables)
   ```bash
   cp .env.example .env
   ```

3. Build and start the services
   ```bash
   docker-compose up --build
   ```

## API Endpoints

### Create a Booking
- **URL**: `/booking/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "customer_id": 1,
    "service_id": 1,
    "date": "2024-02-22",
    "time": "14:30",
    "additional_info": "Optional additional details"
  }
  ```

### Get Booking Details
- **URL**: `/booking/{booking_id}`
- **Method**: `GET`

## Configuration

Key configuration is managed through environment variables in `docker-compose.yml`:
- Odoo credentials
- Directus settings
- API keys

## Security

- API key verification
- Secure integration between services
- Environment-based configuration

## Deployment

- The system is containerized and can be deployed using Docker Compose
- Adjust environment variables for production use
- Ensure proper network and security configurations

## Troubleshooting

- Check Docker logs for service-specific issues
- Verify environment variables
- Ensure all services are running correctly

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Specify your project's license here (e.g., MIT, Apache 2.0)

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/booking-management-system](https://github.com/yourusername/booking-management-system)
