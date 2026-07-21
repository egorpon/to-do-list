from django.test import TestCase
from todolist.todos.tests.factories import UserFactory, TodoListFactory
from todolist.tasks.tests.factories import TaskFactory
from django.utils import timezone
from todolist.tasks.services.notifications import send_daily_summary
from todolist.todos.models import ReminderLog
from django.core import mail
from unittest.mock import patch
from smtplib import SMTPException


class TaskNotificationsTest(TestCase):
    def setUp(self):
        self.user_1 = UserFactory(email="ponomarenkoegor36@gmail.com")
        self.todo = TodoListFactory(owner=self.user_1)
        self.task1 = TaskFactory(todo=self.todo)
        self.task2 = TaskFactory(
            todo=self.todo, due_date=timezone.now() + timezone.timedelta(days=2)
        )

    def test_send_daily_summary_marks_log_success_when_email_sent(self):
        has_error = send_daily_summary()

        log = ReminderLog.objects.get(user=self.user_1, date=timezone.localdate())

        self.assertEqual(log.status, ReminderLog.Status.SUCCESS)
        self.assertFalse(has_error)
        self.assertEqual(len(mail.outbox), 1)

    @patch(
        "todolist.tasks.services.notifications.send_mail",
        side_effect=SMTPException("failed"),
    )
    def test_send_daily_summary_marks_log_failed_on_smtp_exception(
        self, mock_send_email
    ):
        has_error = send_daily_summary()

        log = ReminderLog.objects.get(user=self.user_1, date=timezone.localdate())

        self.assertEqual(log.status, ReminderLog.Status.FAILED)
        self.assertTrue(has_error)
        self.assertEqual(len(mail.outbox), 0)

    @patch("todolist.tasks.services.notifications.send_mail")
    def test_send_daily_summary_skips_user_with_existing_success_log(
        self, mock_send_email
    ):

        log = ReminderLog(
            user=self.user_1,
            date=timezone.localdate(),
            status=ReminderLog.Status.SUCCESS,
        )
        log.save()

        send_daily_summary()

        mock_send_email.assert_not_called()

    @patch("todolist.tasks.services.notifications.send_mail")
    def test_send_daily_summary_retries_user_with_failed_log(self, mock_send_email):

        log = ReminderLog(
            user=self.user_1,
            date=timezone.localdate(),
            status=ReminderLog.Status.FAILED,
        )
        log.save()

        send_daily_summary()

        mock_send_email.assert_called_once()

        log = ReminderLog.objects.get(user=self.user_1, date=timezone.localdate())
        self.assertEqual(log.status, ReminderLog.Status.SUCCESS)


    
    def test_send_daily_summary_continues_processing_after_one_user_fails(self):

        other_user = UserFactory(email='any@gmail.com')
        other_todo = TodoListFactory(owner=other_user) 
        other_task = TaskFactory(todo=other_todo)


        def side_effect(*args, **kwargs):
            if kwargs['recipient_list'] == [self.user_1.email]:
                raise SMTPException("failed")
            return 1
        with patch("todolist.tasks.services.notifications.send_mail", side_effect=side_effect):
            has_error = send_daily_summary()

        self.assertTrue(has_error)
        self.assertEqual(ReminderLog.objects.get(user=self.user_1).status, ReminderLog.Status.FAILED)
        self.assertEqual(ReminderLog.objects.get(user=other_user).status, ReminderLog.Status.SUCCESS)

    