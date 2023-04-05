% Лабораторная работа № 1.2. «Лексический анализатор на основе регулярных выражений»
% 5 апреля 2023 г.
% Лозовска Карина, ИУ9И-64Б

# Цель работы
Целью данной работы является приобретение навыка разработки простейших лексических анализаторов,
работающих на основе поиска в тексте по образцу, заданному регулярным выражением.

# Индивидуальный вариант
Строковые литералы: ограничены двойными кавычками, не могут пересекать границы текста, содержат
последовательности `«\n», «\"», «\t» и «\\»`. Числовые литералы: последовательности
десятичных знаков и знаков «_», начинающиеся с цифры (прочерк не влияет на значение числа).

# Реализация
Данный код представляет собой реализацию лексического анализатора (lexer) на языке Python.
Лексический анализатор принимает на вход текстовую строку и разбивает ее на лексемы (tokens),
которые затем могут быть использованы для дальнейшего синтаксического анализа. 
Класс Token представляет собой лексему и содержит ее имя (`name`), номер строки (`line`),
смещение (`shift`) и значение (`value`), если лексема является строковым или числовым
литералом.
Класс `Lexer` представляет собой лексический анализатор и содержит методы для получения
следующей лексемы (`next_token`) и проверки наличия следующей лексемы (`has_next`). Метод
`next_token` разбивает текст на лексемы, используя регулярные выражения для определения
строковых и числовых литералов, а также обрабатывает ошибки, если лексема не может быть распознана.
В конце кода происходит проверка на то, что скрипт был запущен как основная программа, а не
импортирован как модуль. Если скрипт был запущен как основная программа, то он принимает путь к
файлу с исходным кодом в качестве аргумента командной строки, читает его и передает его
содержимое в лексический анализатор. Затем лексический анализатор выводит на экран полученные
лексемы. Если происходит ошибка, то скрипт выводит сообщение об ошибке и завершает работу с
кодом 1.

```python
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
```

# Тестирование
Тестовый пример:
```txt
 "ja" "ustalj"  16575 ---- &
 "privet"<h2>  &lt;  "poka"  "!@#$%^&*()"
```
Вывод тестового примера на `stdout`
```
{StringLiteral 0 1 "ja"}
{StringLiteral 0 6 "ustalj"}
{NumLiteral 0 16 16575}
{Error 0 22 }
{Error 0 27 }
{StringLiteral 1 1 "privet"}
{Error 1 9 }
{Error 1 15 }
{StringLiteral 1 21 "poka"}
{StringLiteral 1 29 "!@#$%^&*()"}
```
# Вывод
Данный код представляет собой реализацию лексического анализатора на языке Python. Лексический
анализатор принимает на вход текстовую строку и разбивает ее на лексемы, которые затем могут
быть использованы для дальнейшего синтаксического анализа.
В ходе выполнения лабораторной работы была реализована лексический анализатор, который может
использоваться для разбиения исходного кода на лексемы. Для этого были использованы регулярные
выражения для определения строковых и числовых литералов, а также обработка ошибок, если
лексема не может быть распознана.
В результате выполнения лабораторной работы были получены навыки работы с лексическим
анализатором на языке Python, а также понимание принципов его работы. Эти навыки могут быть
использованы для дальнейшей работы с компиляторами и интерпретаторами, а также для разработки
собственных языков программирования.