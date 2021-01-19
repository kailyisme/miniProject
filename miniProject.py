from rich.table import Table
from rich.console import Console
from rich.style import Style
from prompt_toolkit import prompt
import os

class Project:
    def __init__(self, nameOfProject="Project"):
        self.nameOfProject=nameOfProject
        self.data={}    #Initialize data Dic
    #Rich Console Style
        self.cStyle = Style(bgcolor= "thistle1", color="bright_cyan")
        # cStyle = Style(bgcolor= "grey62", color="black")
    #Rich Console Initializer
        self.c = Console()

    #Main Menu Rich Table
        self.menuTable = Table(title = "Program\nMain Menu")
        self.menuTable.add_column("Option", justify = "center", no_wrap = True)
        self.menuTable.add_column("Description", justify = "center")

        self.menuTable.add_row("show", "Show a table")
        self.menuTable.add_row("save", "Save DB")
        self.menuTable.add_row("exit", "Exit without saving")
        
    #Read DB for the first time
        self.readDB()
    #Check for data
        if self.data == {}:
        #Initialize data Dic if empty
            self.data = {"products": [], "couriers": [], "orders": []}

    def printMenu(self):
        self.c.print(self.menuTable, style = self.cStyle)  #Print Main Menu
    
    def readDB(self):
        nameOfProjectDB = self.nameOfProject + "DB"
        if os.path.isdir(nameOfProjectDB):
            for fileName in os.listdir(nameOfProjectDB):
                with open(f"{nameOfProjectDB}/{fileName}") as file:
                    listOfNames = fileName.split(".")[:-1]
                    tableName = listOfNames[0]
                    if len(listOfNames) > 1:
                        for name in listOfNames[1:]:
                            tableName += f".{name}"
                    self.data[tableName] = [line.rstrip().split(",") for line in file]

    def saveDB(self):
        nameOfProjectDB = self.nameOfProject + "DB"
        if not os.path.isdir(nameOfProjectDB):  #check if DB dir exists
            os.mkdir(nameOfProjectDB)   #If not create DB dir
        for fileName in self.data.keys():
            with open(f"{nameOfProjectDB}/{fileName}.txt", "w") as file:
                for line in self.data[fileName]:
                    file.write(f"{','.join(line)}\n")
        self.clearTerm()
        self.promptUser("Saved\nPress Enter")
    
    def showTablesList(self):
        self.clearTerm()
        self.c.print("Tables Present in DB", style = self.cStyle)
        for table in self.data.keys():
            self.c.print(table, style = self.cStyle)

    def showTable(self, tableName):
        self.clearTerm()
        if not self.data.get(tableName):
            self.c.print(f"There's no such table under the name of {tableName}", style = self.cStyle)
        else:
            aTable = Table(title = tableName.title())
            for header in self.data[tableName][0]:
                aTable.add_column(header, justify="center")
            for row in self.data[tableName][1:]:
                aTable.add_row(*[str(entry) for entry in row])
            self.c.print(aTable, style = self.cStyle)
    
    def promptTable(self):
        self.showTablesList()
        userInput = self.promptUser("Which table would you like to see?")
        self.showTable(userInput.strip())
        self.promptUser("Return to main menu?")

    def clearTerm(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def promptUser(self, promptText=""):
        userInput = prompt(f"{promptText}>")
        return userInput
    
    def promptMenuOption(self, promptText="Input Menu Option"):
        self.clearTerm()
        self.printMenu()
        userInput = self.promptUser(promptText).lower().strip()
        if userInput == "show":
            self.promptTable()
        elif userInput == "save":
            self.saveDB()
        elif userInput == "exit":
            self.clearTerm()
            self.c.print("Do you want to save changes? (Y/N)")
            if self.promptUser().lower().strip() == "y":
                self.saveDB()
            self.clearTerm()
            exit()
        else:
            self.promptMenuOption("Input a valid menu option")

#Main Program
if __name__=="__main__":
    main = Project()    #Initialize Program
    while True:
        main.promptMenuOption()