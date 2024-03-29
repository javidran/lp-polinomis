grammar Polygon;

root : (assig | printsmth | area | perimeter | vertices | centroid | inside | equal | draw | color)* EOF;

string: QUOTE STRING QUOTE;

point: NUM NUM;

polygon : LPARENTHESIS polygon RPARENTHESIS     #priority
    | LBRACKET point* RBRACKET                  #newpolygon
    | polygon INTERSECT polygon                 #intersection
    | polygon UNION polygon                     #convexunion
    | RANDOM NUM                                #random
    | BOUNDING polygon                          #bounding
    | ID                                        #polygonid
    ;

assig: ID ASSIG polygon;

printsmth : PRINT polygon
    | PRINT string
    ;

area: AREA polygon;

perimeter: PERIMETER polygon;

vertices: VERTICES polygon;

centroid: CENTROID polygon;

inside: INSIDE LBRACKET point RBRACKET COMMA polygon        #insidepoint
    | INSIDE polygon COMMA polygon                          #insidepolygon
    ;

equal: EQUAL polygon COMMA polygon;

draw: DRAW string (COMMA polygon)+;

colornum: NUM NUM NUM;

color: COLOR polygon COMMA LCLAUDATOR colornum RCLAUDATOR;

NUM : ('-')? NATNUM ('.' NATNUM)? ;
NATNUM : [0-9]+ ;

LPARENTHESIS : '(';
RPARENTHESIS : ')';
LBRACKET : '[' ;
RBRACKET : ']' ;
LCLAUDATOR : '{';
RCLAUDATOR : '}';

ASSIG : ':=';
INTERSECT : '*';
UNION : '+';
BOUNDING : '#';
RANDOM: '!';
COMMA: ',';
QUOTE: '"';

PRINT: 'print';
AREA: 'area';
PERIMETER: 'perimeter';
VERTICES: 'vertices';
CENTROID: 'centroid';
COLOR: 'color';
INSIDE: 'inside';
EQUAL: 'equal';
DRAW: 'draw';

ID : [a-zA-Z] [a-zA-Z0-9_]* ; // Un ID es utilizado para definir variables. Solo acepta letras, números y barras bajas.
STRING : [0-9A-Za-z._\-]+ ; // Un String es utilizado para definir el nombre del archivo. A diferencia del ID, puede aceptar guiones y puntos.

COMMENT : '//' ~[\r\n]* -> skip ; // Ignora el contenido de la linea a partir de doble barra.
WS : [ \r\n\t]+ -> skip ; // Ignora espacios, tabuladores y nuevas lineas.