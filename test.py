a = None
b = None

def setup_params():
    global a, b
    a = "a"
    b = 3

def use_params():
    print(a)
    print(b)

setup_params()
use_params()