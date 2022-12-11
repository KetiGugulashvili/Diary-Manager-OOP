import sys
import json

from diarybook import Diary, DiaryBook
from util import read_from_json_into_application


class Menu:

    def __init__(self):
        self.diarybook = DiaryBook()
        self.email = ""
        self.password = ""
        self.data = {}
        self.choices = {
            "1": self.show_diaries,
            "2": self.add_diary,
            "3": self.search_diaries,
            "4": self.populate_database,
            "5": self.sort_diaries,
            '6': self.quit
        }

    def display_menu(self):
        print(""" 
                     Notebook Menu  
                    1. Show diaries
                    2. Add diary
                    3. Search diaries
                    4. Populate database
                    5. Sort diaries
                    6. Quit program
                    """)

    def run(self):
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

        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def show_diaries(self, diaries=None):
        if not diaries:
            diaries = self.diarybook.diaries
        for diary in diaries:
            print(f"{diary.id}-{diary.memo}")

    def add_diary(self, diaries=None):
        memo = input("Enter a memo:         ")
        tags = input("add tags:             ")
        self.diarybook.new_diary(memo, tags)
        diaries = self.diarybook.diaries
        self.data[f"{self.email}"]["Diaries"].append({"memo": diaries[-1].memo, "tags": diaries[-1].tags})
        print("Your note has been added")

    def search_diaries(self):

        filter_text = input("Search for:  ")
        diaries = self.diarybook.search_diary(filter_text)
        for diary in diaries:
            print(f"{diary.id}-{diary.memo}")

    def sort_diaries(self, diaries=None):
        if not diaries:
            diaries = self.diarybook.diaries
        sort = input("How to sort:\n1. By ID\n2. By memo attributes\nEnter an option: ")
        if sort == "1":
            for diary in diaries:
                print(f"{diary.id}-{diary.memo}")
        elif sort == "2":
            new_diaries = []
            for diary in diaries:
                new_diaries.append(diary.memo)
            new_diaries.sort()
            for diary in new_diaries:
                print(f"{diary}")

    def quit(self):
        with open("user.json", "w") as user:
            json.dump(self.data, user)
        print("Thank you for using diarybook today")
        sys.exit(0)

    def populate_database(self):
        diaries1 = read_from_json_into_application('data.json')
        for diary in diaries1:
            self.diarybook.diaries.append(diary)


if __name__ == "__main__":
    Menu().run()
