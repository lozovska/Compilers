import re
import sys

class Token:
    def __init__(self, name, line, shift, value=None):
        self.name = name
        self.line = line
        self.shift = shift
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.shift = 0

    def has_next(self):
        while self.pos < len(self.text) and self.text[self.pos] == "":
            self.pos += 1
        return self.pos < len(self.text)

    def next_token(self):
        if self.text[self.pos] == "":
            self.pos += 1
            self.shift = 0
        if self.pos >= len(self.text):
            return Token("", 0, 0), ValueError("empty text")

        line = self.text[self.pos]

        while line[0] == ' ':
            line = line[1:]
            self.shift += 1

        str_loc = re.match('^"([^"\\\n]|\\n|\\"|\\t|\\)*\\"', line)
        num_loc = re.match('^\d(\d|_)*', line)

        if str_loc is None and num_loc is None:
            tok = Token("Error", self.pos, self.shift)
            while len(line) > 0 and line[0] != ' ':
                line = line[1:]
                self.shift += 1
                self.text[self.pos] = line
            return tok, None

        if num_loc is None:
            tok = Token("StringLiteral", self.pos, self.shift, line[str_loc.start():str_loc.end()])
            self.shift += len(line[str_loc.start():str_loc.end()])
            self.text[self.pos] = line[str_loc.end():]
            return tok, None

        if str_loc is None:
            tok = Token("NumLiteral", self.pos, self.shift, line[num_loc.start():num_loc.end()])
            self.shift += len(line[num_loc.start():num_loc.end()])
            self.text[self.pos] = line[num_loc.end():]
            return tok, None

        return Token("", 0, 0), ValueError("smth went wrong")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Wrong usage")
        sys.exit(1)

    path_to_file = sys.argv[1]

    try:
        with open(path_to_file, "r") as file:
            lines = file.readlines()
    except IOError as e:
        print(e)
        sys.exit(1)

    lexer = Lexer(lines)
    while lexer.has_next():
        tok, err = lexer.next_token()
        if err is not None:
            print(err)
            sys.exit(1)
        print(tok)
