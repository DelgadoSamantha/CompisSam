using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AnalizadorLexico
{
    class Globals
    {
        public static int MAXRESERVED = 8;
        public static int FALSE = 0;
        public static int TRUE = 1;
        public static int linepos = 0;
        public static int lineno=0;
        public static int EchoSource;

        public static class Global
        {


            public enum TokenType
            {
                //book-keeping tokens
                ENDFILE,
                ERROR,
                //reserved words 
                IF,
                THEN,
                ELSE,
                END,
                REPEAT,
                UNTIL,
                MAIN,
                DO,
                WHILE,
                CIN,
                COUT,
                BOOLEAN,
                INT,
                REAL,
                //multicharacter tokens 
                ID,
                NREAL,
                ENTERO,

                //special symbols
                SUMA,
                RESTA,
                MULTI,
                DIV,
                RES, //%
                MENOR, //<
                MENOREQ, //<=
                MAYOR, //>
                MAYOREQ, //>=
                IGUALDAD, //==
                DIFERENTEDE, //!=
                ASIGNACION, //:=
                PARENIZQ, //(
                PARENDERE, //)
                LLAVEDER, //}
                LLAVEIZQ, //{
                PLUSPLUS, //++
                MENOSMENOS, //--
                COMA,
                PUNTOCOMA,
                COMMENT,
                MULTICOMMENT

            }


            public enum TokenTypeSin
            {
                ENDFILE=1
                ERROR=2

                IF=3
                THEN=4
                ELSE=5
                END=6
                REPEAT=7
                UNTIL=8
                MAIN=9
                DO=10
                WHILE=11
                CIN=12
                COUT=13
                BOOLEAN=14
                INT=15
                REAL=16
    
                ID=17
                NREAL=18
                ENTERO=19
    
                SUMA=20
                RESTA=21
                MULTI=22
                DIV=23
                RES=24
                MENOR=25
                MENOREQ=26
                MAYOR=27
                MAYOREQ=27
                IGUALDAD=28
                DIFERENTEDE=29
                ASIGNACION=30
                PARENIZQ=31
                PARENDERE=32
                LLAVEIZQ=33
                LLAVEDER=34
                PLUSPLUS=35
                MENOSMENOS=36
                COMA=37
                PUNTOCOMA=38
                COMMENT=39
                MULTICOMMENT=40

            }
    }

        //public const int MAXRESERVED = 8;


    }
}
