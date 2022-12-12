import sys
import json

from diarybook import Diary, DiaryBook
from util import read_from_json_into_application
from user import User


class Menu:

    def __init__(self):
        self.diarybook = DiaryBook()
        self.user = User()
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
        self.user.log_in()

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
        self.user.data[f"{self.user.email}"]["Diaries"].append({"memo": diaries[-1].memo, "tags": diaries[-1].tags})
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
            json.dump(self.user.data, user)
        print("Thank you for using diarybook today")
        sys.exit(0)

    def populate_database(self):
        diaries1 = read_from_json_into_application('data.json')
        for diary in diaries1:
            self.diarybook.diaries.append(diary)


if __name__ == "__main__":
    Menu().run()
