import subprocess


class User:
    user_id = ''
    password = ''
    user_name = ''
    privilege = 0
    select_ISBN = ' '

    def __init__(self, user_id, password, user_name, privilege, ISBN):
        self.user_id = user_id
        self.password = password
        self.user_name = user_name
        self.privilege = privilege
        self.select_ISBN = ISBN


class Book:
    ISBN = ''
    name = ''
    author = ''
    keyword = ''
    price = 0
    stock = 0

    def __init__(self, ISBN, name, author, keyword, price, stock):
        self.ISBN = ISBN
        self.name = name
        self.author = author
        self.keyword = keyword
        self.price = price
        self.stock = stock


class Command:
    # proc = subprocess.Popen(['wsl', './bin/core'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc = subprocess.Popen(['./bin/core.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    current_user = User('visitor', '', 'visitor', 0, ' ')

    def io(self, input_str):
        self.proc.stdin.write(input_str.encode())
        self.proc.stdin.flush()
        res = []
        line = ''
        while line != 'Success\n' and line != 'Invalid\n':
            line = self.proc.stdout.readline().decode().replace('\r\n', '\n')
            res.append(line)
        return res

    def io_text(self, input_str):
        self.proc.stdin.write(input_str.encode())
        self.proc.stdin.flush()
        res = ''
        line = ''
        while line != 'Success\n' and line != 'Invalid\n':
            line = self.proc.stdout.readline().decode().replace('\r\n', '\n')
            res += line
        return res

    def end(self):
        self.proc.stdin.write(b'exit\n')

    def check_privilege(self, privilege):
        return self.current_user.privilege >= privilege

    def get_current_user(self):
        res = self.io('$get_account\n')
        if res[0] == 'visitor\n':
            self.current_user.user_id, \
            self.current_user.password, \
            self.current_user.user_name, \
            self.current_user.privilege, \
            self.current_user.select_ISBN = 'visitor', '', 'visitor', 0, ' '
        else:
            arr = res[0].split('\t')
            self.current_user.user_id, \
            self.current_user.password, \
            self.current_user.user_name, \
            self.current_user.privilege, \
            self.current_user.select_ISBN = arr[0], arr[1], arr[2], int(arr[3]), arr[4]

    def login(self, user_id="", password=""):
        res = self.io('su ' + user_id + ' ' + password + '\n')
        if res[0] == 'Invalid\n':
            return True, False
        else:
            self.get_current_user()
            return False, True

    def logout(self):
        self.io('logout\n')
        self.get_current_user()

    def register(self, user_id="", password="", user_name=""):
        res = self.io('register ' + user_id + ' ' + password + ' ' + user_name + '\n')
        if res[0] == 'Invalid\n':
            return True, False
        else:
            return False, True

    def add_user(self, user_id="", password="", privilege="", user_name=""):
        res = self.io('useradd ' + user_id + ' ' + password + ' ' + privilege + ' ' + user_name + '\n')
        if res[0] == 'Invalid\n':
            return True, False
        else:
            return False, True

    def modify_password(self, user_id="", cur_password="", new_password=""):
        res = self.io('passwd ' + user_id + ' ' + cur_password + ' ' + new_password + '\n')
        if res[0] == 'Invalid\n':
            return True, False
        else:
            return False, True

    def delete(self, user_id=""):
        res = self.io('delete ' + user_id + '\n')
        if res[0] == 'Invalid\n':
            return True, False
        else:
            return False, True

    def show(self, ISBN="", name="", author="", keyword=""):
        s = 'show'
        if ISBN is not None:
            s += ' -ISBN=' + ISBN
        elif name is not None:
            s += ' -name=\"' + name + '\"'
        elif author is not None:
            s += ' -author=\"' + author + '\"'
        elif keyword is not None:
            s += ' -keyword=\"' + keyword + '\"'
        s += '\n'
        res = self.io(s)
        if res[0] == 'Invalid\n':
            return True, False, []
        else:
            books = []
            for line in res:
                if line == '\n':
                    continue
                if line == 'Success\n':
                    break
                arr = []
                pos = 0
                while True:
                    new_pos = line.find('\t', pos)
                    if new_pos == -1:
                        arr.append(line[pos:len(line) - 1])
                        break
                    else:
                        arr.append(line[pos:new_pos])
                    pos = new_pos + 1
                book = Book(arr[0], arr[1], arr[2], arr[3], arr[4], int(arr[5]))
                books.append(book)
            return False, True, books

    def select(self, ISBN=""):
        res = self.io('select ' + ISBN + '\n')
        if res[0] == 'Invalid\n':
            return True, False
        else:
            self.current_user.select_ISBN = ISBN
            return False, True

    def modify(self, ISBN="", name="", author="", keyword="", price=""):
        s = 'modify'
        if ISBN is not None:
            s += ' -ISBN=' + ISBN
        if name is not None:
            s += ' -name=\"' + name + '\"'
        if author is not None:
            s += ' -author=\"' + author + '\"'
        if keyword is not None:
            s += ' -keyword=\"' + keyword + '\"'
        if price is not None:
            s += ' -price=' + price
        s += '\n'
        res = self.io(s)
        if res[0] == 'Invalid\n':
            return True, False
        else:
            return False, True

    def buy(self, ISBN="", quantity=""):
        res = self.io('buy ' + ISBN + ' ' + quantity + '\n')
        if res[0] == 'Invalid\n':
            return True, False, ""
        else:
            return False, True, res[0].strip()

    def import_book(self, quantity="", total_cost=""):
        res = self.io('import ' + quantity + ' ' + total_cost + '\n')
        if res[0] == 'Invalid\n':
            return True, False
        else:
            return False, True

    def show_finance(self, count=""):
        s = 'show finance '
        if count is not None:
            s += count
        s += '\n'
        res = self.io(s)
        if res[0] == 'Invalid\n':
            return True, False, ""
        else:
            return False, True, res[0]

    def report_finance(self):
        res = self.io_text('report finance\n')
        return True, res

    def report_employee(self):
        res = self.io_text('report employee\n')
        return True, res

    def log(self):
        res = self.io_text('log\n')
        return True, res
