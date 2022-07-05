class Foo:
    def __init__(self):
        self.name = 0
        print(self.name)

    def func(self):
        print(self.name)


foo = Foo()
foo.name = 1
print(foo.name)
foo.func()
