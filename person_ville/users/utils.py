import bcrypt

from users.models import User


def verify_password(password: str, hash_str: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hash_str.encode('utf-8'),
    )


def hash_password(password: str, rounds: int = 12) -> str:
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(rounds=rounds),
    ).decode('utf-8')


def check_password(username: str, password: str) -> bool:
    user = User.user_objects.get_user_by_username(username)
    user = User.user_objects.get_user_by_email(username) if not user else user
    return user and verify_password(password, user.password)
