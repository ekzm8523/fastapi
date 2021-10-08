
def dict_update():
    a = {1: "from a", 2: "from a", 3: "from a"}
    b = {3: "from b", 4: "from b", 5: "from b"}
    print(f"a | b is : {a | b}")
    print(f"b | a is : {b | a}")
    a |= b
    print(a)

def new_string_method():
    string = "새로 나온 기능"
    print(string)
    print(string.removeprefix("새로"))
    print(string.removesuffix("기능"))

if __name__ == '__main__':
    dict_update()
    new_string_method()

