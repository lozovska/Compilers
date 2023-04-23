% Лабораторная работа № 1.5. «Объектно-ориентированный лексический анализатор»
% 23 апреля 2023 г.
% Лозовска Карина, ИУ9И-64Б

# Цель работы
Целью данной работы является изучение генератора лексических анализаторов flex.

# Индивидуальный вариант
Идентификаторы: последовательности латинских букв и цифр, начинающиеся с буквы. Строковые
константы — последовательности строковых секций, записанных слитно. Строковые секции: либо
последовательность символов, ограниченных апострофами, апостроф внутри строки описывается как
два апострофа подряд, не пересекают границы строк текста, либо знак «#», за которым следует
десятичная константа (код символа). Пример строковой константы: «'hello'#10#13'world'» (эта
строковая константа состоит из 4 строковых секций, однако является единым токеном).

# Реализация
Данный код является спецификацией лексера, написанной на языке `Flex`. Лексер считывает входной
текст и производит поток токенов, которые передаются парсеру для дальнейшей обработки.
Спецификация лексера определяет набор правил для распознавания токенов во входном тексте.
Каждое правило состоит из шаблона для сопоставления и действия, которое выполняется при
распознавании шаблона. Шаблоны являются регулярными выражениями, которые описывают структуру
входного текста.

```flex
%option noyywrap bison-bridge bison-locations
%{
    #include <stdio.h>
    #include <stdlib.h>

    #define TAG_IDENT 1
    #define TAG_STRING 2

    char *tag_names[] = { "END_OF_PROGRAM", "IDENT", "STRING" };

    typedef struct Position Position;
    struct Position {
        int line, pos, index;
    };

    void print_pos(Position *p) {
        printf("(%d,%d)",p->line,p->pos);
    }

    struct Fragment {
        Position starting, following;
    };

    typedef struct Fragment YYLTYPE;
    typedef struct Fragment Fragment;
    void print_frag(Fragment* f) {
    	print_pos(&(f->starting));
    	printf("-");
    	print_pos(&(f->following));
    }

    union Token {
        char *string_literal;
        int ident_num;
        double value;
    };

    typedef union Token YYSTYPE;

    int continued;
    struct Position cur;
    #define YY_USER_ACTION {             \
        int i;                           \
        if (!continued)                  \
            yylloc->starting = cur;      \
        continued = 0;                   \
        for ( i = 0; i < yyleng; i++){   \
            if ( yytext[i] == '\n'){     \
                cur.line++;              \
                cur.pos = 1;             \
            }                            \
            else                         \
                cur.pos++;               \
            cur.index++;                 \
        }                                \
        yylloc->following = cur;         \
    } 


    void init_scanner (char *program){
        continued = 0;
        cur.line = 1;
        cur.pos = 1;
        cur.index = 0;
        yy_scan_string(program);
    }

    void err (char *msg){
        printf ("Error");
        print_pos(&cur);
        printf(":%s\n",msg);
    }

    int lexem_size;

    typedef struct{
        int size;
        char** names;
    } identTabel;

    void create_ident_tabel(identTabel * t){
        t->size = 0;
        t->names = NULL;
    }

    int add_ident(identTabel* tabel, char* name){
        for (int i = 0; i < tabel->size; i++){
            if (strcmp(name, tabel->names[i]) == 0){
                return i;
            }
        }

        tabel->size++;
        if (tabel->size == 1){
            tabel->names = (char**)malloc(sizeof(char*) * (tabel->size));
        }
        else {
            tabel->names = (char**)realloc(tabel->names, sizeof(char*) * (tabel->size));
        }
        tabel->names[tabel->size - 1] = (char*)malloc(sizeof(char)*strlen(name));
        strcpy(tabel->names[tabel->size - 1], name);
        return tabel->size-1;
    }

    identTabel tabel;
    
%}

IDENT [a-zA-Z][a-zA-Z0-9]*

%x STRING SYMBOL_CODE START

%%

[\n\t ]+

'          	        {
						 BEGIN(STRING); 
						 continued = 1; 
						 lexem_size = 1;
						 yylval->string_literal=(char*)malloc(1*sizeof(char));
                         strcpy(yylval->string_literal, "\0");
                    }

#                   {
                        BEGIN(SYMBOL_CODE); 
						continued = 1; 
						lexem_size = 1;
						yylval->string_literal=(char*)malloc(1*sizeof(char));
                        strcpy(yylval->string_literal, "\0");
                    }

<START>#            {
                        BEGIN(SYMBOL_CODE); 
						continued = 1; 
                    }

<START>'            {
                        BEGIN(STRING); 
						continued = 1; 
                    }

<STRING>\n          { 
                        continued = 1;
                        err("Error: newline in string");
                    }     

<STRING><<EOF>>     {
                        err("found EOF but \"'\" expected");
                        return 0;
                    }

<STRING>[^'\n]*    {
                        continued = 1;
                        lexem_size += yyleng;
                        if (lexem_size == yyleng){
                            yylval->string_literal=(char*)malloc(yyleng*sizeof(char));
                        } else { 
                            yylval->string_literal=(char*)realloc(yylval->string_literal,lexem_size*sizeof(char));
                        }
                        strcat(yylval->string_literal,yytext);
                    }

<STRING>''          {
                        continued = 1;
                        lexem_size += 1;
                        if (lexem_size == 1){
                            yylval->string_literal=(char*)malloc(1*sizeof(char));
                        } else { 
                            yylval->string_literal=(char*)realloc(yylval->string_literal,
                            lexem_size*sizeof(char));
                        }
                        strcat(yylval->string_literal,"'");
                    }

<SYMBOL_CODE>[0-9]+ {
                        continued = 1;
                        lexem_size += sizeof(yytext);
                        yylval->string_literal=(char*)realloc(yylval->string_literal,
                        lexem_size*sizeof(char));
                        int code = atoi(yytext);
                        if (code > 255) {
                            err("invalid character code");
                            strcat(yylval->string_literal, 0);
                        } else {
                            char str[2];
                            str[0] = (char)code;
                            str[1] = '0';
                            strncat(yylval->string_literal, str, 1);
                        }
                        BEGIN(START);
                    }

<STRING>'#          {
                        BEGIN(SYMBOL_CODE);
                        continued = 1;
                    }

<STRING>['\n*]|['\s*] { 
                        BEGIN(0);
                        return TAG_STRING; 
                    }
                      
{IDENT}               { 
                        yylval->ident_num = add_ident(&tabel, yytext);
                        return TAG_IDENT;
                      }

.                     err ("ERROR unknown symbol");

<<EOF>>               return 0;


%%

int main(){
    int tag;
    YYSTYPE value;
    YYLTYPE coords;
   	FILE *inputfile;
	long size_str;
	char *str;
	union Token token;
	{
        inputfile = fopen("input.txt","r");
        if (inputfile == NULL) {
            fputs("File not found", stderr);
            exit(1);
        }
        fseek(inputfile, 0,SEEK_END);
        size_str = ftell(inputfile);
        rewind(inputfile);

        str=(char*)malloc(sizeof(char)*(size_str+1));
        if (str == NULL) {
            fputs("Memory error",stderr);
            exit(2);
        }    
        size_t n = fread(str,sizeof(char),size_str,inputfile);
        if (n != size_str) {
            fputs ("Reading error",stderr);
            exit (3);
        }
    }

    str[size_str] = '\0';
    fclose (inputfile);
    init_scanner(str);
    create_ident_tabel(&tabel);
    do{
        tag = yylex(&value,&coords);
        if (tag == 0)
            break;

        printf("%s ",tag_names[tag]);
        print_frag(&coords);
        
        
        if (tag == TAG_STRING){
            printf(": %s", value.string_literal); 
            free(value.string_literal);   
        }

        if (tag == TAG_IDENT){
            printf(": %d", value.ident_num); 
        } 

        printf("\n");        
    }
    while (tag != 0); 
    
    printf("\nIDENT TABEL:\n");
    for (int i = 0; i < tabel.size; i++){
        printf("    %d -> %s\n", i, tabel.names[i]);
        free(tabel.names[i]);
    }
    free(tabel.names);

	free(str);
    return 0;
}
```

# Тестирование
Тестовый пример:
```txt
'hello'#10#32'world''s' 'kuku'
z0u0u0u0 0iiiis0 z z
```
Вывод тестового примера на `stdout`
(`#10 = \n, #32 = \s`)
```
STRING (1,1)-(1,24): hello
 world's
STRING (1,25)-(1,31): kuku
IDENT (2,1)-(2,9): 0
Error(2,11):ERROR unknown symbol
IDENT (2,11)-(2,17): 1
IDENT (2,18)-(2,19): 2
IDENT (2,20)-(2,21): 2
```
# Вывод
В ходе выполнения лабораторной работы было изучено использование генератора лексических
анализаторов flex для создания лексического анализатора на языке C. 
Flex позволяет определить набор правил для распознавания лексем во входном потоке данных и
генерирует соответствующий код на языке C или C++. Это позволяет создавать эффективные и
быстрые лексические анализаторы для различных языков программирования и других форматов данных.
В процессе работы были изучены основные конструкции языка flex, такие как определение
регулярных выражений, правил для обработки лексем и действий, которые выполняются при
обнаружении соответствующей лексемы.
Была создана программа на языке C, использующая лексический анализатор, созданный с помощью
flex. Программа успешно выполняла задачу, для которой была создана.
Таким образом, использование генератора лексических анализаторов flex позволяет создавать
эффективные и быстрые лексические анализаторы на языке C или C++, что может быть полезно при
разработке программного обеспечения, работающего с различными форматами данных.