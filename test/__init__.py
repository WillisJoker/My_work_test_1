from flask_testing import TestCase
from app import app


class Setting_TestCase_app(TestCase):  # 單元測試設定
    def create_app(self):
        app.config['TESTING'] = True
        return app
