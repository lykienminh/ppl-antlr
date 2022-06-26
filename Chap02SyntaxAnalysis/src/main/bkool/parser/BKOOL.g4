grammar BKOOL;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STRING:       
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    else:
        return result;
}

options{
	language=Python3;
}

/* 
 * =========================================================================================
 * Author: github@lykienminh
 * Chap 02: Syntax Analysis
 * Date: 20220615
 * =========================================================================================
 */

// Question 4 BKOOL
// =========================================================================================
program: decls;

decls: decl decls | decl;
decl: vardecl | funcdecl;

vardecl: typ idlist SEMI;
idlist: ID COMMA idlist | ID;
typ: 'int' | 'float';

funcdecl: typ ID LB (params | ) RB body;
params: params SEMI param | param;
param: typ idlist;
body: LP bodyList RP;
bodyList: (vardecl | stmt) bodyList | ;

//stmt
stmt: assignStmt | callStmt | returnStmt;
// stmts: stmt stmts | stmt;
assignStmt: ID EQUAL exprlist SEMI;
exprlist: expr COMMA exprlist | expr;
callStmt: ID LB (exprlist | ) RB SEMI;
returnStmt: RETURN expr SEMI;
expr: 'expr';

RETURN: 'return';
EQUAL: '=';
LP: '{';
RP: '}';
ID: [a-zA-Z]+;
COMMA: ',';
SEMI: ';';
LB: '(';
RB: ')';
WS: [ \t\r\n] -> skip;
ERROR_CHAR: . {raise ErrorToken(self.text)};
// =========================================================================================

// Question 3 BKOOL
// =========================================================================================
// program: decls;

// decls: decl decls | decl;
// decl: vardecl | funcdecl;

// vardecl: typ idlist SEMI;
// idlist: ID COMMA idlist | ID;
// typ: 'int' | 'float';

// funcdecl: typ ID LB (params | ) RB body;
// params: params SEMI param | param;
// param: typ idlist;
// body: LP bodyList RP;
// bodyList: (vardecl | stmt) bodyList | ;

// //stmt
// stmt: assignStmt | callStmt | returnStmt;
// // stmts: stmt stmts | stmt;
// assignStmt: ID EQUAL exprlist SEMI;
// exprlist: expr COMMA exprlist | expr;
// callStmt: ID LB (exprlist | ) RB SEMI;
// returnStmt: RETURN expr SEMI;
// expr: 'expr';

// RETURN: 'return';
// EQUAL: '=';
// LP: '{';
// RP: '}';
// ID: [a-zA-Z]+;
// COMMA: ',';
// SEMI: ';';
// LB: '(';
// RB: ')';
// WS: [ \t\r\n] -> skip;
// ERROR_CHAR: . {raise ErrorToken(self.text)};
// =========================================================================================

// Question 1 BKOOL
// =========================================================================================
// program: decls;
// decls: decl decls | decl;
// decl: vardecl | funcdecl;
// vardecl: 'vardecl';
// funcdecl: 'funcdecl';
// WS: [ \t\r\n] -> skip;
// ERROR_CHAR: . {raise ErrorToken(self.text)};
// =========================================================================================

// Question 2 BKOOL
// =========================================================================================
// program: decls;

// decls: decl decls | decl;
// decl: vardecl | funcdecl;

// vardecl: typ idlist SEMI;
// idlist: ID COMMA idlist | ID;

// funcdecl: typ ID LB (params | ) RB body;
// params: params SEMI param | param;
// param: typ idlist;

// typ: 'int' | 'float';
// body: 'body';

// ID: [a-zA-Z]+;
// COMMA: ',';
// SEMI: ';';
// LB: '(';
// RB: ')';
// WS: [ \t\r\n] -> skip;
// ERROR_CHAR: . {raise ErrorToken(self.text)};
// =========================================================================================


/* 
 * =========================================================================================
 * Do not modify this part
 * =========================================================================================
 */

UNCLOSE_STRING: .;
ILLEGAL_ESCAPE: .;
UNTERMINATED_COMMENT: .;
