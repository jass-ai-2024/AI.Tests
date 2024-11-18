# не должно пройти

def read_file():
    with open("/home/user/data.txt", "r") as f:
        return f.read()

if __name__ == "__main__":
    print(read_file())
