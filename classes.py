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
        removed_phone = self.find_phone(phone)
        if removed_phone:
            self.phones.remove(removed_phone)
            return
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for record_phone in self.phones:
            if str(record_phone) == phone:
                return record_phone
        raise ValueError("Phone number not found")

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


# test
book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_phone("0987654321")
john_record.add_phone("4444444444")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("2222222222")
jane_record.add_phone("7777777771")

book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
jane = book.find("Jane")
john.edit_phone("1234567890", "1112223333")
print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

john.remove_phone("1112223333")
print(john)
john.remove_phone("0987654321")
john.remove_phone("4444444444")
john.remove_phone("5555555555")
print(john)
john.add_birthday("15.06.2020")
jane.add_birthday("17.05.2020")
print(john)

birthdays = book.get_upcoming_birthdays()
print(birthdays)
book.delete("Jane")
book.delete("John")


