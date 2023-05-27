% Лабораторная работа № 2.3. «Синтаксический анализатор на основе предсказывающего анализа»
% 27 мая 2023 г.
% Лозовска Карина, ИУ9И-64Б

# Цель работы
Целью данной работы является изучение алгоритма построения таблиц предсказывающего анализатора.

# Индивидуальный вариант
```
/* аксиома помечена звёздочкой */
  F  ("n") 
     ("(" E ")")
  T  (F T')
  T' ("*" F T') ()
* E  (T E')
  E' ("+" T E') ()
```
# Реализация
Реализация состоит из нескольких классов, основные из которых это: ```Main```, ```LexicAnalysis``` и ```SyntaxAnalysis```.
В классе ```Main``` код осуществляет чтение и анализ содержимого файла "test.txt" с помощью лексического и синтаксического анализаторов, и выводит структуру дерева разбора на экран.
```java
package com.company;
import java.io.*;
import java.util.ArrayList;

public class Main {
    public static void main(String args[]){

        int i = 0;
        ArrayList<token> toks = new ArrayList<token>();
        try(BufferedReader br = new BufferedReader(new FileReader("test.txt"))){
            String s;
            while((s=br.readLine())!=null){
                i++;

                // Лексический анализатор
                LexicAnalis ide = new LexicAnalis();

                // Получение списка токенов из текущей строки
                ArrayList<token> t = ide.main(s,i);

                // Добавление токенов в общий список
                for (int j = 0; j < t.size(); j++){
                    toks.add(t.get(j));
                }
            }
        }
        catch(IOException ex){
            System.out.println(ex.getMessage());
        }

        // Создание токена для обозначения конца программы
        token t = new token();
        t.type = "ENDOFFILE";
        toks.add(t);

        // Синтаксический анализатор
        SyntaxAnalys parser = new SyntaxAnalys();

        // Инициализация таблицы разбора
        parser.init_table();

        // Выполнение верхнеуровневого разбора и получение синтаксического дерева
        Node tree = parser.topDownParse(toks);

        // Вывод синтаксического дерева
        tree.print("");
    }
}

```
Класс ```LexicAnalysis``` выполняет лексический анализ текста с помощью регулярных выражений и создает список токенов, которые представлены объектами ```token```.

```java
package com.company;

import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LexicAnalis {

    ArrayList<token> tokens = new ArrayList<token>();
    public void search(String text, int aaa){
        // Регулярные выражения
        String T = "\\s?\"[a-z+*()]*\"";
        String NonT = " ?[A-Z]+'?";
        String AxSign = "\\*\\s";
        String EqSign = "^ {2}(?=\\S)";
        String AltStart = " *\\(";
        String AltEnd = "\\)";
        String comment = "/\\*.*\\*/";
        String pattern = "(?<T>" + T + ")|(?<NonT>" + NonT + ")|" +
                "(?<comment>" + comment + ")|(?<AxSign>" + AxSign + ")|" +
                "(?<EqSign>" + EqSign + ")|(?<AltStart>" + AltStart + ")|" +
                "(?<AltEnd>" + AltEnd + ")";

        // Компиляция регулярного выражения
        Pattern p = Pattern.compile(pattern);
        boolean flag = true;
        int index = 0;
        while (flag) {
            if (text.length() == 0) {
                flag = false;
            } else {
                // Сопоставление текста с регулярным выражением
                Matcher m = p.matcher(text);
                if (m.find()) {
                    if (m.group("comment") != null){
                        if (m.group("comment") == text) {
                            flag = false;
                        }
                        index += m.group("comment").length();
                        text = text.substring(m.group("comment").length());
                    }

                    else if (m.group("AxSign") != null) {
                        if (m.group("AxSign") == text) {
                            flag = false;
                        }
                        token toks = new token();
                        toks.tok = m.group("AxSign");
                        toks.type = "AxSign";
                        index += m.group("AxSign").length();
                        toks.index_str = index;
                        toks.index_file = aaa;
                        this.tokens.add(toks);
                        text = text.substring(m.group("AxSign").length());
                    }

                    else if (m.group("EqSign") != null){
                        if (m.group("EqSign") == text) {
                            flag = false;
                        }
                        token toks = new token();
                        toks.tok = m.group("EqSign");
                        toks.type = "EqSign";
                        index += m.group("EqSign").length();
                        toks.index_str = index;
                        toks.index_file = aaa;
                        this.tokens.add(toks);
                        text = text.substring(m.group("EqSign").length());

                    }

                    else if (m.group("AltStart") != null){
                        if (m.group("AltStart") == text) {
                            flag = false;
                        }
                        token toks = new token();
                        toks.tok = "(";
                        toks.type = "AltStart";
                        index += m.group("AltStart").length();
                        toks.index_str = index;
                        toks.index_file = aaa;
                        this.tokens.add(toks);
                        text = text.substring(m.group("AltStart").length());
                    }

                    else if (m.group("AltEnd") != null){
                        if (m.group("AltEnd") == text) {
                            flag = false;
                        }
                        token toks = new token();
                        toks.tok = m.group("AltEnd");
                        toks.type = "AltEnd";
                        index += m.group("AltEnd").length();
                        toks.index_str = index;
                        toks.index_file = aaa;
                        this.tokens.add(toks);
                        text = text.substring(m.group("AltEnd").length());
                    }

                    else if (m.group("T") != null){
                        if (m.group("T") == text) {
                            flag = false;
                        }
                        token toks = new token();
                        toks.tok = m.group("T");
                        toks.type = "T";
                        index += m.group("T").length();
                        toks.index_str = index;
                        toks.index_file = aaa;
                        this.tokens.add(toks);
                        text = text.substring(m.group("T").length());
                    }

                    else if (m.group("NonT") != null){
                        if (m.group("NonT") == text) {
                            flag = false;
                        }
                        token toks = new token();
                        toks.tok = m.group("NonT");
                        toks.type = "NonT";
                        index += m.group("NonT").length();
                        toks.index_str = index;
                        toks.index_file = aaa;
                        this.tokens.add(toks);
                        text = text.substring(m.group("NonT").length());
                    }
/*
                    else if (m.group("Space") != null){
                        if (m.group("Space") == text) {
                            flag = false;
                        }
                        token toks = new token();
                        toks.tok = m.group("Space");
                        toks.type = "Space";
                        index += m.group("Space").length();
                        toks.index_str = index;
                        toks.index_file = aaa;
                        this.tokens.add(toks);
                        text = text.substring(m.group("Space").length());
                    }
*/
                } else {
                    index++;
                    if (text.charAt(0) != ' ') {
                        System.out.println("syntax error (" + aaa + "," + index + ")");
                    }
                    text = text.substring(1);

                }
            }
        }
    }

    public ArrayList<token> main(String text, int aaa) {
        search(text, aaa);
        return this.tokens;
    }
}
```
Класс ```SyntaxAnalysis``` представляет функциональность для синтаксического анализа и создания синтаксического дерева на основе списка токенов.
```java
package com.company;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Stack;

abstract class Node {
    abstract void print(String indent);
}
class Leaf extends Node{
    token tok;

    public Leaf(token a) {
        this.tok = a;
    }

    void print(String indent) {
        if (tok.type == "T" || tok.type == "NonT"){
            System.out.println(indent + "Leaf: " + tok.type + " " + tok.tok);
        } else {
            System.out.println(indent + "Leaf: " + tok.type);
        }
    }
}
class Inner extends Node {
    String nterm;
    int ruleId;
    ArrayList<Node> children = new ArrayList<>();
    void print(String indent) {
        System.out.println(indent + "Inner node: " + nterm );
        for (int i = 0; i < children.size(); i++){
            Node child = children.get(i);
            child.print(indent + "\t");
        }

    }
}

public class SyntaxAnalys {
    HashMap<String, String[]> crossing = new HashMap<String, String[]>();
    void init_table() {
        this.crossing.put("S AxSign", new String[]{"Axiom", "Rules"});
        this.crossing.put("S NonT", new String[]{"Rules", "S"});
        this.crossing.put("S ENDOFFILE", new String[]{});
        this.crossing.put("Axiom AxSign", new String[]{"AxSign", "NonT", "EqSign", "RightPart"});
        this.crossing.put("Rules NonT", new String[]{"Rule", "Rules"});
        this.crossing.put("Rules AxSign", new String[]{});
        this.crossing.put("Rule NonT", new String[]{"NonT", "EqSign", "RightPart"});
        this.crossing.put("RightPart NonT", new String[]{});
        this.crossing.put("RightPart AxSign", new String[]{});
        this.crossing.put("RightPart AltStart", new String[]{"AltStart", "Altern", "AltEnd", "RightPart"});
        this.crossing.put("Altern T", new String[]{"T", "Altern"});
        this.crossing.put("Altern NonT", new String[]{"NonT", "Altern"});
        this.crossing.put("Altern AltEnd", new String[]{});
    }

    boolean isTerm(String s){
        return !(s == "S" || s == "Axiom" || s == "Rules" || s == "Rule" || s == "RightPart" || s == "Altern");

    }

    Node topDownParse(ArrayList<token> toks) {
        Inner sparent = new Inner();
        Stack<Inner> stackIn = new Stack<>();
        Stack<String> stackStr = new Stack<>();
        stackIn.push(sparent);
        stackStr.push("S");
        int i = 0;
        token a = toks.get(i);
        i++;
        while(i < toks.size() && toks.get(i).type != "ENDOFPROGRAM") {
            Inner parent= stackIn.pop();
            String X = stackStr.pop();
            if (isTerm(X)) {
                if (X.equals(a.type)) {
                    parent.children.add(new Leaf(a));
                    a = toks.get(i);
                    i++;
                    //a.print();
                } else {
                    this.err("Ожидался " + X + ", получен " + a.type, a);
                    //break;
                }
            } else if (crossing.containsKey(X + " " + a.type)) {
                Inner inner = new Inner();
                inner.nterm = X;
                inner.children = new ArrayList<>();
                parent.children.add(inner);
                String[] array = crossing.get(X + " " + a.type);
                for (int j = array.length - 1; j >= 0; j--) {
                    stackIn.push(inner);
                    stackStr.push(array[j]);
                }
            } else {
                this.err("Ожидался " + X + ", получен " + a.type, a);
                //break;
            }
        }
        return sparent.children.get(0);
    }

    void err(String err_str, token tok) {
        System.out.print("(" + tok.index_file + "," + tok.index_str + ") ");
        System.out.println("" + err_str);
    }


}

```

# Тестирование
Тестовый пример:
```txt
F  ("n")
   ("(" E ")")
T  (F T')
T'  ("*" F T') ()
* E  (T E')
E'  ("+" T E') ()
```
Вывод тестового примера на `stdout`:
```
Inner node: S
	Inner node: Rules
		Inner node: Rule
			Leaf: NonT F
			Leaf: EqSign
			Inner node: RightPart
				Leaf: AltStart
				Inner node: Altern
					Leaf: T "n"
					Inner node: Altern
				Leaf: AltEnd
				Inner node: RightPart
					Leaf: AltStart
					Inner node: Altern
						Leaf: T "("
						Inner node: Altern
							Leaf: NonT  E
							Inner node: Altern
								Leaf: T  ")"
								Inner node: Altern
					Leaf: AltEnd
					Inner node: RightPart
		Inner node: Rules
			Inner node: Rule
				Leaf: NonT T
				Leaf: EqSign
				Inner node: RightPart
					Leaf: AltStart
					Inner node: Altern
						Leaf: NonT F
						Inner node: Altern
							Leaf: NonT  T'
							Inner node: Altern
					Leaf: AltEnd
					Inner node: RightPart
			Inner node: Rules
				Inner node: Rule
					Leaf: NonT T'
					Leaf: EqSign
					Inner node: RightPart
						Leaf: AltStart
						Inner node: Altern
							Leaf: T "*"
							Inner node: Altern
								Leaf: NonT  F
								Inner node: Altern
									Leaf: NonT  T'
									Inner node: Altern
						Leaf: AltEnd
						Inner node: RightPart
							Leaf: AltStart
							Inner node: Altern
							Leaf: AltEnd
							Inner node: RightPart
				Inner node: Rules
	Inner node: S
		Inner node: Axiom
			Leaf: AxSign
			Leaf: NonT E
			Leaf: EqSign
			Inner node: RightPart
				Leaf: AltStart
				Inner node: Altern
					Leaf: NonT T
					Inner node: Altern
						Leaf: NonT  E'
						Inner node: Altern
				Leaf: AltEnd
				Inner node: RightPart
		Inner node: Rules
			Inner node: Rule
				Leaf: NonT E'
				Leaf: EqSign
				Inner node: RightPart
					Leaf: AltStart
					Inner node: Altern
						Leaf: T "+"
						Inner node: Altern
							Leaf: NonT  T
							Inner node: Altern
								Leaf: NonT  E'
								Inner node: Altern
					Leaf: AltEnd
					Inner node: RightPart
						Leaf: AltStart
						Inner node: Altern
						Leaf: AltEnd
```
# Вывод
В результате выполнения данной лабораторной работы был реализован синтаксический анализатор на основе предсказывающего анализа. Предсказывающий анализ основан на использовании заранее определенной таблицы разбора, которая содержит информацию о следующем шаге разбора на основе текущего символа входной строки и верхнего символа стека.
Основная задача синтаксического анализатора состоит в проверке синтаксической корректности входного текста путем построения его дерева разбора. Дерево разбора представляет собой структуру, отображающую иерархическую организацию выражений и операторов в исходном коде.
В целом, разработка синтаксического анализатора на основе предсказывающего анализа является важным шагом в создании компиляторов, интерпретаторов и других инструментов для обработки и анализа языков программирования. Дальнейшая работа может включать завершение реализации синтаксического анализатора, включая таблицу разбора, а также тестирование и оптимизацию его работы.
