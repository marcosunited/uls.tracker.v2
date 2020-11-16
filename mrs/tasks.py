from background_task import background


@background(schedule=20)
def test():
    print("task executed")
