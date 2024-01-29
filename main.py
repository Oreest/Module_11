from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(str(value)) == 10 and str(value).isdigit():
            super().__init__(value)
        else:
            raise ValueError("Phone must be 10 digits")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.__birthday = None

    def get_birthday(self):
        return self.__birthday
    def set_birthday(self, value):

        today = datetime.now().date()
        birthday = datetime.strptime(value, '%Y-%m-%d').date()
        self.__birthday = birthday

    birthday = property(get_birthday, set_birthday)

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError("This contact doesn't have attribute birthday")

        today = datetime.now().date()
        birthday = datetime(year=today.year, month=self.__birthday.month, day=self.__birthday.day).date()
        if birthday > today:
            days_till_birthday = (birthday - today).days
            return days_till_birthday
        if birthday < today:
            birthday = datetime(year=today.year + 1, month=self.__birthday.month, day=self.__birthday.day).date()
            days_till_birthday = (birthday - today).days
            return days_till_birthday
        if birthday == today:
            return "Todays is the birthday"

    def get_info(self):
        phones_info = ''
        for phone in self.phones:
            phones_info += f'{phone.value}, '
        return f'{self.name.value} : {phones_info[:-2]}'

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def add_phone(self, phone):
        if len(str(phone)) == 10:
            self.phones.append(Phone(phone))
        else:
            raise ValueError("Phone must be 10 digits")

    def edit_phone(self, old_phone, new_phone):
        is_edited = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                is_edited = True
        if not is_edited:
            raise ValueError("No phone edited as phone does not exist")

    def remove_phone(self, phone):
        is_removed = False
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                is_removed = True
        if is_removed:
            return f"{phone}(s)has been removed"
        else:
            raise ValueError("No such phone in this record")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = dict()

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name) -> Record:
        return self.data.get(name)

    def find(self, value):
        if self.has_record(value):
            return self.get_record(value)
        for record in self.get_all_record().values():
            for phone in record.phones:
                if phone.value == value:
                    return record

        # raise ValueError("Contact with this value does not exist.")

    def delete(self, name):
        if self.find(name):
            del self.data[name]

    def iterator(self, count = 5):
        page = []
        i = 0
        for record in self.data.values():
            page.append(record)
            i += 1
            if i == count:
                yield page
                page = []
                i = 0
        if page:
            yield page


def main():
    try:
        book = AddressBook()
        john_record = Record("John")
        print(john_record.get_info())
        john_record.birthday = '2011-01-30'
        print(john_record.birthday)
        print(john_record.days_to_birthday())
        john_record.birthday = '2011-01-18'
        print(john_record.days_to_birthday())
        # john_record.edit_phone('5555555555', '4555555555')
        #
        # john_record.remove_phone("4555555555")
        # print(john_record.get_info())
        # print(john_record.find_phone("4555555555"))
        record_1 = Record('Amy')
        record_2 = Record('Bmy')
        record_3 = Record('Emy')
        record_4 = Record('Cmy')
        record_5 = Record('Dmy')
        record_6 = Record('Dmy')
        book.add_record(john_record)
        book.add_record(record_1)
        book.add_record(record_2)
        book.add_record(record_3)
        book.add_record(record_4)
        book.add_record(record_5)
        book.add_record(record_6)
        book.iterator(count=2)
        # jane_record = Record("Jane")
        # jane_record.add_phone("9876543210")
        # book.add_record(jane_record)
        # for name, record in book.data.items():
        #     print(name, record)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
