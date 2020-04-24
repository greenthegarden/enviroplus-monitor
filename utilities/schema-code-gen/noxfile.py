import nox


# @nox.session
# def tests(session):
#     session.install('pytest')
#     session.run('pytest')


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', '*.py')


@nox.session
def run(session):
  session.install("-r", "requirements.txt")
  session.run('python', 'json-schema-code-gen.py')
