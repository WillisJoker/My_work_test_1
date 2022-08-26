from . import Setting_TestCase_app
import json
from unittest.mock import patch


class Test_Api(Setting_TestCase_app):
    def test_Get_name(self):
        response = self.client.get(
            '/B_get_name', query_string={'NAME': 'Will'})
        self.assertEqual(response.json, {'NAME': 'Will'})
        self.assertEqual(response.status_code, 200)

    def test_Post_name(self):
        response = self.client.post(
            '/B_post_name',
            data=json.dumps({'NAME': 'Will'}), content_type='application/json')
        self.assertEqual(response.json, {'NAME': 'Will'})
        self.assertEqual(response.status_code, 200)

    @patch('tasks.class_celery.delay')
    def test_Class_post_tasksID(self, mock_class_celery):
        response = self.client.post(
            '/A_class_post_tasksID',
            data=json.dumps({"NAME": "string"}), content_type='application/json')
        self.assertTrue(mock_class_celery.called)
        self.assertEqual(response.status_code, 200)

    @patch('tasks.fun_celery.delay')
    def test_Fun_post_tasksID(self, mock_fun_celery):
        response = self.client.post(
            '/A_fun_post_tasksID',
            data=json.dumps({"NAME": "string"}), content_type='application/json')
        self.assertTrue(mock_fun_celery.called)
        self.assertEqual(response.status_code, 200)

    @patch('app.request')
    @patch('app.AsyncResult')
    def test_Get_tasks_state(self, mock_request, AsyncResult):
        response = self.client.get(
            '/A_get_tasks_state', query_string={'NAME': 'Will'})
        self.assertEqual(response.status_code, 200)
