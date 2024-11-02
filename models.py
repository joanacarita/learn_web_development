from flask_login import UserMixin
from scripts.database import *


class User(UserMixin):
    # proxy for a database of users
    user_database = read_doctors()

    def __init__(self, id, email, numero_ordem, nome, apelido):
        # self.id = username
        # self.password = password
        self.id = id
        self.email = email
        self.numero_ordem = numero_ordem
        self.nome = nome
        self.apelido = apelido

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)