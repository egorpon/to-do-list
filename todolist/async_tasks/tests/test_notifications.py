from django.test import TestCase
from unittest.mock import patch
from todolist.async_tasks.notifications.send_summary import send_daily_summary_task


class SendDailySummaryTest(TestCase):
    @patch("todolist.tasks.services.notifications.send_daily_summary")
    def test_send_daily_summary_task_calls_service(self, mock_send_daily_summary):
        mock_send_daily_summary.return_value = False

        send_daily_summary_task()

        mock_send_daily_summary.assert_called_once()

    @patch("todolist.tasks.services.notifications.send_daily_summary")
    def test_send_daily_summary_task_retries_when_service_returns_error(
        self, mock_send_daily_summary
    ):
        mock_send_daily_summary.return_value = True

        with patch.object(send_daily_summary_task, "retry") as mock_retry:
            send_daily_summary_task()

        mock_retry.assert_called_once_with(countdown=30)

    @patch("todolist.tasks.services.notifications.send_daily_summary")
    def test_send_daily_summary_task_does_not_retry_when_no_error(
        self, mock_send_daily_summary
    ):
        mock_send_daily_summary.return_value = False

        with patch.object(send_daily_summary_task, "retry") as mock_retry:
            send_daily_summary_task()

        mock_retry.assert_not_called()
