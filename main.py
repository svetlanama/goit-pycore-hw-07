from address_book import AddressBook, Record


book = AddressBook()


john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")


book.add_record(john_record)


jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)


for name, record in book.data.items():
    print(record)


john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)


found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")


book.delete("Jane")

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper

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
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    if record.edit_phone(old_phone, new_phone):
        return "Phone updated."
    return "Phone not found."

@input_error
def show_phones(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    return f"Phones: {', '.join(p.value for p in record.phones)}"

@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "No contacts."
    return '\n'.join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book):
    name, bday, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(bday)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    if not record.birthday:
        return "Birthday not set."
    return f"Birthday for {name}: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book):
    bdays = book.get_upcoming_birthdays()
    if not bdays:
        return "No birthdays in the next 7 days."
    result = []
    for b in bdays:
        result.append(f"{b['name']}: {b['birthday']}")
    return '\n'.join(result)

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

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
            print(show_phones(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main() 