from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError("The phone number must consist of 10 digits")
        self.value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for record_phone in self.phones:
            if str(record_phone) == phone:
                self.phones.remove(record_phone)
                return 
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone number not found")

    def find_phone(self):
        phones = '; '.join(p.value for p in self.phones)
        return phones

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday if self.birthday else ""}, phones: {'; '.join(p.value for p in self.phones)}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            raise ValueError("Record not found.")
        
    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        current_timedelta = current_date + timedelta(7)
        current_year = datetime.now().year
        result = []
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value.date().replace(year=current_year)
                if birthday_date < current_date:
                    birthday_date = birthday_date.replace(year=current_year + 1)
                if current_date <= birthday_date <= current_timedelta:
                    result.append({"name": record.name.value, "congratulation_date": birthday_date.strftime("%Y-%m-%d")})
        result.sort(key=lambda x: x["congratulation_date"])
        return result
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found. Please provide a valid name."
        except ValueError:
            return "Give me correct name and phone please."
        except IndexError:
            return "Please provide the correct number of arguments."
        except Exception:
            return "An unexpected error occurred. Please try again."
    return wrapper

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for contact {name} changed"
    else:
        return f"Contact {name} not found"

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    else:
        finded_phone = record.find_phone()
        if finded_phone:
            return finded_phone
        else:
            return f"No phones for contact {name}"
        
@input_error
def remove_phone(args, book: AddressBook):
    name, phone,  *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    else:
        record.remove_phone(phone)
        return f"Phone number {phone} for contact {name} removed"

@input_error
def show_all(book: AddressBook):
    if len(book) == 0:
        return "You have no contacts yet."   
    else:
        records = []
        for _, record in book.data.items():
            records.append(str(record))
        return records

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for contact {name} changed"
    else:
        return f"Contact {name} not found"
    

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        birthday = record.show_birthday()
        if birthday:
            return f"Birthday for contact {name}: {birthday}"
        else:
            return f"Birthday for contact {name} not provided"
    else:
        return f"Contact {name} not found"

@input_error
def birthdays(book):
    if len(book) == 0:
        return "You have no contacts yet."   
    else:
        birthdays = book.get_upcoming_birthdays()
        if birthdays:
            return birthdays
        else:
            return "No birthdays next week."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))
        
        elif command == "change":
            print(change_contact(args, book))
        
        elif command == "phone":
            print(show_phone(args, book))

        elif command == "remove-phone":
            print(remove_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()