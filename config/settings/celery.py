from config.env import env


CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_BACKEND_RESULT = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
