from faker import Faker


class FakeUser:
    fake: Faker = Faker()

    def __init__(self) -> None:
        self.username: str = self.fake.user_name()
        self.password: str = self.fake.password()
        self.email: str = self.fake.email()

    def get_data(self) -> dict[str, str]:
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }
