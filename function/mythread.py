from threading import Thread

class MyThread(Thread):
    def __init__(self,function,args):
        Thread.__init__(self)
        self.func=function
        self.args=args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None