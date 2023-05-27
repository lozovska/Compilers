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