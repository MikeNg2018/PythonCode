def use_logging(func):
    def wrapper(*args,**kwargs):
        print("%s is running" % func.__name__)
        print('wrapper')
        print("name=",args[0])
        print("age=",args[1])
        return func(*args,**kwargs)   # 把 foo 当做参数传递进来时，执行func()就相当于执行foo()
    return wrapper

def use_logging2(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                print("%s is running warn" % func.__name__)
            elif level == "info":
                print("%s is running info" % func.__name__)
            return func(*args)
        return wrapper
    return decorator

@use_logging
def foo(*args,**kwargs):
    print("i am %s , age %s" % (args[0],args[1]))
    print("He say: %s" % kwargs['a'])

@use_logging2(level='info')
def test():
    print('Test it!')
#foo = use_logging(foo)  # 因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper

foo("Mike","30",a='hello',b=3,c='C')

test()


class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print('class decorator runing')
        self._func()
        print('class decorator ending')

@Foo
def bar():
    print('bar')
bar()
