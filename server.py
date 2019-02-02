#!/usr/bin/python

from flask import Flask,jsonify, make_response, request, abort
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask_caching import Cache
import dao

app   = Flask(__name__)
api   = Api(app)
auth  = HTTPBasicAuth()
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


class Contacts(Resource):
    @auth.login_required
    @cache.cached(timeout=60)
    def get(self,pageno=None):
        if pageno is None:
            return jsonify({'result':dao.get_all_users()})
        else:
            offset = (pageno - 1) * 5
            pageno = 5
            return jsonify({'result':dao.get_all_users(pageno,offset)})


    @auth.login_required
    def post(self):
        print(request.json)
        if not request.json :
            print('request.json failed  ')
            abort(400)
        if request.json['name'] and type(request.json['name']) is not str:
            abort(400)
        if request.json['email'] and type(request.json['email']) is not str:
            abort(400)
        if request.json['mobile'] and type(request.json['mobile']) is not str:
            abort(400)
        if request.json['city'] and type(request.json['city']) is not str:
            abort(400)

        if dao.insert_user(request.json['name'],request.json['email'],request.json['mobile'],request.json['city']):
            return make_response(jsonify({'result': 'success'}), 201)
        else:
            return make_response(jsonify({'result': 'failure(Possible email duplication)'}), 201)



class ContactsByName(Resource):
    @auth.login_required
    def put(self,name):
        if not request.json :
            abort(400)
        if request.json['email'] and type(request.json['email']) is not str:
            abort(400)
        if request.json['mobile'] and type(request.json['mobile']) is not str:
            abort(400)
        if request.json['city'] and type(request.json['city']) is not str:
            abort(400)

        dao.update_user_by_name(name,request.json['email'],request.json['mobile'],request.json['city'])
        return make_response(jsonify({'result':'success'}),201)

    @auth.login_required
    def delete(self,name):
        dao.delete_user_by_name(name)
        return make_response(jsonify({'result':'success'}),202)

    @auth.login_required
    @cache.cached(timeout=60)
    def get(self,name,pageno=None):
        if pageno is None:
            return jsonify({'result':dao.get_user_by_name(name)})
        else:
            print('getting pageno ',pageno)
            offset = (pageno-1)*5
            pageno = 5
            print('offset ',offset,'pageno ',pageno)
            return jsonify({'result': dao.get_user_by_name(name, pageno, offset)})

class ContactsByEmail(Resource):
    @auth.login_required
    def put(self, email):
        if not request.json:
            abort(400)
        if request.json['name'] and type(request.json['email']) is not str:
            abort(400)
        if request.json['mobile'] and type(request.json['mobile']) is not str:
            abort(400)
        if request.json['city'] and type(request.json['city']) is not str:
            abort(400)

        dao.update_user_by_email(email, request.json['name'], request.json['mobile'], request.json['city'])
        return make_response(jsonify({'result': 'success'}), 201)

    @auth.login_required
    @cache.cached(timeout=60)
    def get(self,email,pageno=None):
        if pageno is None:
            print('pageno is none')
            return jsonify({'result':dao.get_user_by_email(email)})
        else:
            offset = (pageno-1)*5
            pageno = 5
            return jsonify({'result':dao.get_user_by_email(email,pageno,offset)})

    @auth.login_required
    def put(self,email):
        if not request.json :
            abort(400)
        if request.json['name'] and type(request.json['name']) is not str:
            abort(400)
        if request.json['mobile'] and type(request.json['mobile']) is not str:
            abort(400)
        if request.json['city'] and type(request.json['city']) is not str:
            abort(400)

        dao.update_user_by_email(request.json['name'],email,request.json['mobile'],request.json['city'])
        return make_response(jsonify({'result':'success'}),201)

    @auth.login_required
    def delete(self, email):
        dao.delete_user_by_email(email)
        return make_response(jsonify({'result': 'success'}), 202)


@auth.get_password
def get_password(username):
    return dao.get_password(username)

@auth.error_handler
def unauthorezed():
    return make_response(jsonify({'error': 'unauthorized'}),401)

api.add_resource(Contacts,'/contacts/api/v1.0', '/contacts/api/v1.0/<int:pageno>')
api.add_resource(ContactsByName,'/contacts/api/v1.0/name/<string:name>/<int:pageno>', '/contacts/api/v1.0/name/<string:name>')
api.add_resource(ContactsByEmail,'/contacts/api/v1.0/email/<string:email>/<int:pageno>', '/contacts/api/v1.0/email/<string:email>')

if __name__ == '__main__':
    app.run(debug=True)
