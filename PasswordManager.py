import random
import pickle
import hashlib
import timeit

class userInfo:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.accounts = dict()

    def getAccounts (self):
        return self.accounts()

    def getUsername (self):
        return self.username

    def lookUser (self):
        print(f"user: {self.username} \npassword: {self.password}")

class usersTable:
    def __init__ (self) :
        self.tableSize = 960
        self.users = [[] for i in range(self.tableSize)]

    def getAllUsers(self):
        for i in range(self.tableSize):
            if len(self.users[i]) == 0:
                pass
            else:
                print(f"\nIndexKey: {i}")
                for j, registerUser in enumerate(self.users[i]):
                    print(f"{self.users[i][j].getUsername()}", end = "")
                    if j != (len(self.users[i])-1):
                        print(", ", end = "")

    def hashIndex (self, username):
        index = 0
        for char in username:
            index += ord(char)
        return index % self.tableSize
    
    def getUserSequential (self, search):
        startTimer = timeit.default_timer()
        for i in range(self.tableSize):
            for registeredUser in self.users[i]:
                if registeredUser.getUsername() == search:
                    stopTimer = timeit.default_timer()
                    print(f"encontrado Sequential em {(stopTimer - startTimer):.6f} segundos")
                    return
                
    def getUserBinary (self, search):
        userIndex = self.hashIndex(search)
        startTimer = timeit.default_timer()
        lowerPos = 0
        biggerPos = self.tableSize - 1
        while lowerPos <= biggerPos:
            middlePos = (lowerPos + biggerPos) // 2
            if middlePos == userIndex:
                for registeredUser in self.users[userIndex]:
                    if registeredUser.getUsername() == search:
                        stopTimer = timeit.default_timer()
                        print(f"Encontrado Binary em {(stopTimer - startTimer):.6f} segundos")
                        return
            if middlePos > userIndex:
                biggerPos = middlePos - 1
            if middlePos < userIndex:
                lowerPos = middlePos + 1

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
    
    def deleteUser (self, user):
        username = user.getUsername()
        i = self.hashIndex(username)
        for j, registerUser in enumerate(self.users[i]):
            if registerUser.getUsername() == username:
                del self.users[i][j]
                break

users = usersTable()

try: 
    with open("SavedUsers.users", "rb") as file:
        for line in file.readlines():
            serializedUser = line.rstrip()
            user = pickle.loads(serializedUser)
            users.setUser(user)
except FileNotFoundError:
    pass

while True:
    action = input("\nQue ação deseja realizar?\
                   \n\"Registrar\": Registra um novo usuário.\
                   \n\"Entrar\": Entra com um usuário existente.\
                   \n\"Sair\": Fecha o programa.\n").lower()
    
    if action == "sair":
        break
    
    elif action == "registrar":
        username = input("Informe um usuário: ")
        exists = False
        for i in range(users.tableSize):
            for j, registerUser in enumerate(users.users[i]):
                if users.users[i][j].getUsername() == username:
                    print("Esse usuário já existe!")
                    exists = True
                    break
            if exists == True:
                break

        if exists == False:
            password = hashlib.md5(input("Informe uma senha: ").encode()).hexdigest()
            user = userInfo(username, password)
            users.setUser(user)
            serializedUser = pickle.dumps(user) + b"\n"
            with open("SavedUsers.users", "ab") as file:
                file.write(serializedUser)
            print("usuário salvo!")
    
    elif action == "entrar":
        search = input("Informe seu usuário: ")
        user = users.getUser(search)
        if user == None:
            print("Usuário inexistente.")
        else:
            password = hashlib.md5(input("Informe sua senha: ").encode()).hexdigest()
            if password != user.password:
                print("Acesso negado.")
            else:
                while True:
                    action = input("\nQue ação deseja realizar?\
                                    \n\"Ler\": Ver suas contas.\
                                    \n\"Adicionar\": Adiciona uma nova conta.\
                                    \n\"Remover\": Remove uma conta existente.\
                                    \n\"Apagar\": Apaga seu usuário.\
                                    \n\"Sair\": Sai do seu usuário e renorna ao início.\n").lower()
                    
                    if action == "ler":
                        for plataform, plataformPassword in user.accounts.items():
                            print(f"{plataform}: {plataformPassword}")

                    if action == "adicionar":
                        plataform = input("Informe a plataforma: ")
                        plataformPassword = input("Informe a senha: ")
                        user.accounts[plataform] = plataformPassword

                    if action == "remover":
                        plataform = input("Informe a plataforma que deseja remover: ")
                        if plataform in user.accounts:
                            del user.accounts[plataform]
                        else:
                            print("Conta inexistente.")

                    if action == "apagar":
                        password = hashlib.md5(input("Informe sua senha para confirmar: ").encode()).hexdigest()
                        if password == user.password:
                            userLine = 0
                            with open("SavedUsers.users", "rb") as file:
                                for line in (editUser := file.readlines()):
                                    serializedUser = line.rstrip()
                                    lookingForUser = pickle.loads(serializedUser)
                                    if lookingForUser.getUsername() == user.getUsername():
                                        break
                                    userLine +=1
                            with open("SavedUsers.users", "wb") as file:
                                del editUser[userLine]
                                file.writelines(editUser)
                            users.deleteUser(user)
                            print("Seu usuário foi deletado.")
                            break
                        else:
                            print("Senha incorreta.")

                    if action == "sair":
                        userLine = 0
                        with open("SavedUsers.users", "rb") as file:
                            for line in (editUser := file.readlines()):
                                serializedUser = line.rstrip()
                                lookingForUser = pickle.loads(serializedUser)
                                if lookingForUser.getUsername() == user.getUsername():
                                    serializedUser = pickle.dumps(user)
                                    break
                                userLine +=1
                        with open("SavedUsers.users", "wb") as file:
                            editUser[userLine] = serializedUser + b"\n"
                            file.writelines(editUser)
                        break
    
    elif action == "devtools":
        while True:
            action = input("\nEstá é uma ferramenta para testes, que função deseja realizar?\
                            \n\"Gerar\": Gera alguma quantidade de usuários aleatórios.\
                            \n\"Visualizar\": Vizualiza todos os usuários existentes.\
                            \n\"Teste\": Testa a velocidade dos meios de busca.\
                            \n\"Sair\": Sai das ferramentas de testes e renorna ao início.\n").lower()

            if action == "sair":
                break

            if action == "gerar":
                lower_abc = "abcdefghijklmnopqrstuvwxyz"
                upper_ABC = lower_abc.upper()
                letters = lower_abc + upper_ABC
                generatedUsers = int(input("Quantos usuários aleatórios você deseja gerar? "))
                for i in range(generatedUsers):
                    username = "".join(random.sample(letters, random.randint(3, 8)))
                    user = userInfo(username, "randomUser")
                    users.setUser(user)
            
            if action == "visualizar":
                users.getAllUsers()

            if action == "teste":
                search = input("Qual usuário você procura? ")
                users.getUserSequential(search)
                users.getUserBinary(search)
                startTimer = timeit.default_timer()
                users.getUser(search)
                stopTimer = timeit.default_timer()
                print(f"Encontrado hash em {(stopTimer - startTimer):.6f} segundos")
                