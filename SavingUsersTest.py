import pickle

class userInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsername (self):
        return self.username

while True:  
    a = input()
    
    if a == "1":

        user = userInfo("vine", "123")

        
        serializedUser = pickle.dumps(user)
        with open("SavedUsers.pickle", "ab") as file:
            file.write(serializedUser)
        with open("SavedUsers.pickle", "a") as file:
            file.write("\n")

        break

    elif a == "2":

        with open("SavedUsers.pickle", "rb") as file:
            for line in file.readlines():
                serializedUser = line.rstrip()
                user = pickle.loads(serializedUser)
                print(user.getUsername())

        break
    
    break