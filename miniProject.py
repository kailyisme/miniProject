from rich.table import Table
from rich.console import Console
from rich.style import Style
from prompt_toolkit import prompt
import os
import datetime

class Project:
    def __init__(self, nameOfProject="Project"):
        self.nameOfProject=nameOfProject
        real_path = os.path.realpath(__file__)  #Get program file path
        self.dir_path = os.path.dirname(real_path)  #Get dir path for program file
        self.data={}    #Initialize data Dic
    #Rich Console Style
        # self.cStyle = Style(bgcolor= "thistle1", color="bright_cyan")
        self.cStyle = Style(bgcolor= "thistle1", color="black")
        # self.cStyle = Style(bgcolor= "grey62", color="black")
    #Rich Console Initializer
        self.c = Console()
    #Main Menu Rich Table
        self.menuTable = Table(title = "Program\nMain Menu")
        self.menuTable.add_column("Option", justify = "center", no_wrap = True)
        self.menuTable.add_column("Description", justify = "center")

        self.menuTable.add_row("add", "Add an order")
        self.menuTable.add_row("update", "Update Couriers or Products")
        self.menuTable.add_row("show", "Show a table")
        self.menuTable.add_row("save", "Save DB")
        self.menuTable.add_row("exit", "Exit without saving")
    #Read DB for the first time
        self.readDB()
    #Check for data
        if self.data == {}:
        #Initialize data Dic if empty
            self.data = {"products": [["Name"]], "couriers": [["Name"]], "orders": [["Time", "Courier", "Product", "Description"]]}

    def printMenu(self):
        self.c.print(self.menuTable, style = self.cStyle)  #Print Main Menu
    
    def readDB(self):
        nameOfProjectDB = self.nameOfProject + "DB"
        if os.path.isdir(self.dir_path + "/" + nameOfProjectDB):
            for fileName in os.listdir(self.dir_path + "/" + nameOfProjectDB):
                with open(f"{self.dir_path}/{nameOfProjectDB}/{fileName}") as file:
                    listOfNames = fileName.split(".")[:-1]  #remove
                    tableName = listOfNames[0]              #file
                    if len(listOfNames) > 1:                #extension
                        for name in listOfNames[1:]:
                            tableName += f".{name}"
                    self.data[tableName] = [line.rstrip().split(",") for line in file]

    def saveDB(self):
        nameOfProjectDB = self.nameOfProject + "DB"
        if not os.path.isdir(self.dir_path + "/" + nameOfProjectDB):  #check if DB dir exists
            os.mkdir(self.dir_path + "/" + nameOfProjectDB)   #If not create DB dir
        for fileName in self.data.keys():
            with open(f"{self.dir_path}/{nameOfProjectDB}/{fileName}.txt", "w") as file:
                for line in self.data[fileName]:
                    file.write(f"{','.join(line)}\n")
        self.clearTerm()
        self.promptUser("Saved\nPress Enter")
    
    def showTablesList(self):
        self.clearTerm()
        self.c.print("Tables Present in DB", style = self.cStyle)
        for table in self.data.keys():
            self.c.print(table, style = self.cStyle)

    def showTable(self, tableName, toEnum=False):
        self.clearTerm()
        if not tableName in self.data:
            self.c.print(f"There's no such table under the name of {tableName}", style = self.cStyle)
            return False
        elif not self.data.get(tableName):
            self.c.print(f"Table name: {tableName} is empty", style = self.cStyle)
            return False
        else:
            aTable = Table(title = tableName.title())
            if toEnum:
                aTable.add_column("#", justify="center")
                for header in self.data[tableName][0]:
                    aTable.add_column(header, justify="center")
                for num, row in enumerate(self.data[tableName][1:], 1):
                    aTable.add_row(str(num), *[str(entry) for entry in row])
            else:
                for header in self.data[tableName][0]:
                    aTable.add_column(header, justify="center")
                for row in self.data[tableName][1:]:
                    aTable.add_row(*[str(entry) for entry in row])
            self.c.print(aTable, style = self.cStyle)
    
    def addOrder(self):
        now = datetime.datetime.now()
        now = f"{now.hour}:{now.minute}_{now.day}/{now.month}/{now.year}"
        self.showTable("couriers", True)
        selectedCourier = self.promptUser("Select a courier (number/name)").lower()
        while True:
            try:
                selectedCourier = int(selectedCourier)
                if not selectedCourier in range(1, len(self.data["couriers"][1:]) + 1):
                    raise Exception("Not a valid option")
                break
            except Exception:
                for num, name in enumerate(self.data["couriers"][1:], 1):
                    if selectedCourier == name[0].lower():
                        selectedCourier = num
                        break
                selectedCourier = self.promptUser("Not a Valid Option\nSelect a courier (number/name)").lower()
        self.showTable("products", True)
        selectedProduct = self.promptUser("Select a product (number/name)").lower()
        while True:
            try:
                selectedProduct = int(selectedProduct)
                if not selectedProduct in range(1, len(self.data["products"][1:]) + 1):
                    raise Exception("Not a valid option")
                break
            except Exception:
                for num, name in enumerate(self.data["products"][1:], 1):
                    if selectedProduct == name[0].lower():
                        selectedProduct = num
                        break
                selectedProduct = self.promptUser("Not a Valid Option\nSelect a product (number/name)").lower()
        self.clearTerm()
        self.c.print("Input order details (Separate by commas if more than one field)")
        otherSelectedDetails = self.promptUser(",".join(self.data["orders"][0][3:]))
        self.data["orders"].append([now])
        self.data["orders"][-1].append(str(self.data["couriers"][selectedCourier][0]))
        self.data["orders"][-1].append(str(self.data["products"][selectedProduct][0]))
        otherSelectedDetails = [each.strip() for each in otherSelectedDetails.split(",")]
        for fieldNum in range(len(self.data["orders"][0][3:])):
            self.data["orders"][-1].append(otherSelectedDetails[fieldNum])
    
    def updateTable(self):
        self.showTablesList()
        userInput = self.promptUser("Which table would you like to update?").lower()
        if self.showTable(userInput) == False:
            self.promptUser("Press Enter")
            return None
        tableName = userInput
        userInput = self.promptUser("[add] Add entry/row [rm] Remove entry/row").lower()
        headers = ",".join(self.data[tableName][0])
        if userInput == "add":
            self.clearTerm()
            self.c.print("Add fields separated by commas")
            userInput = self.promptUser(headers)
            userInput = [x.strip() for x in userInput.split(",")]
            if userInput[0] in self.data[tableName]:
                self.c.print(f"Entry already present for {userInput[0]}")
                self.promptUser("Press Enter")
                return None
            newRow = [userInput[x] for x in range(len(self.data[tableName][0]))]
            self.data[tableName].append(newRow)
            self.showTable(tableName)
            self.c.print(f"Entry {newRow[0]} added")
            self.promptUser("Press Enter")
        elif userInput == "rm":
            self.showTable(tableName, True)
            selectedRow = self.promptUser("Select a row (number/name) to remove").lower()
            while True:
                try:
                    selectedRow = int(selectedRow)
                    if not selectedRow in range(1, len(self.data[tableName][1:]) + 1):
                        raise Exception("Not a valid row")
                    break
                except Exception:
                    for num, name in enumerate(self.data[tableName][1:], 1):
                        if selectedRow == name[0].lower():
                            selectedRow = num
                            break
                    selectedRow = self.promptUser("Not a Valid Option\nSelect a row (number/name)").lower()
            self.clearTerm()
            self.c.print(f"Are you sure you want to remove row\n{self.data[tableName][selectedRow]}")
            userInput = self.promptUser("Enter (Y/N)").lower()
            if userInput == "y":
                self.data[tableName].pop(selectedRow)
                self.showTable(tableName)
                self.c.print("Entry/Row Deleted")
                self.promptUser("Press Enter")
            else:
                self.clearTerm()
                self.c.print("No Entry/Row Deleted")
                self.promptUser("Press Enter")
        else:
            self.c.print("Invalid Option")
            self.promptUser("Press Enter")
    
    def promptTable(self):
        self.showTablesList()
        userInput = self.promptUser("Which table would you like to see?")
        self.showTable(userInput.strip())
        self.promptUser("Return to main menu?")

    def clearTerm(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def promptUser(self, promptText=""):
        userInput = prompt(f"{promptText} >")
        return userInput.strip()
    
    def promptMenuOption(self, promptText="Input Menu Option"):
        self.clearTerm()
        self.printMenu()
        # for each in self.data.items():
        #     print(each)
        userInput = self.promptUser(promptText).lower().strip()
        if userInput == "add":
            self.addOrder()
        elif userInput == "update":
            self.updateTable()
        elif userInput == "show":
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