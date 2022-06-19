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

// program  : VAR COLON ID SEMI EOF ;

// ID: [a-z]+ ;

// SEMI: ';' ;

// COLON: ':' ;

// VAR: 'Var' ;

program: EOF ;

// Question 1
ID: [a-z][a-z0-9]* ;

// Question 2
// fragment INT_PART: [0-9]+;
// fragment FRAC_PART: '.'INT_PART;
// fragment EXP_PART: 'e''-'?INT_PART;
// FLOAT: INT_PART (FRAC_PART EXP_PART? | EXP_PART);

// Question 3
// fragment SINGLE_QUOTE: '\'';
// STRING: SINGLE_QUOTE (~['] | SINGLE_QUOTE SINGLE_QUOTE)* SINGLE_QUOTE;

// Question 4
// fragment STR_PART: [1-9][0-9]?[0-9]? | '0';
// IPV4: STR_PART '.' STR_PART '.' STR_PART '.' STR_PART;

// Question 5
// fragment DIGITS
//     : [0-9]
//     ;
// fragment UNDER_SCORE
//     : '_'
//     ;
// PHP_INT
//     : ([1-9] (DIGITS | UNDER_SCORE DIGITS)* | '0')
//     {self.text = self.text.replace("_","")}
//     ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

ERROR_CHAR: .;
UNCLOSE_STRING: .;
ILLEGAL_ESCAPE: .;
UNTERMINATED_COMMENT: .;
