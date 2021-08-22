from flask import jsonify
from flask import Flask, request
from flask_restful import Api, Resource, abort
import database
from database import db, app
from weiboapi import weiboapi
import pdb

api = Api(app)
weibo = weiboapi()

# http://127.0.0.1:5000/user
class UserResource(Resource):

    def get(self):
        cmd = request.args.get('search')
        
        # 我关注的人
        if(cmd == 'follow'):

            user_id = request.json['user_id']
            follow_list = weibo.show_follow_list(user_id)

            user_schema = database.UserSchema(many=True)
            follow_data = user_schema.dump(follow_list)

            return jsonify(follow_data)
        
        # 关注我的人
        elif(cmd == 'fan'):

            user_id = request.json['user_id']
            fan_list = weibo.show_fan_list(user_id)

            user_schema = database.UserSchema(many=True)
            follow_data = user_schema.dump(fan_list)

            return jsonify(follow_data)
        
        # 搜索用户
        elif(cmd == 'name'):

            user_name = request.args.get('name')
            # user_name = request.json['name']
            user_info = weibo.search_by_name(user_name)

            if(user_info != False):

                user_schema = database.UserSchema()
                user_data = user_schema.dump(user_info)

                return jsonify(user_data)
            else:
                abort(400)


    def post(self):
        cmd = request.args.get('cmd')

        # 注册
        if(cmd == 'register'):

            name = request.json['name']
            password1 = request.json['password1']
            password2 = request.json['password2']

            new_user = weibo.user_sign_up(name, password1, password2)
            if(new_user != False):

                user_schema = database.UserSchema()
                user_data = user_schema.dump(new_user)

                return jsonify(user_data)
            else:
                abort(400)
                # return False
        
        # 关注
        elif(cmd == 'follow'):
            user_id = request.json['user_id']
            follow_id = request.json['follow_id']

            new_follow = weibo.follow_other(user_id, follow_id)
            if(new_follow != False):

                follow_schema = database.FollowSchema()
                follow_data = follow_schema.dump(new_follow)
                return jsonify(follow_data)
            else:
                abort(400)
        
    def put(self):
        cmd = request.args.get('cmd')

        # 登录
        if(cmd == 'login'):
            name = request.json['name']
            password = request.json['password']

            user = weibo.user_login(name, password)
            if(user != False):
                user_schema = database.UserSchema()
                user_data = user_schema.dump(user)
                return jsonify(user_data)
            else:
                abort(400)
                # return False
        
        # 退出
        elif(cmd == 'quit'):

            user_id = request.json['user_id']
            is_quit = weibo.user_quit(user_id)

            if(is_quit != False):
                user_schema = database.UserSchema()
                user_data = user_schema.dump(is_quit)
                return jsonify(user_data)
            else:
                abort(400)

        # 修改密码
        elif(cmd == 'pass'):
            
            user_id = request.json['user_id']
            old_pass = request.json['origin_password']
            new_pass = request.json['new_password']

            change_user = weibo.change_pass(user_id, old_pass, new_pass)
            if(change_user != False):
                user_schema = database.UserSchema()
                user_data = user_schema.dump(change_user)
                return jsonify(user_data)
            else:
                abort(400)
        

    def delete(self):
        cmd = request.args.get('cmd')

        # 取消关注
        if(cmd == 'unfollow'):

            user_id = request.json['user_id']
            follow_id = request.json['follow_id']

            unfollow = weibo.unfollow_other(user_id, follow_id)
            return jsonify(msg=unfollow)



# http://127.0.0.1:5000/weibo
class MessageResource(Resource):

    def get(self):
        cmd = request.args.get('message')

        # 我的微博
        if(cmd == 'my'):

            user_id = request.json['user_id']
            message_list = weibo.show_my_message(user_id)

            message_schema = database.MessageSchema(many=True)
            message_data = message_schema.dump(message_list)

            return jsonify(message_data)
        
        # 所有微博
        elif(cmd == 'all'):

            msg = database.Message.query.all()
            msg_schema = database.MessageSchema(many=True)
            msg_data = msg_schema.dump(msg)

            return jsonify(msg_data)
        
        # 关注微博
        elif(cmd == 'follow'):

            user_id = request.json['user_id']
            message_list = weibo.show_follow_message(user_id)

            message_schema = database.MessageSchema(many=True)
            message_data = message_schema.dump(message_list)

            return jsonify(message_data)
        
        elif(cmd == 'plot'):

            user_id = request.json['user_id']
            plot = weibo.show_plot(user_id)

            return jsonify(msg=plot)
    
    # 发微博
    def post(self):

        user_id = request.json['user_id']
        content = request.json['content']

        new_msg = weibo.send_message(user_id, content)
        if(new_msg != False):

            message_schema = database.MessageSchema()
            message_data = message_schema.dump(new_msg)

            return jsonify(message_data)
        
        else:
            abort(400)

# http://127.0.0.1:5000/weibo/1
class MessageDetail(Resource):

    # 微博详情
    def get(self, message_id):

        msg = database.Message.query.filter_by(id = message_id).first()
        message_schema = database.MessageSchema()
        message_data = message_schema.dump(msg)
        return jsonify(message_data)
    
    # 修改微博
    def put(self, message_id):

        user_id = request.json['user_id']
        content = request.json['content']

        new_content = weibo.change_msg(user_id, message_id, content)
        if(new_content != False):

            message_schema = database.MessageSchema()
            message_data = message_schema.dump(new_content)

            return jsonify(message_data)
        else:
            abort(400)
    
    # 删除微博
    def delete(self, message_id):

        user_id = request.json['user_id']

        is_deleted = weibo.delete_msg(user_id, message_id)
        return jsonify(msg=is_deleted)
    
    
    # 转发微博
    def post(self, message_id):

        user_id = request.json['user_id']
        content = request.json['content']

        relay_msg = weibo.relay_msg(user_id, message_id, content)
        if(relay_msg != False):

            message_schema = database.MessageSchema()
            message_data = message_schema.dump(relay_msg)

            return jsonify(message_data)
        else:
            abort(400)

# http://127.0.0.1:5000/weibo/1/comment
class CommentResource(Resource):

    # 查看评论
    def get(self, message_id):

        comment = database.Comment.query.filter_by(message_id = message_id).all()
        comment_schema = database.CommentSchema(many=True)
        comment_data = comment_schema.dump(comment)
        return jsonify(comment_data)
    
    # 发表评论
    def post(self, message_id):

        user_id = request.json['user_id']
        content = request.json['content']

        new_comment = weibo.send_comment(user_id, message_id, content)
        if(new_comment != False):
            comment_schema = database.CommentSchema()
            comment_data = comment_schema.dump(new_comment)
            return jsonify(comment_data)
        else:
            abort(400)

# http://127.0.0.1:5000/weibo/1/comment/1
class CommentDetail(Resource):

    # 评论详情
    def get(self, message_id, comment_id):

        comment = database.Comment.query.filter_by(id = comment_id)
        if(comment.count() > 0):
            comment_schema = database.CommentSchema()
            comment_data = comment_schema.dump(comment.first())
            return jsonify(comment_data)
        else:
            abort(400)

    # 修改评论  
    def put(self, message_id, comment_id):

        content = request.json['content']
        new_comment = weibo.change_comment(message_id, comment_id, content)
        if(new_comment != False):
            comment_schema = database.CommentSchema()
            comment_data = comment_schema.dump(new_comment)
            return jsonify(comment_data)
        else:
            abort(400)
    
    # 删除评论
    def delete(self, message_id, comment_id):

        is_delete = weibo.delete_comment(message_id, comment_id)
        return jsonify(msg=is_delete)

class Top10Message(Resource):

    def get(self):

        top_msg = weibo.show_top10()
        message_schema = database.MessageSchema(many=True)
        message_data = message_schema.dump(top_msg)

        return jsonify(message_data)


api.add_resource(UserResource, '/user')
api.add_resource(MessageResource, '/weibo')
api.add_resource(MessageDetail, '/weibo/<int:message_id>')
api.add_resource(CommentResource, '/weibo/<int:message_id>/comment')
api.add_resource(CommentDetail, '/weibo/<int:message_id>/comment/<int:comment_id>')
api.add_resource(Top10Message,'/weibo/top10')

# # 插入记录、更新数据
# @app.route("/add")
# def addTables():
#     obj = database.User(id=5, name='dsieadm')
#     db.session.add(obj)
#     db.session.commit()
 
#     return jsonify(msg="add successfully!")


# @app.route('/users')
# def list_users():
#     users = database.User.query.all()
#     user_schema = database.UserSchema(many=True)

#     user_data = user_schema.dump(users)

#     return jsonify(user_data)


# @app.route('/users/<userid>')
# def find_user(userid):
#     user = database.User.query.get(userid)
#     user_schema = database.UserSchema()

#     user_data = user_schema.dump(user)

#     return jsonify(user_data)

# @app.route("/")
# def index():
#     return "hello"

# @app.route("/createAll", methods=['GET', ])
# def createAllTables():
#     db.create_all()
#     return jsonify(msg="create successfully!")

if __name__ == "__main__":
    app.run(debug=True)
    