import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth.settings")
app = Celery("auth")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


class RetryableTask:
    def __init__(self, func: callable, **kwargs):
        self.func = app.task(
            **(
                dict(
                    autoretry_for=(Exception,),
                    max_retries=10,
                    retry_backoff=2,
                    retry_backoff_max=60,
                )
                | kwargs
            )
        )(func)

    def __call__(self, *args, **kwargs):
        return self.func.apply_async(args=args, kwargs=kwargs)
