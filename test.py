import sys

def test(option):
    if option == "fail":
        rise = 1
        run = 2 * 0
        return rise/run
    else:
        return True

if __name__ == "__main__":
    option = sys.argv[1]
    hello = test(option)
