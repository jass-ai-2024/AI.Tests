# не должно пройти
class UnusedClass:
    def __init__(self, value):
        self.value = value

def add_numbers(a, b):
    return a + b

if __name__ == "__main__":
    print(add_numbers(3, 5))
