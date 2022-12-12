import json
from diarybook import DiaryBook


class User:
    def __init__(self):
        self.email = ""
        self.password = ""
        self.data = {}
        self.diarybook = DiaryBook()

    def log_in(self):
        while True:
            log_in = input("1.Register\n2.Log in\nEnter an option: ")
            if log_in == "1":
                self.email = input("Please, register.\nEmail: ")
                self.password = input("Password: ")
                with open("user.json") as user:
                    self.data = json.loads(user.read())
                with open("user.json", "w") as user:
                    self.data[f"{self.email}"] = {"Password": self.password, "Diaries": []}
                    json.dump(self.data, user)
                break
            elif log_in == "2":
                self.email = input("Please, log in.\nEmail: ")
                self.password = input("Password: ")
                user = open("user.json")
                self.data = json.loads(user.read())
                checking_correct = False
                for users in self.data:
                    if self.email == users:
                        if self.password == self.data[self.email]["Password"]:
                            checking_correct = True
                            for diary in self.data[self.email]["Diaries"]:
                                self.diarybook.new_diary(diary["memo"], diary["tags"])
                        else:
                            print("Incorrect password.")
                if checking_correct:
                    break
                print("Such user does not exist.")