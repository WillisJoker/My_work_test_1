from flask import Flask, request
from flask_restx import Resource, Api, fields
from tasks import cls_celery, fun_celery, celery
from celery.result import AsyncResult

app = Flask(__name__)
api = Api(app, title='Api', doc="/api/doc")  # api

tasksID_output_test = api.model('工作ID', {'ID':
                                         fields.String(required=True)})  # 預設:工作ID輸出

get_response = api.model('任務', {'任務狀態': fields.String(
    required=True), '任務進度': fields.String(required=True)})  # 預設:工作任務訊息輸出

input_name = api.model('使用者名稱', {'NAME':
                       fields.String(required=True)})  # 預設:名稱輸入訊息

output_name = api.model('使用者名稱', {'NAME':
                        fields.String(required=True)})  # 預設:名稱輸出訊息


@api.route('/A_get_tasks_state',)  # swagger 頁面_GET_工作狀態
class Get_tasks_state(Resource):
    @api.doc(params={'Tasks ID': 'ID'})
    @api.marshal_with(get_response)
    def get(self):
        data = request.args.get('Tasks ID')
        get_fun_res = AsyncResult(id=data, app=celery)
        return {'任務狀態': get_fun_res.state, '任務進度': get_fun_res.info}


@api.route('/A_fun_post_tasksID')  # swagger 頁面Fun_POST_tasksID
class Fun_post_tasksID(Resource):
    @api.expect(input_name)
    @api.marshal_with(tasksID_output_test)
    def post(self):
        res = fun_celery.delay()
        return {'ID': res.id}


@ api.route('/A_class_post_tasksID')  # swagger 頁面Class_POST_tasksID
class Class_post_tasksID(Resource):
    @ api.expect(input_name)
    @ api.marshal_with(tasksID_output_test)
    def post(self):
        res = cls_celery.delay()
        return {'ID': res.id}


@ api.route('/B_post_name')  # swagger 頁面POST_name
class Post_name(Resource):
    @ api.expect(input_name)
    @ api.marshal_with(output_name)
    def post(self):
        data_json = request.get_json()
        data = data_json.get('NAME', None)
        print("您的大名是:{}".format(data))
        return {'NAME': data}


@api.route('/B_get_name',)  # swagger 頁面Get_name
class Get_name(Resource):
    @api.doc(params={'NAME': 'User'})
    @api.marshal_with(output_name)
    def get(self):
        data = request.args.get('NAME')
        print("您的大名是:{}".format(data))
        return {'NAME': data}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
