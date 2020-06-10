import sys

from enviroplusmonitor import enviroplusmonitor

if __name__ == "__main__":
    print("Running from environplusmonitor package")
    args = enviroplusmonitor.parse_args(sys.argv[1:])
    enviroplusmonitor.run(args)
