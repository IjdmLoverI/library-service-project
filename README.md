# library-service-project
a simple library api, you can mke borrowings, add books,
powerful admin panel, stripe payment system, login with JWT
has a tg-bot with notifications 

## Installation

1. **Clone the Repository**

```bash
   git clone https://github.com/IjdmLoverI/library-service-project.git
   pip install -r requirements.txt
   run backend and tg-bot
   docker run -d -p 6379:6379 redis
   celery -A library_service_project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler