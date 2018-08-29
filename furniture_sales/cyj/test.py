class singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


obj1 = singleton()
print(obj1)
obj2 = singleton()
print(obj1 is obj2)
