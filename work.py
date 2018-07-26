#codeing=utf-8


import os

#数据库类
class Dt:
    def __init__(self):
        self.build()
    
    def build(self):

        created = os.path.exists(DATABASE)#数据库是否存在 #DATABASE是一个数据库
        if not created:
            new_db.conect




if __name__=='__main__':

    #建表
    dt = Dt()