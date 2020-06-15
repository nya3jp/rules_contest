import time


def main():
    n = int(input())
    if n == 1:
        print(42)
    else:
        time.sleep(10)
        print(84)


if __name__ == '__main__':
    main()
