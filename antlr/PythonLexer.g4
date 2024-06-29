lexer grammar PythonLexer;
 
// 关键字
AND : 'and';
AS : 'as';
ASSERT : 'assert';
BREAK : 'break';
CLASS : 'class';
CONTINUE : 'continue';
DEF : 'def';
DEL : 'del';
ELIF : 'elif';
ELSE : 'else';
EXCEPT : 'except';
FALSE : 'False';
FINALLY : 'finally';
FOR : 'for';
FROM : 'from';
GLOBAL : 'global';
IF : 'if';
IMPORT : 'import';
IN : 'in';
IS : 'is';
LAMBDA : 'lambda';
NONLOCAL : 'nonlocal';
NOT : 'not';
NULL : 'None';
OR : 'or';
PASS : 'pass';
RAISE : 'raise';
RETURN : 'return';
TRUE : 'True';
TRY : 'try';
WHILE : 'while';
WITH : 'with';
YIELD : 'yield';
 
// 标点符号
LPAREN : '(' ;
RPAREN : ')' ;
LSQUARE : '[' ;
RSQUARE : ']' ;
COLON : ':' ;   // :冒号
COMMA : ',' ;   // ,逗号
DOT : '.' ;     // .点号
PLUS : '+' ;    // +加号
MINUS : '-' ;   // -减号
STAR : '*' ;    // *星号
SLASH : '/' ;   // /除号
PERCENT : '%' ; // %百分号
EQ : '==' ;     // ==等于号
NEQ : '!=' ;    // !=不等于号
LT : '<' ;      // <小于号
GT : '>' ;      // >大于号
LE : '<=' ;     // <=小于等于号
GE : '>=' ;     // >=大于等于号
PIPE : '|' ;    // |管道符号
CARET : '^' ;   // ^尖号
AMPERSAND : '&' ; // &与号
TILDE : '~' ;   // ~波浪线
AT : '@' ;      // @@符号
DOUBLE_STAR : '**' ; // **双星号
 
// 数值、变量名、函数名等
ID : [a-zA-Z][a-zA-Z0-9]* ;
NUMBER : [0-9]+(.[0-9]+)? ;
STRING : '"' (ESCAPED_CHARACTER | ~[\\"])*? '"' ;
COMMENT : '#' ~[\r\n]* ;
WS : [\t