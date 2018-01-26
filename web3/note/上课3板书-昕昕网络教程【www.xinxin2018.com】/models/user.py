from models import Model
from models import load


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        valid_users = self.all()
        print('valid_users {}'.format(valid_users))
        for user in valid_users:
            if self.username == user.username and self.password == user.password:
                return True
        else:
            return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

