#
# def make_gen(n=3):
#     i = 0
#     while i < n:
#         yield i
#
#
# def generator_process():
#     print("enter the generator method")
#     return "generator finished"
#
# def not_generator_process():
#     print("enter the method")
#     return "method finished"
#
#
# if __name__ == '__main__':
#     gen = (generator_process() for i in range(5))
#     print("start")
#     print(type(gen))
#     for num in gen:
#         print(num)
#
#     print("start 2")
#     no_gen = [not_generator_process() for i in range(5)]
#     print(type(no_gen))
#     for fun in no_gen:
#         print(fun)
