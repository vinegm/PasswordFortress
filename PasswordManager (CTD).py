import numpy as np
import random

class userInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def getUsername (self):
        return self.username

    def lookUser (self):
        print(f"user: {self.username} \npassword: {self.password}")

class usersTable:
    def __init__ (self) :
        self.tableSize = 100
        self.users = [[] for i in range(self.tableSize)]

    def olhar(self):
        for i in range(self.tableSize):
            print(self.users[i])

    def hashIndex (self, username):
        index = 0
        for char in username:
            index += ord(char)
        return index % self.tableSize
    
    def getUser (self, search):       
        i = self.hashIndex(search)
        for registeredUser in self.users[i]:
            if registeredUser.getUsername() == search:
                return registeredUser
    
    def setUser (self, user):
        username = user.getUsername()
        i = self.hashIndex(username)
        found = False
        for j, registerUser in enumerate(self.users[i]):
            if registerUser.getUsername() == username:
                self.users[i][j] = (user)
                found = True
                break
        if found == False:
            self.users[i].append((user))
    
    def deleteUser (Self, user):
        return


users = usersTable()
while True:
    action = input("Que ação deseja realizar? \"sair\", \"registrar\", \"entrar\": ").lower()
    
    if action == "sair":
        quit()
    
    elif action == "registrar":
        username = input("Informe um usuário: ")
        password = input("Informe uma senha: ")
        user = userInfo(username, password)
        users.setUser(user)
    
    elif action == "entrar":
        search = input("Informe seu usuário: ")
        user = users.getUser(search)
        if user != None:
            password = input("Informe sua senha: ")
            if password == user.password:
                print("Acesso garantido.")
            else:
                print("Acesso negado.")
        else:
            print("Usuário inexistente.")
    
    elif action == "olhar":
        users.olhar()
