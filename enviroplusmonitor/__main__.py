import sys

from enviroplusmonitor import app

if __name__ == "__main__":
    args = app.parse_args()
    app.main(args)
