import datetime, csv, os

class User:
    def __init__(self, name :str, address :str, account_num : int, password : str):
        assert isinstance(name, str) and name.isalpha(), f"{name} is not a string"
        assert isinstance(address, str) and address.isalpha(), f"{address} is not a string"
        assert isinstance(account_num, int), f"{account_num} is not a string"
        assert password.isalnum(), f"{password} fill the password with number and alphabet"

        self.name = name
        self.address = address
        self.account_num = account_num
        self.__password = password

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def change_password(self, new_pass):
        self.__password = new_pass

    @password.deleter
    def delete_password(self):
        self.__password = None

    def show_user_details(self):
        return "%-9s: %s\n%-9s: %s\n%-9s: %s\n%-9s: %s\n" % ("Name", self.name, "address", self.address, "id", self.account_num, "password", self.__password)


class Bank(User):
    """Doc String

    Args:
        User (class)                : class that has user account features
        is_activity_record_empty    : bool variable that will check that the activity_record.csv file is empty or not
                                        (for define the condition to write the headers) false means write header
    """

    def __init__(self, name :str, address :str, account_num : int, password, balance=None):
        super().__init__(name, address, account_num, password)
        self.balance = balance

    def view_balance(self) -> str:
        print(f"Remaining balance is {self.balance}")

    def __write_activity(self, record: dict):
            if os.path.getsize(r'D:\simple_banking_sistem\activity_record.csv') == 0:
                with open(r"D:\simple_banking_sistem\activity_record.csv", 'w', newline='') as file:
                    headers = ['Name', 'Activity', 'Amount', 'Current Balance', 'Time', 'Description']
                    csv_write = csv.DictWriter(file, fieldnames=headers ,delimiter=',')
                    csv_write.writeheader()
                    csv_write.writerow(record)
            else:
                with open(r"D:\simple_banking_sistem\activity_record.csv", 'a', newline='') as file:
                    headers = ['Name', 'Activity', 'Amount', 'Current Balance', 'Time', 'Description']
                    csv_write = csv.DictWriter(file, fieldnames=headers ,delimiter=',')
                    csv_write.writerow(record)

    def read_activity(self):
        with open(r'D:\simple_banking_sistem\activity_record.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                print("%-12s: %s" % ('Name', row['Name']))
                print("%-12s: %s" % ('Activity', row['Activity']))
                print("%-12s: %s" % ('Amount', row['Amount']))
                print("%-12s: %s" % ('Balance', row['Current Balance']))
                print("%-12s: %s" % ('Time', row['Time']))
                print("%-12s: %s" % ('Description', row['Description']))
                print()

    def withdraw(self, amount: float) -> str:
        if self.balance - amount >= 0:
            self.balance -= amount
            print("withdraw money success")
            record = {
                'Name' : self.name,
                'Activity' : 'withdraw',
                'Amount' : f"-{amount}",
                'Current Balance' : self.balance,
                'Time' : str(datetime.datetime.now())[:19],
                'Description' : '-'.center(25)
                }

            self.__write_activity(record)
            self.view_balance()
        else:
            print(f"{amount} is greater than your balance which is just {self.balance} idr")

    def deposit(self, amount: float) -> str:
        self.balance += amount
        print("deposit money success")
        record = {
                'Name' : self.name,
                'Activity' : 'deposit',
                'Amount' : f"+{amount}",
                'Current Balance' : self.balance,
                'Time' : str(datetime.datetime.now())[:19],
                'Description' : '-'.center(25)
                }
        self.__write_activity(record)
        self.view_balance()

    def send(self, recipient_account: object, amount: float) -> str:
        if self.balance - amount >= 0:
            self.balance -= amount
            recipient_account.balance += amount
            print("Send money success")

            record_sender = {
                    'Name' : self.name,
                    'Activity' : 'send money',
                    'Amount' : f"-{amount}",
                    'Current Balance' : self.balance,
                    'Time' : str(datetime.datetime.now())[:19],
                    'Description' : f"Send money to {recipient_account.name}"
                    }

            record_recipient = {
                    'Name' : recipient_account.name,
                    'Activity' : 'receive money',
                    'Amount' : f"+{amount}",
                    'Current Balance' : recipient_account.balance,
                    'Time' : str(datetime.datetime.now())[:19],
                    'Description' : f"Receive money from {self.name}"
                    }

            self.__write_activity(record_sender)
            self.__write_activity(record_recipient)

        else:
            print(f"{amount} is greater than your balance which is just {self.balance} idr")


people1 = Bank('Jack', "London", 12487536, "archer123", 100)
people2 = Bank('Emily', "NYC", 12458897, "saber321", 110)

people1.deposit(5000)
people2.withdraw(50)

people1.send(people2, 300)
people2.withdraw(250.5)

people1.read_activity()
