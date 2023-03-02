package main

import (
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"os"
	"strconv"
	"strings"
)

func insertIntVar(file *ast.File, name string, value int) {
	var before, after []ast.Decl

	if len(file.Decls) > 0 {
		hasImport := false
		if genDecl, ok := file.Decls[0].(*ast.GenDecl); ok {
			hasImport = genDecl.Tok == token.IMPORT
		}

		if hasImport {
			before, after = []ast.Decl{file.Decls[0]}, file.Decls[1:]
		} else {
			after = file.Decls
		}
	}

	file.Decls = append(before,
		&ast.GenDecl{
			Tok: token.VAR,
			Specs: []ast.Spec{
				&ast.ValueSpec{
					Names: []*ast.Ident{ast.NewIdent(name)},
					Type:  ast.NewIdent("int"),
					Values: []ast.Expr{
						&ast.BasicLit{
							Kind:  token.INT,
							Value: fmt.Sprintf("%d", value),
						},
					},
				},
			},
		},
	)
	file.Decls = append(file.Decls, after...)
}

func insertHello(file *ast.File) {
	ast.Inspect(file, func(node ast.Node) bool {
		if ifStmt, ok := node.(*ast.IfStmt); ok {
			ifStmt.Body.List = append(
				[]ast.Stmt{
					&ast.ExprStmt{
						X: &ast.CallExpr{
							Fun: &ast.SelectorExpr{
								X:   ast.NewIdent("fmt"),
								Sel: ast.NewIdent("Printf"),
							},
							Args: []ast.Expr{
								&ast.BasicLit{
									Kind:  token.STRING,
									Value: "\"hello\"",
								},
							},
						},
					},
				},
				ifStmt.Body.List...,
			)
		}
		return true
	})
}

func main() {
	if len(os.Args) != 2 {
		return
	}

	fset := token.NewFileSet()
	if file, err := parser.ParseFile(fset, os.Args[1], nil, parser.ParseComments); err == nil {

		ast.Inspect(file, func(n ast.Node) bool {
			functions, ok := n.(*ast.FuncDecl)
			if ok {
				nameoffunc := functions.Name.Name
				body := functions.Body
				for i := 0; i < len(body.List); i++ {
					hzwhatido := body.List[i].(*ast.ExprStmt).X.(*ast.CallExpr)
					dkwhatido := hzwhatido.Fun.(*ast.SelectorExpr).Sel.Name
					if dkwhatido == "Printf" {
						str1 := fset.Position(hzwhatido.Pos()).Line
						str2 := strings.Split(hzwhatido.Args[0].(*ast.BasicLit).Value, "\"")
						str3 := "\"" + strconv.Itoa(str1) + "(" + nameoffunc + "):" + strings.Join(str2, " ") + "\""
						hzwhatido.Args[0].(*ast.BasicLit).Value = str3
					}
				}
			}
			return true
		})
		if format.Node(os.Stdout, fset, file) != nil {
			fmt.Printf("Formatter error: %v\n", err)
		}
	} else {
		fmt.Printf("Errors in %s\n", os.Args[1])
	}
}
