from datetime import datetime, timezone
from operator import and_, truediv
from flask_restful import abort
import numpy as np

from sqlalchemy.orm import query
import database
from database import User, Comment, Follow, Message, db, app
import pytz
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import pdb

class weiboapi():

    # 密码加密
    def encrypt(self, passwordstr):
        # 导入密码加密模块
        import hashlib
        # 1.创建一个hash对象
        h = hashlib.sha256()
        # 2.填充要加密的数据
        h.update(bytes(passwordstr, encoding='utf-8'))
        # 3.获取加密结果
        password_result = h.hexdigest()
        return password_result

    # 获取用户id
    def get_id(self, user_name):
        query = User.query.filter_by(name=user_name)
        if (query.count() > 0):
            user_id = query.first().id
            return user_id
        else:
            return False

    def get_time_with_timezone(self):
        utc_tz = pytz.timezone('UTC')
        dt = datetime.now(tz=utc_tz)
        return dt


    # 用户注册
    def user_sign_up(self, user_name, user_password1, user_password2):
        name_count = User.query.filter_by(name=user_name).count()
        if(name_count > 0):
            print("用户名重复")
            return False
        elif(user_password1 == user_password2):
            new_user = User(
                name = user_name,
                password = self.encrypt(user_password1),
            )
            db.session.add(new_user)
            db.session.commit()
            print("注册成功")
            return new_user
        else:
            print("两次输入密码不相同")
            return False

    # 用户登录
    def user_login(self, user_name, user_password):
        query = User.query.filter_by(name=user_name)
        if(query.count() > 0):
            psw_crypt = query.first().password
            if(psw_crypt == self.encrypt(user_password)):
                query.update({"is_logined":True})
                db.session.commit()
                print("登录成功")
                return query.first()
            else:
                print("登录失败，密码错误")
                return False
        else:
            print("用户不存在")
            return False
    
    # 发送消息
    def send_message(self, user_id, content):

        if(user_id != False):
            new_msg = Message(
                user_id = user_id,
                content = content,
                send_date = self.get_time_with_timezone()
            )
            db.session.add(new_msg)
            db.session.commit()
            print("发送消息成功")
            return new_msg
        else:
            print("发送消息失败")
            return False
    
    # 发送评论
    def send_comment(self, user_id, message_id, content):

        query = Message.query.filter_by(id = message_id)
        user_query = User.query.filter_by(id = user_id)

        if(user_query.count() > 0 and query.count() > 0):
            new_comment = Comment(
                message_id = message_id,
                content = content,
                comment_date = self.get_time_with_timezone()
            )
            db.session.add(new_comment)
            db.session.commit()
            print("评论成功")
            return new_comment
        else:
            print("评论失败")
            return False
    
    # 关注
    def follow_other(self, user_id, follow_id):

        user_query = User.query.filter_by(id = user_id)
        follow_query = User.query.filter_by(id = follow_id)        

        if(user_query.count() > 0 and follow_query.count() > 0):
            new_follow = Follow(
                user_id = user_id,
                follow_id = follow_id,
                follow_date = self.get_time_with_timezone()
            )
            db.session.add(new_follow)
            db.session.commit()
            print("关注成功")
            return new_follow
        else:
            print("关注失败")
            return False
    
    def unfollow_other(self, user_id, follow_id):

        user1_query = User.query.filter_by(id = user_id)
        user2_query = User.query.filter_by(id = follow_id)        

        if(user1_query.count() > 0 and user2_query.count() > 0):
            
            follow_query = Follow.query.filter(and_(Follow.user_id == user_id, Follow.follow_id == follow_id))
            if(follow_query.count() > 0):
                db.session.delete(follow_query.first())
                db.session.commit()
                return "follow relation is deleted"
            else:
                return "follow relation is not exist"
        
        else:
            return "user or follower is not exist"



    
    # 显示关注列表
    def show_follow_list(self, show_user_id):
        query = Follow.query.filter_by(user_id = show_user_id).all()
        follow_list = []

        for i in range(len(query)):
            follow_id = query[i].follow_id
            follow_info = User.query.filter_by(id=follow_id).first()
            follow_list.append(follow_info)

        return follow_list
    
    # 显示粉丝列表
    def show_fan_list(self, show_user_id):
        query = Follow.query.filter_by(follow_id = show_user_id).all()
        fan_list = []

        for i in range(len(query)):
            fan_id = query[i].user_id
            fan_info = User.query.filter_by(id=fan_id).first()
            fan_list.append(fan_info)
        
        return fan_list
    
    def search_by_name(self, search_name):
        user_id = self.get_id(search_name)

        query = User.query.filter_by(id = user_id)

        if(query.count() > 0):
            return query.first()
        else:
            return False





    
    def show_my_message(self, show_user_id):
        query = Message.query.filter_by(user_id = show_user_id).all()
        print(query)
        return query

    def show_follow_message(self, show_user_id):
        query = Follow.query.filter_by(user_id = show_user_id).all()
        follow_msg_list = []
        for i in range(len(query)):
            follow_id = query[i].follow_id
            follow_msg = Message.query.filter_by(user_id = follow_id).all()

            follow_msg_list += follow_msg
        
        print(follow_msg_list)
        return follow_msg_list
    
    def change_msg(self, user_id, msg_id, content):

        query = Message.query.filter_by(id = msg_id).first()
        if(query.user_id == user_id):
            query.content = content
            db.session.commit()
            print(query)
            return query
        else:
            return False

    def delete_msg(self, user_id, msg_id):

        msg_query = Message.query.filter_by(id = msg_id)
        if(msg_query.count() > 0 and msg_query.first().user_id == user_id):

            # 删除消息之前首先将评论全部删除
            if(msg_query.first().comment_count != None):

                com_query = Comment.query.filter_by(message_id = msg_id).all()

                for i in range(len(com_query)):    
                    db.session.delete(com_query[i])

            db.session.delete(msg_query.first())
            db.session.commit()

            return "message %d is deleted" % msg_id
        else:
            return "message %d id not exist or have no authority" % msg_id
    
    def relay_msg(self, user_id, msg_id, content):

        query_cnt = Message.query.filter_by(id = msg_id).count()
        if(query_cnt > 0):
            new_msg = Message(
                user_id = user_id,
                content = content,
                send_date = self.get_time_with_timezone(),
                origin_message_id = msg_id
            )
            db.session.add(new_msg)
            db.session.commit()
            print("转发消息成功")
            return new_msg
        else:
            return False
    
    def change_comment(self, message_id, comment_id, content):

        query = Comment.query.filter_by(id = comment_id).first()
        # pdb.set_trace()
        if(query.message_id == message_id):
            query.content = content
            db.session.commit()
            print(query)
            return query
        else:
            return False

    def delete_comment(self, message_id, comment_id):

        query = Comment.query.filter_by(id = comment_id)
        if(query.count() > 0 and query.first().message_id == message_id):

            db.session.delete(query.first())
            db.session.commit()
            return "comment %d of message %d is deleted" % (comment_id, message_id)
        else:
            return "comment %d of message %d is not exist" % (comment_id, message_id)

    def user_quit(self, user_id):
        query = User.query.filter_by(id=user_id)
        if(query.count() > 0):
            query.update({"is_logined":False})
            db.session.commit()
            return query.first()
        else:
            return False
    
    def change_pass(self, user_id, old_pass, new_pass):
        query = User.query.filter_by(id=user_id)
        if(query.count() > 0 and query.first().is_logined == True) :
            psw_crypt = query.first().password
            if(psw_crypt == self.encrypt(old_pass)):
                query.update({"password" : self.encrypt(new_pass)})
                db.session.commit()
                print("修改密码成功")
                return query.first()
            else:
                return False
        else:
            return False

    def show_top10(self):
        query = Message.query.order_by(Message.comment_count.desc()).limit(10).all()
        return query

    def show_plot(self, user_id):
        query = Message.query.filter_by(user_id = user_id).all()           

        p = {}
        for i in range(24):
            p[i] = 0

        if(len(query) > 0):
            for i in range(len(query)):
                time = query[i].send_date
                hour = time.replace(tzinfo=None).strftime("%H")
                p[int(hour)] += 1
        else:
            return "user%d is not exist" % user_id

        t = list(p)
        cnt = list(p.values())

        ax = plt.figure().gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
        x_ticks = np.arange(0, 24)
        plt.xticks(x_ticks)

        plt.plot(t,cnt)
        plt.xlabel('时间')
        plt.ylabel('微博数量')
        plt.savefig('./restful/count.jpg')
        plt.close()
        # plt.show()
        return "user%d's count-time plot is saved" % user_id


if __name__ == "__main__":
    weibo1 = weiboapi()
    # weibo1.user_sign_up('张三','pass123','pass123')
    # weibo1.send_message(7,'iam7')
    # weibo1.follow_other(5,8)
    # weibo1.show_follow_list(5)
    # weibo1.send_comment(7,4,'iam7')
    # weibo1.show_my_message(5)
    # weibo1.show_follow_message(5)
    # weibo1.change_msg(6,5,'iam6')
    # weibo1.delete_msg(8,8)
    # weibo1.relay_msg(8,5,"relay test")
    # weibo1.change_comment(5, 8, 'change comment again')
    # weibo1.delete_comment(3, 5)
    # weibo1.user_login('c','1357')
    # weibo1.change_pass(9,'1357','123')
    weibo1.show_plot(5)
