import strawberry

@strawberry.type
class PasswordInfo():
    verify: str
    noMatch: list[str]