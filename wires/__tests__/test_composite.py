from wires.composite import Composite
from dataclasses import dataclass, field


def test_composite() -> None:
    @dataclass
    class User:
        name: str
        age: int
        skills: list[str]

    composite: Composite[User] = Composite(
        User,
        "John",
        30,
        skills=["Python", "JavaScript"]
    )

    assert composite.model == User
    assert composite.args == ["John", 30]
    assert composite.kwargs == {"skills": ["Python", "JavaScript"]}

    assert composite() == User(
        name="John",
        age=30,
        skills=["Python", "JavaScript"]
    )


def test_composite_nested() -> None:
    @dataclass
    class Skill:
        name: str

    class Repository:
        def get_all(self) -> list[Skill]:
            return [
                Skill(name="Python"),
                Skill(name="JavaScript"),
            ]

    @dataclass
    class User:
        name: str
        age: int
        repository_port: Repository
        skills: list[Skill] = field(default_factory=list)

        def __post_init__(self):
            self.skills = self.repository_port.get_all()

    repository_composite: Composite[
        Repository
    ] = Composite(Repository)  # type: ignore
    user_composite: Composite[User] = Composite(  # type: ignore
        User,
        "Ricardo",
        35,
        repository_port=repository_composite
    )
    user = user_composite()

    assert user.skills == [Skill(name="Python"), Skill(name="JavaScript")]
