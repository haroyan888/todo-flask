import secrets
import string


def gen_id(len: int):
	return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(len))