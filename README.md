# library-service-project
run backend and tg-bot

then to enable celery and daily task:

docker run -d -p 6379:6379 redis


celery -A library_service_project beat -l INFO --


scheduler django_celery_beat.schedulers:DatabaseScheduler