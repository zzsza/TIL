class LazyDB:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = "Value for {name}".format(name=name)
        setattr(self, name, value)
        return value


data = LazyDB()
print("Before: ", data.__dict__)
print("foo: ", data.foo)
print("After ", data.__dict__)


class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print("Called __getattr__({name})".format(name=name))
        return super().__getattr__(name)


data = LoggingLazyDB()
print("exists: ", data.exists)
print("foo: ", data.foo)
print("foo: ", data.foo)
print("="*30)


class ValidatingDB:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print("Called __getattributed__ ({name})".format(name=name))
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = "Value for {name}".format(name=name)
            setattr(self, name, value)
            return value


data2 = ValidatingDB()
print("exists: ", data2.exists)
print("foo: ", data2.foo)
print("foo: ", data2.foo)