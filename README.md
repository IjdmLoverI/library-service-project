# library-service-project

pip install -r requirements.txt

run backend and tg-bot

then to enable celery and daily task:

docker run -d -p 6379:6379 redis


celery -A library_service_project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# Project Setup

## Prerequisites

Ensure you have Docker, Python, and pip installed on your system.

## Installation

1. **Clone the Repository**

```bash
   git clone <repository-url>
   pip install -r requirements.txt
   run backend and tg-bot
   then to enable celery and daily task:
   docker run -d -p 6379:6379 redis
   celery -A library_service_project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler