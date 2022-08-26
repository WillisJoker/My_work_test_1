from tasks import class_celery, fun_celery

from . import Setting_TestCase_app


class TestfunTask(Setting_TestCase_app):
    def test_fun_setUp(self):
        self.task = fun_celery.apply()
        self.assertEqual(self.task.state, 'SUCCESS')

    def test_class_setUp(self):
        self.task = class_celery.apply()
        self.assertEqual(self.task.state, 'SUCCESS')
