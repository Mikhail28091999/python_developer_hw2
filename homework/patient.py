import logging
from datetime import datetime
from calendar import monthrange
import csv
import os


def csv_writer(data, path):
    with open(path, "a", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


class Logging:
    def __init__(self, name, level, file):
        self.level = level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handler = logging.FileHandler(file, 'a', 'utf-8')
        formatter = logging.Formatter("[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(name)s  %(message)s")
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def write(self, string):
        self.additional_func(string)
        self.handler.close()

    def additional_func(self, string):
        if self.level == 'ERROR':
            return self.logger.error(string)
        else:
            return self.logger.info(string)


##################################
##################################
class Patient:
    _info = Logging('info', 'INFO', 'Information.log')
    _err = Logging('error', 'ERROR', 'Errors.log')

    ##################################
    def __init__(self, first_name, last_name, birth_date, phone, document_type, document_id):
        self._first_name = self.check_name(first_name)
        self._last_name = self.check_name(last_name)
        self._birth_date = self.check_birth_date(birth_date)
        self._phone = self.check_phone(phone)
        self._document_type = self.check_document_type(document_type)
        self._document_id = self.check_document_id(document_id)
        self._info.write(f"New user: {self._first_name, self._last_name, self._birth_date,}")

    ##################################
    @classmethod
    def create(cls, first_name, last_name, birth_date, phone, document_type, document_id):
        return Patient(first_name, last_name, birth_date, phone, document_type, document_id)

    ##################################
    def __getattr__(self, item):
        return 0

    ##################################
    def name_client(self):
        name = 'Client'
        if self._last_name and self._first_name:
            name = f"{self._last_name + ' ' + self._first_name}"
        return name

    ##################################
    def check_phone(self, phone):
        if not isinstance(phone, str):
            self._err.write(f'{phone} should be str: {self.name_client()}')
            raise TypeError("Phone number should be str")
        letters = '+( )-0123456789'
        number = []
        for symbol in phone:
            if symbol not in list(letters):
                self._err.write(f'{phone} is not number of phone: {self.name_client()}')
                raise ValueError(f"{phone} is not number of phone")
            try:
                number = number + [int(symbol)]
            except ValueError:
                continue
        if (number[0] == 7 or number[0] == 8) and len(number) == 11:
            number[0] = 7
            example = ['+', '#', ' ', '(', '#', '#', '#', ')', ' ', '#', '#', '#', '-', '#', '#', '-', '#', '#']
            i = 0
            phone = ''
            for j in range(0, len(example)):
                if example[j] == '#':
                    example[j] = str(number[i])
                    i = i + 1
                phone = phone + example[j]
            return phone
        else:
            self._err.write(f'{phone} is not number of phone: {self.name_client()}')
            raise ValueError(f"{phone} is not number of phone")

    ##################################
    def check_name(self, name):
        if not isinstance(name, str):
            self._err.write(f'{name} should be str: {self.name_client()}')
            raise TypeError("First name or last name should be str")
        if not name.isalpha():
            self._err.write(f'{name} should consist of letters: {self.name_client()}')
            raise ValueError('First name or last name should consist of letters')
        name = name.capitalize()
        return name

    ##################################
    def check_birth_date(self, birth_date):
        if not isinstance(birth_date, str):
            self._err.write(f'{birth_date} should be str: {self.name_client()}')
            raise TypeError("Birth date should be str")
        letters = ' -0123456789'
        date = []
        for symbol in birth_date:
            if symbol not in list(letters):
                self._err.write(f'{birth_date} is not date of birth: {self.name_client()}')
                raise ValueError(f"{birth_date} is not date of birth")
            try:
                date = date + [int(symbol)]
            except ValueError:
                continue
        if len(date) == 8:
            year = month = day = ''
            for num in date[0:4]:
                year = year + str(num)
            for num in date[4:6]:
                month = month + str(num)
            for num in date[6:8]:
                day = day + str(num)
            if int(year) < 1850:
                self._err.write(f'There are no so old people in Russia! {self.name_client()}')
                raise ValueError('There are no so old people in Russia!')
            if int(month) > 12:
                self._err.write(f'There are only 12 month! {self.name_client()}')
                raise ValueError('There are only 12 month!')
            if int(day) > monthrange(int(year), int(month))[1]:
                self._err.write(f'There are no so many days in this month! {self.name_client()}')
                raise ValueError('There are no so many days in this month!')
            if datetime(int(year), int(month), int(day)) > datetime.now():
                self._err.write(f'There are no people from future! {self.name_client()}')
                raise ValueError('There are no people from future!')
            birth_date = year + '-' + month + '-' + day
            return birth_date
        else:
            self._err.write(f'{birth_date} is not date of birth: {self.name_client()}')
            raise ValueError(f"{birth_date} is not date of birth")

    ##################################
    def check_document_type(self, document_type):
        if not isinstance(document_type, str):
            self._err.write(f'{document_type} should be str: {self.name_client()}')
            raise TypeError("Document type should be str")
        document_type = document_type.lower()
        if document_type == 'passport' or document_type == 'international passport' or document_type == "driver's license":
            return document_type
        else:
            self._err.write(f'{document_type} is not type of document: {self.name_client()}')
            raise ValueError("It is not type of document")

    ##################################
    def check_document_id(self, document_id):
        if not isinstance(document_id, str):
            self._err.write(f'{document_id} should be str: {self.name_client()}')
            raise TypeError("Document id should be str")
        letters = '1234567890/- '
        id = []
        for symbol in document_id:
            if symbol not in list(letters):
                self._err.write(f'{document_id} is not id: {self.name_client()}')
                raise ValueError(f"{document_id} is not id")
            try:
                id = id + [int(symbol)]
            except ValueError:
                continue
        if self._document_type == 'passport':
            series = number = ''
            for num in id[0:4]:
                series = series + str(num)
            for num in id[4:10]:
                number = number + str(num)
            return series + ' ' + number
        elif self._document_type == 'international passport':
            series = number = ''
            for num in id[0:2]:
                series = series + str(num)
            for num in id[2:9]:
                number = number + str(num)
            return series + ' ' + number
        elif self._document_type == "driver's license":
            series1 = series2 = number = ''
            for num in id[0:2]:
                series1 = series1 + str(num)
            for num in id[2:4]:
                series2 = series2 + str(num)
            for num in id[4:10]:
                number = number + str(num)
            return series1 + ' ' + series2 + ' ' + number

    ##################################
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._err.write(f'Attempt to change name: {self.name_client()}')
        raise AttributeError('''Don't change name!''')

    ##################################
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._err.write(f'Attempt to change name: {self.name_client()}')
        raise AttributeError('''Don't change name!''')

    ##################################
    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date):
        self._birth_date = self.check_birth_date(birth_date)
        self._info.write(f'You changed date of birth: {self.name_client()}')

    ##################################
    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = self.check_phone(phone)
        self._info.write(f'You changed number of phone: {self.name_client()}')

    ##################################
    @property
    def document_type(self):
        return self._document_type

    @document_type.setter
    def document_type(self, document_type):
        self._document_type = self.check_document_type(document_type)
        self._info.write(f'You changed document type: {self.name_client()}')

    ##################################
    @property
    def document_id(self):
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        self._document_id = self.check_document_id(document_id)
        self._info.write(f'You changed document id: {self.name_client()}')

    ##################################
    def save(self):
        csv_writer([[self._first_name, self._last_name, self._birth_date,
                              self._phone, self._document_type, self._document_id]], 'Patient.csv')
        self._info.write(f'User saved in csv-file: {self.name_client()}')

##################################
##################################


class Iterator:
    def __init__(self, path_to_file, lim=None):
        self._path_to_file = path_to_file
        self._lim = lim
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        with open(self._path_to_file, newline='', encoding='utf-8') as File:
            reader = csv.reader(File)
            clients = []
            for row in reader:
                clients.append(Patient(*row))
        if len(clients) == 0:
            raise StopIteration
        if self._lim is None or self._lim > len(clients):
            if self._index < len(clients):
                self._index += 1
                return clients[self._index - 1]
            else:
                raise StopIteration
        elif self._lim < 0:
            raise ValueError('Size of massive > 0 !')
        elif self._lim == 0:
            raise StopIteration
        else:
            if self._index < self._lim:
                self._index += 1
                return clients[self._index - 1]
            else:
                raise StopIteration


class PatientCollection:
    def __init__(self, path_to_file):
        if os.path.isfile(path_to_file):
            self.path_to_file = path_to_file
        else:
            raise FileExistsError("File don't exist")

    def __iter__(self):
        return Iterator(self.path_to_file)

    def limit(self, lim):
        return Iterator(self.path_to_file, lim)

