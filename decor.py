

def decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase
    return wrapper

@decorator
def say_hi():
    return "Hi"


res=say_hi()
print(res)
