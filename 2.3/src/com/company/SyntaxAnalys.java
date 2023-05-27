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
