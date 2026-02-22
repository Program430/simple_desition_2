class DomainError(Exception):
    pass


class RequestError(DomainError):
    pass


class ParserError(DomainError):
    pass
