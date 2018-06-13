import threading
import time

begin = time.time()

def foo(n):
    print("In foo %s" %n)
    time.sleep(1)
    print("foo end!")

def bar(n):
    print("In bar %s" %n)
    time.sleep(2)
    print("bar end!")


# foo()
# bar()

t1 = threading.Thread(target=foo, args=(1,))
t2 = threading.Thread(target=bar, args=(2,))

t1.start()
t2.start()

print("-------end----------")

end = time.time()
print(end - begin)
