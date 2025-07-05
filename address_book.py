from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return isinstance(value, str) and value.isdigit() and len(value) == 10

class Birthday(Field):
    def __init__(self, value):
        try:
            if isinstance(value, str):
                date_obj = datetime.strptime(value, "%d.%m.%Y")
            elif isinstance(value, datetime):
                date_obj = value
            else:
                raise ValueError
            super().__init__(date_obj)
        except Exception:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        bday = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{bday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year).date()

                if bday_this_year < today:
                    bday_this_year = record.birthday.value.replace(year=today.year + 1).date()
                if today <= bday_this_year < next_week:
                    birthdays.append({
                        "name": record.name.value,
                        "birthday": bday_this_year.strftime('%d.%m.%Y')
                    })
        return birthdays 