from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from todolist.tasks.models import Task
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Task)
def invalidate_task_cache(sender, instance, **kwargs):

    print("Clearing tasks cache")

    cache.delete_pattern("*tasks*")
