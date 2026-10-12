def greet(name: str) -> str:
    return f"hello {name}"


print("module name is", __name__)

if __name__ == "__main__":
    print(greet("world"))
