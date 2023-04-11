import random
import pickle
import hashlib
import timeit

# Link da apresentação:
# https://docs.google.com/presentation/d/14Zd6fDJbgf_g8AuVjajRNByQ6G67CAFfbbH2vvIYiUc/edit#slide=id.p

# Classe responsável por segurar as informações do usuário
class userInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.accounts = dict()

    def getAccounts (self):
        return self.accounts()

    def getUsername (self):
        return self.username

# Hashtable que contém todos os usuários criados
class usersTable:
    def __init__ (self) :
        self.tableSize = 320
        self.users = [[] for i in range(self.tableSize)]

    # Função responsável por imprimir todos os usuários ao terminal para meios interativos
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

    # Função responsável por tornar o username do usuário em uma chave hash
    def hashIndex (self, username):
        index = 0
        for char in username:
            index += ord(char)
        return index % self.tableSize
    
    # Função responsável por calcular o tempo de busca de um usuário de forma sequencial
    def getUserSequential (self, search):
        startTimer = timeit.default_timer()
        for i in range(self.tableSize): # Corre pelos slots em ordem para tentar encontrar o usuário
            for registeredUser in self.users[i]: # Corre pelos usuários salvos no slot para verificar se o usuário está lá
                if registeredUser.getUsername() == search: # Ao encontrar o usuário no slot entra nesse if, finalizando a função
                    stopTimer = timeit.default_timer()
                    print(f"Encontrado (Sequencial) em {(stopTimer - startTimer):.6f} segundos")
                    return
        stopTimer = timeit.default_timer()
        print(f"Não encontrado (Sequencial) em {(stopTimer - startTimer):.6f} segundos") # Caso o usuário não seja enontrado ao correr pela lista toda retorna essa informação
        return
    
    # Função responsável por calcular o tempo de busca de um usuário de forma binária
    def getUserBinary (self, search):
        startTimer = timeit.default_timer()
        userIndex = self.hashIndex(search) # simula o index que a busca está procurando
        lowerPos = 0
        biggerPos = self.tableSize - 1
        while lowerPos <= biggerPos: # Procura pelo usuário dividindo a lista a cada busca, cada vez se aproximando mais
            middlePos = (lowerPos + biggerPos) // 2
            if middlePos < userIndex:
                lowerPos = middlePos + 1
            elif middlePos > userIndex:
                biggerPos = middlePos - 1
            elif middlePos == userIndex:
                for registeredUser in self.users[userIndex]: # procura sequenciamente pelo usuário apos encontrar o slot que ele está
                    if registeredUser.getUsername() == search:
                        stopTimer = timeit.default_timer()
                        print(f"Encontrado (Binary) em {(stopTimer - startTimer):.6f} segundos")
                        return
                stopTimer = timeit.default_timer()
                print(f"Não encontrado (Binary) em {(stopTimer - startTimer):.6f} segundos") # Retorna o tempo que a função tomou para concluir que o usuário não existe
                return

    # Função responsável por calcular o tempo de busca de um usuário em hash.  
    def getUserHash (self, search):
      startTimer = timeit.default_timer()
      i = self.hashIndex(search) # Faz o hash do username e descobre o sloth que ele se encontra em
      for registeredUser in self.users[i]: # Procura o usuário sequencialmente dentro do slot
          if registeredUser.getUsername() == search:
                stopTimer = timeit.default_timer()
                print(f"Encontrado (Hash) em {(stopTimer - startTimer):.6f} segundos")
                return registeredUser
      stopTimer = timeit.default_timer()
      print(f"Não encontrado (Hash) em {(stopTimer - startTimer):.6f} segundos") # Retorna o tempo que a função tomou para concluir que o usuário não existe
      return

    # Busca o usuário no sistema por hash, identica a função temporizada.
    def getUser (self, search):       
        i = self.hashIndex(search)
        for registeredUser in self.users[i]:
            if registeredUser.getUsername() == search:
                return registeredUser
        raise Exception("Usuário não encontrado")
  
    # Função responsável por adicionar o usuário a lista
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
    
    # Função responsável por remover um usuário da lista
    def deleteUser (self, user):
        username = user.getUsername()
        i = self.hashIndex(username)
        for j, registerUser in enumerate(self.users[i]):
            if registerUser.getUsername() == username:
                del self.users[i][j]
                break

users = usersTable()

# Processo de buscar usuários salvos fora do programa, caso existam
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
        quit()
    
    elif action == "registrar":
        username = input("Informe um usuário: ")
        exists = False
        # Processo de verificar se o username do usuário já está em uso
        for i in range(users.tableSize):
            for j, registerUser in enumerate(users.users[i]):
                if users.users[i][j].getUsername() == username:
                    print("Esse usuário já existe!")
                    exists = True
                    break
            if exists == True:
                break

        if exists == False:
            # Finalização do cadastro
            password = hashlib.md5(input("Informe uma senha: ").encode()).hexdigest()
            user = userInfo(username, password)
            # Processo de inserir o novo usuário na lista
            users.setUser(user)
            # Processo de salvar o novo usuário externamente
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
                            # Processo de deletar o usuário externamente
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
                            # Processo de deletar o usuário da lista
                            users.deleteUser(user)
                            print("Seu usuário foi deletado.")
                            break
                        else:
                            print("Senha incorreta.")

                    if action == "sair":
                        userLine = 0
                        # Processo de salvar as mudanças feitas externamente
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
                # Processo de gerar usuários aleatórios para simular um sistema com múltiplos usuários
                lower_abc = "abcdefghijklmnopqrstuvwxyz"
                upper_ABC = lower_abc.upper()
                letters = lower_abc + upper_ABC
                generatedUsers = int(input("Quantos usuários aleatórios você deseja gerar? "))
                for i in range(generatedUsers):
                    username = "".join(random.sample(letters, random.randint(3, 8)))
                    user = userInfo(username, "randomUser")
                    users.setUser(user)
            
            if action == "visualizar":
                # Processo de visualizar todos os usuários registrados na lista
                users.getAllUsers()

            if action == "teste":
                # Processo de testar a velocidade dos meios de busca
                search = input("Qual usuário você procura? ")
                users.getUserSequential(search)
                users.getUserBinary(search)
                users.getUserHash(search)