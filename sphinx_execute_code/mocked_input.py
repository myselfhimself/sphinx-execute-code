class MockedInput:
    def __init__(self, side_effects):
        self.__side_effects = (se for se in side_effects)

    def __call__(self, *args, **kwargs):
        p = args[0]
        print(p, end=" ")
        s = next(self.__side_effects)
        print(s)
        return s