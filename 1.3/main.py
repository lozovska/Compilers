class Position_and_Symbol:
    pos = 0
    line = 0
    index = 0

    def __init__(self, text):
        self.text = text
        self.line = 1
        self.pos = 1
        self.index = 0

    def __pos__(self):
        if self.index < len(self.text):
            if self.is_newline():
                self.line += 1
                self.pos = 0
            else: self.pos += 1
            self.index += 1
        return self

    def __neg__(self):
        if (self.index - 1) >= 0:
            self.pos -= 1
            self.index -= 1
        return self

    def ToString(self): return "(" + str(self.line) + "," + str(self.pos) + ")"

    def get_next(self):
        if self.index == len(self.text): return -1
        else: return self.text[self.index]

    def is_space(self):
        if self.text[self.index] == " ": return True
        else: return False

    def is_newline(self):
        if self.text[self.index] == "\n": return True
        else: return False

    def is_decimal(self):
        if (self.text[self.index] >= '0') and (self.text[self.index] <= '9'): return True
        else: return False

    def is_char(self):
        if ((self.text[self.index] >= 'a') and (self.text[self.index] <= 'z')) \
                or ((self.text[self.index] >= 'A') and (self.text[self.index] <= 'Z')):
            return True
        else:
            return False

    def is_and(self):
        if ((self.index + 2) < len(self.text)) and (self.text[self.index] == 'a') and (
                self.text[self.index + 1] == 'n') and (self.text[self.index + 2] == 'd'):
            return True
        else: return False

    def is_or(self):
        if ((self.index + 1) < len(self.text)) and (self.text[self.index] == 'o') and (
                self.text[self.index + 1] == 'r'):
            return True
        else: return False

    def is_zero(self):
        if self.text[self.index] == '0': return True
        else: return False

    def get_notation(self):
        if self.text[self.index] == 'b': return 2
        elif self.text[self.index] == 't': return 8
        elif self.text[self.index] == 'x': return 16
        else: return -1

    def check_2notation(self):
        if (self.text[self.index] >= '0') and (self.text[self.index] <= '1'): return True
        else: return False

    def check_8notation(self):
        if (self.text[self.index] >= '0') and (self.text[self.index] <= '7'): return True
        else: return False

    def check_16notation(self):
        if (self.text[self.index] >= '0') and (self.text[self.index] <= '9') and (
                (self.text[self.index] >= 'a') and (self.text[self.index] <= 'f')) or (
                (self.text[self.index] >= 'A') and (self.text[self.index] <= 'F')):
            return True
        else: return False

    def clone(self, f = False):
        result = Position_and_Symbol(self.text)
        if f == False:
            result.pos = self.pos
            result.index = self.index
            result.line = self.line
        else:
            result.pos = self.pos
            result.index = self.index + 1
            result.line = self.line
        return result

    def return_string(self, t1, t2):
        if t1.index == t2.index: return self.text[t1.index]
        return (self.text[t1.index:t2.index])

# Starting - array
class Part:
    def __init__(self, current, next):
        self.Starting = current
        self.Following = next

    def ToString(self):
        return '(' + str(self.Starting[0]) + ', ' + str(self.Starting[1]) + ")-(" \
            + str(self.Following[0]) + " ," + str(self.Following[1]) + ")"

# Добавляем класс IdentToken/Number/so on
class Message:
    def __init__(self, isError, text):
        self.isError = isError
        self.text = text

class Token:
    def __init__(self, tag, first, last):
        self.tag = tag
        start = [first.pos, first.line]
        end = [last.pos, last.line]
        self.Coords = Part(start, end)

class IdentToken(Token):
    def __init__(self, code, first, last):
        self.Ident = Token(Tags[0], first, last)
        self.Val = code

class NumberToken(Token):
    def __init__(self, val, first, last):
        self.Ident = Token(Tags[1], first, last)
        self.Val = val

class NumberKeyWordToken(Token):
    def __init__(self, val, first, last):
        self.Ident = Token(Tags[3], first, last)
        self.Val = val

class NumberAssign(Token):
    def __init__(self, val, first, last):
        self.Ident = Token(Tags[2], first, last)
        self.Val = val

class ErrorToken(Token):
    def __init__(self, val, first, last):
        self.Ident = Token(Tags[5], first, last)
        self.Val = val

# Нужен, чтобы взять позицию
class Scanner:
    def __init__(self, program, compiler):
        self.program = program
        self.compiler = compiler

    def scan(self):
        self.cur = Position_and_Symbol(self.program)

    def func(self, start):
        self.cur = -self.cur
        end = self.cur.clone(True)
        self.cur = +self.cur
        return ErrorToken(self.cur.return_string(start, end), start, end)

    @property
    def next_token(self):
        start = self.cur.clone()
        end = self.cur.clone(True)
        flag = 0
        while self.cur.get_next() != -1:
            ###### пробелы ######
            while self.cur.is_space():
                if flag == 1: return self.func(start)
                self.cur = +self.cur
                if self.cur.get_next() == -1: break

            if self.cur.get_next() == -1: break

            ###### новая строка ######
            while self.cur.get_next() == '\n':
                if flag == 1: return self.func(start)
                self.cur = +self.cur
                if self.cur.get_next() == -1: break

            if self.cur.get_next() == -1: break

            ###### скобки ######
            if (self.cur.get_next() == '(') or (self.cur.get_next() == ')'):
                if flag == 1: return self.func(start)
                start = self.cur.clone()
                self.cur = +self.cur
                return NumberKeyWordToken(self.cur.return_string(start, start), start, start)

            ###### нуль ######
            elif self.cur.get_next() == '0':
                if flag == 1: return self.func(start)
                start = self.cur.clone()
                self.cur = +self.cur
                if (self.cur.get_next() == -1) or (self.cur.get_next() == '\n') or (self.cur.get_notation() == -1):
                    return NumberToken(self.cur.return_string(start, start), start, start)
                else:
                    ###### 2 CC ######
                    if self.cur.get_notation() == 2:
                        self.cur = +self.cur
                        if (self.cur.get_next() != -1) and (self.cur.check_2notation()) and (self.cur.get_next() != '\n'):
                            while True:
                                end = self.cur
                                self.cur = +self.cur
                                if (self.cur.check_2notation() == False) or (self.cur.get_next() == -1) \
                                        or (self.cur.get_next() == '\n') or (self.cur.is_space()):
                                    break
                            return NumberToken(self.cur.return_string(start, end), start, end)
                        else:
                            self.cur = -self.cur
                            return NumberToken(self.cur.return_string(start, start), start, start)

                    ###### 8 СС ######
                    if self.cur.get_notation() == 8:
                        self.cur = +self.cur
                        if (self.cur.get_next() != -1) and (self.cur.check_8notation()) and (self.cur.get_next() != '\n'):
                            while True:
                                end = self.cur.clone(True)
                                self.cur = +self.cur
                                if (self.cur.get_next() == -1) or (self.cur.check_8notation() == False) \
                                        or (self.cur.get_next() == '\n') or (self.cur.is_space()):
                                    break
                            return NumberToken(self.cur.return_string(start, end), start, end)
                        else:
                            self.cur = -self.cur
                            return NumberToken(self.cur.return_string(start, start), start, start)

                    ###### 16 CC ######
                    if self.cur.get_notation() == 16:
                        self.cur = +self.cur
                        if (self.cur.get_next() != -1) and (self.cur.check_16notation()) and (self.cur.get_next() != '\n'):
                            while True:
                                end = self.cur.clone(True)
                                self.cur = +self.cur
                                if (self.cur.get_next() == -1) or (self.cur.check_16notation() == False) \
                                        or (self.cur.get_next() == '\n') or (self.cur.is_space()):
                                    break
                            return NumberToken(self.cur.return_string(start, end), start, end)
                        else:
                            self.cur = -self.cur
                            return NumberToken(self.cur.return_string(start, start), start, start)

            ###### десятичные ######
            elif self.cur.is_decimal():
                if flag == 1: return self.func(start)
                start = self.cur.clone()
                while True:
                    end = self.cur.clone(True)
                    self.cur = +self.cur
                    if (self.cur.get_next() == -1) or (self.cur.is_decimal() == False) \
                            or (self.cur.get_next() == '\n') or (self.cur.is_space()):
                        break
                return NumberToken(self.cur.return_string(start, end), start, end)

            ###### символы ######
            elif self.cur.is_char():
                if flag == 1:
                    end = -self.cur.clone(True)
                    self.cur = +self.cur
                    return ErrorToken("", start, end)
                if self.cur.is_and():
                    start = self.cur
                    end = ++self.cur
                    self.cur = +self.cur
                    return NumberAssign('and', start, end)
                elif self.cur.is_or():
                    start = self.cur
                    end = +self.cur
                    self.cur = +self.cur
                    return NumberAssign('or', start, end)
                else:
                    start = self.cur.clone()
                    while True:
                        end = self.cur.clone(True)
                        self.cur = +self.cur
                        if (self.cur.get_next() == -1) or (self.cur.is_char() == False) or (self.cur.get_next() == '\n') or (
                        self.cur.is_space()):
                            break
                    return IdentToken(self.cur.return_string(start, end), start, end)
            else:
                if flag == 1: end = self.cur.clone(True)
                if flag == 0: start = self.cur.clone()
                flag = 1
                self.cur = +self.cur
        if flag == 1: return ErrorToken(self.cur.return_string(start, end), start, end)
        if self.cur.get_next() == -1: return -1


# text-NumberAssign/And so on
class Compiler:
    def __init__(self, messages, nameCodes, names, program):
        self.messages = messages
        self.nameCodes = nameCodes
        self.names = names
        self.program = program

    def add_message(self, isErr, text):
        self.messages.append(Message(isErr, text))

    def output(self):
        for word in self.messages:
            print(word.text.Ident.tag + " " + word.text.Ident.Coords.ToString() + ': ' + word.text.Val)


Tags = {
    0: 'IDENT',
    1: 'NUMBER',
    2: 'KEY WORD',
    3: 'ASSIGN',
    4: 'END OF PROGRAMM',
    5: 'ERROR'
}

nameCodes = {}
names = []
message = []

text = '0xAAA %100 hello# andhi((\n)) kukuuu'
compiler = Compiler(message, nameCodes, names, text)
scanner = Scanner(text, compiler)
scanner.scan()

while True:
    next_token = scanner.next_token
    if next_token == -1: break
    if isinstance(next_token, ErrorToken): compiler.add_message(True, next_token)
    else: compiler.add_message(False, next_token)

compiler.output()
