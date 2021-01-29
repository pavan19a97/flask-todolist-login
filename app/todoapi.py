from flask import jsonify, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with 
from app.models import TodoTasks
from app import db


argparser = reqparse.RequestParser()
argparser.add_argument("task", type=str, help="Task of the Todotask is required", required=True)
argparser.add_argument("user_id", type = int)


resource_field = {
    'id': fields.Integer,
    'task' : fields.String,
    'timestamp':fields.DateTime,
    'user_id': fields.Integer

}

class TodoApi(Resource):
    @marshal_with(resource_field)
    def get(self):
        result = TodoTasks.query.all()
        
        return result
    @marshal_with(resource_field)
    def post(self):
        # data = request.get_json()
        args = argparser.parse_args()
        if args['user_id']:
            addTask = TodoTasks(task=args['task'], user_id=args['user_id'])
        else:
            addTask = TodoTasks(task=args['task'])

        db.session.add(addTask)
        db.session.commit()
        result = TodoTasks.query.all()
        return result, 201

class TodoApiModify(Resource):
    @marshal_with(resource_field)
    def get(self, todo_id):
        result = TodoTasks.query.get(todo_id)
        if not result:
            abort(404, message="Todo task id doesn't exists to show")
        return result
    @marshal_with(resource_field)
    def delete(self, todo_id):
        result = TodoTasks.query.get(todo_id)
        if not result:
            abort(404, message="Todo task id doesn't exists to delete")
        db.session.delete(result)
        db.session.commit()
        result = TodoTasks.query.all()
        return result

    @marshal_with(resource_field)
    def put(self, todo_id):
        args = argparser.parse_args()
        result = TodoTasks.query.get(todo_id)
        if not result:
            abort(404, message="Todo task id doesn't exists to delete")
        result.task = args['task']
        db.session.commit()
        result = TodoTasks.query.all()
        return result
   
    

   
