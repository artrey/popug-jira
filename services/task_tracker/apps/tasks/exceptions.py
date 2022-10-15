class TaskException(Exception):
    pass


class NoAvailablePopugs(TaskException):
    def __init__(self):
        super().__init__("no available popugs")
