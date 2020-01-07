import sys

from enviroplusmonitor import app

if __name__ == "__main__":
    print("Running from environplusmonitor package")
    args = app.parse_args()
    app.run(args)
