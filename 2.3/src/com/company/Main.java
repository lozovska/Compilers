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
                LexicAnalis ide = new LexicAnalis();
                ArrayList<token> t = ide.main(s,i);
                for (int j = 0; j < t.size(); j++){
                    toks.add(t.get(j));
                }
            }
        }
        catch(IOException ex){
            System.out.println(ex.getMessage());
        }

        token t = new token();
        t.type = "ENDOFFILE";
        toks.add(t);
        SyntaxAnalys parser = new SyntaxAnalys();
        parser.init_table();
        Node tree = parser.topDownParse(toks);
        tree.print("");
    }
}

