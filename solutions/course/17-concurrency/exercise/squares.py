
from concurrent.futures import ProcessPoolExecutor


def square(value: int) -> int:
    return value * value


def main() -> None:
    with ProcessPoolExecutor(max_workers=2) as pool:
        print(list(pool.map(square, [1, 2, 3])))


if __name__ == "__main__":
    main()
