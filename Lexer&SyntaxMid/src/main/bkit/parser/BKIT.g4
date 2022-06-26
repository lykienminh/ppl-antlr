grammar BKIT;

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

// program : ;

// Question 4
program: VARNAME EQ expression ';';

expression: exp1 DQUES exp1 | exp1;
exp1: exp2 ADD exp1
    | exp2 SUB exp1
    | exp2;
exp2: exp2 MUL exp3 
    | exp2 DIV exp3
    | exp2 MOD exp3
    | exp3;
exp3: exp3 DOT exp4 | exp4;
exp4: exp5 DSTAR exp4 | exp5;
exp5: '(' expression ')' | operand;
operand: array | PAIRNAME | VARNAME | INTLIT | FLOATLIT | STRINGLIT;

expList: expression COMMA expList | expression;

array: i_arr | a_arr;
i_arr: ARR LB (expList | ) RB;

assPair: PAIRNAME '=>' expression;
aPairList: assPair COMMA aPairList | assPair;
a_arr: ARR LB (aPairList | ) RB;

ARR: 'array';
PAIRNAME: [a-z] [0-9];
VARNAME: [a-z]+;
INTLIT: [1-9][0-9]* | '0';
FLOATLIT: INTLIT '.' [0-9]+;
STRINGLIT: ([A-Z] | [a-z])+;
EQ: '=';
LB: '(';
RB: ')';
COMMA: ',';
// OPERATOR
DSTAR: '**';
DOT: '.';
MUL: '*';
DIV: '/';
MOD: '%';
ADD: '+';
SUB: '-';
DQUES: '??';

// Question 1
// fragment STR_PART: [1-9][0-9]?[0-9]? | '0';
// IPV4: STR_PART '.' STR_PART '.' STR_PART '.' STR_PART;

// Question 2
// fragment REQUIRE_PART: [a-z]+;
// fragment DOT: '.';
// fragment UNDER_SCORE: '_';
// fragment CUSTOM_PART_END: ([a-z0-9] | UNDER_SCORE);
// fragment CUSTOM_PART: ([a-z0-9] | UNDER_SCORE | DOT)* CUSTOM_PART_END;
// BKNETID: REQUIRE_PART '.' REQUIRE_PART CUSTOM_PART;

// Question 3
// fragment EVEN_SUBSET: '0' | '2' | '4' | '6' | '8'
//                     | 'A' | 'C' | 'E'
//                     | 'a' | 'c' | 'e'
//                     ;
// fragment SHEXA_DEC: [0-9];
// fragment SHEXA_HEX: [a-fA-F];  
// SHEXA   : SHEXA_DEC (SHEXA_DEC+ | SHEXA_HEX+)* EVEN_SUBSET
//         ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines


ERROR_CHAR: .;
UNCLOSE_STRING: .;
ILLEGAL_ESCAPE: .;
UNTERMINATED_COMMENT: .;
