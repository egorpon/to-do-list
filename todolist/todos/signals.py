from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from todolist.todos.models import TodoList
from todolist.tasks.models import Task
from django.core.cache import cache


@receiver([post_save, post_delete], sender=TodoList)
def invalidate_todolist_cache(sender, instance, **kwargs):

    print("Clearing todolist cache")

    cache.delete_pattern("*todos*")