import numpy as np
import random

class userinfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def lookUser(self):
        print(f"user: {self.username} \npassword: {self.password}")









# while True:
#     action = input("Que ação deseja realizar? \"sair\", \"registrar\", \"entrar\": ").lower()
#     if action == "sair":
#         quit()
#     elif action == "registrar":
#         username = input("Informe um usuário: ")
#         password = input("Informe uma senha: ")
#         user = userInfo(username, password)
#         users = np.append(users, user)
#     elif action == "entrar":
#         search = input("Qual usuário você procura? ")
#         for i in range(users.size):
#             if search == users[i].username:
#                 passwordCheck = input("Qual sua senha? ")
#                 if passwordCheck == users[i].password:
#                     print("Acesso garantido.")
#                 else:
#                     print("Acesso negado.")
#                 break
#             elif i == (users.size-1):
#                 print("Usuário não encontrado.")
#     elif action == "gerar":
#         quantity = int(input("Quantos usuarios deseja gerar? "))
#         for _ in range(quantity):
#             username = str(random.randint(1, 999))
#             user = userInfo(username, "1")
#             users = np.append(users, user)
#     elif action == "olhar":
#         for i in range(users.size):
#             print(f"\nUser {i}:")
#             users[i].lookUser()