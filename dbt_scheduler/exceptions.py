from http import HTTPStatus


class DbtSchedulerException(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def serialize(self):
        cls = self.__class__
        return f"{cls.__module__}.{cls.__name__}", (str(self),), {}
