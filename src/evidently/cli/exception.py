from evidently.cli import app


@app.command("exception")
def exception():
    f1()


def f1():
    f2()


def f2():
    f3()


def f3():
    raise Exception("Something went wrong")
