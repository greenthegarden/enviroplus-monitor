# Import Python libs
import sys

# Import 3rd-party libs
import nox

if __name__ == "__main__":
    sys.stderr.write(
        "Do not execute this file directly. Use nox instead, it will know how to handle this file\n"
    )
    sys.stderr.flush()
    exit(1)


@nox.session(python="3.7")
def tests(session):
    """Run test suite with pytest."""
    session.install("-r", "requirements-test.txt")
    # session.run("pytest", "-v", "tests")
    session.run(
        "pytest",
        "--cov=enviroplusmonitor",
        "--cov-config",
        ".coveragerc",
        "--cov-report=",
        "-v",
        "tests",
    )
    session.notify("cover")


@nox.session
def cover(session):
    """Coverage analysis."""
    session.install("coverage")
    # if ON_APPVEYOR:
    #     fail_under = "--fail-under=99"
    # else:
    fail_under = "--fail-under=100"
    session.run("coverage", "report", fail_under, "--show-missing")
    session.run("coverage", "erase")


@nox.session(python="3.7")
def blacken(session):
    """Run black code formatter."""
    session.install("black==19.10b0", "isort==4.3.21")
    files = ["enviroplusmonitor", "tests", "noxfile.py"]
    session.run("black", *files)
    session.run("isort", "--recursive", *files)


@nox.session(python="3.7")
def lint(session):
    """Run code linting."""
    session.install("flake8==3.7.9", "black==19.10b0", "mypy==0.760")
    session.install("-r", "requirements-test.txt")
    session.run("mypy", "enviroplusmonitor")
    files = ["enviroplusmonitor", "tests", "noxfile.py"]
    session.run("black", "--check", *files)
    session.run("flake8", "src", *files)


@nox.session(python="3.7")
def security(session):
    """Run security tests."""
    session.install("bandit==1.6.2")
    session.install("-r", "requirements-test.txt")
    files = ["enviroplusmonitor", "tests"]
    session.run("bandit", "-r", *files)


@nox.session(python="3.7")
def docs(session):
    """Build the documentation."""
    session.run("rm", "-rf", "docs/_build", external=True)
    session.install("-r", "requirements-test.txt")
    # session.install(".")
    session.cd("docs")
    sphinx_args = ["-b", "html", "-W", "-d", "_build/doctrees", ".", "_build/html"]

    if not session.interactive:
        sphinx_cmd = "sphinx-build"
    else:
        sphinx_cmd = "sphinx-autobuild"
        sphinx_args.insert(0, "--open-browser")

    session.run(sphinx_cmd, *sphinx_args)
