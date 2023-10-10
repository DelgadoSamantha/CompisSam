using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AnalizadorLexico
{
    class Util
    {
        private const string V = "Palabra Reservada: ";
        
        public static void printToken(Globals.Global.TokenType token, string tokenString, string fileName, string fileNameError)
        {
            StreamWriter writer = new StreamWriter(fileName, true);
            StreamWriter writerEr = new StreamWriter(fileNameError, true);

            //MessageBox.Show(""+Globals.Global.MAXRESERVED);
            switch (token)
            {
                case Globals.Global.TokenType.IF:

                case Globals.Global.TokenType.THEN:

                case Globals.Global.TokenType.ELSE:

                case Globals.Global.TokenType.END:

                case Globals.Global.TokenType.REPEAT:

                case Globals.Global.TokenType.UNTIL:

                case Globals.Global.TokenType.MAIN:

                case Globals.Global.TokenType.DO:

                case Globals.Global.TokenType.WHILE:

                case Globals.Global.TokenType.CIN:

                case Globals.Global.TokenType.COUT:

                case Globals.Global.TokenType.BOOLEAN:

                case Globals.Global.TokenType.REAL:

                case Globals.Global.TokenType.INT:

                    //imprimir a pantalla la palabra reservada
                    //File.WriteAllText(openSalida.FileName, "Palabra Reservada: "+tokenString);
                    writer.WriteLine("PALABRARESERVADA\t" + tokenString +"\t"+Globals.lineno+"\t" +Globals.linepos);
                    break;

                case Globals.Global.TokenType.SUMA:
                    writer.WriteLine("SUMA\t+\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.RESTA:
                    writer.WriteLine("RESTA\t-\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.MULTI:
                    writer.WriteLine("MULTI\t*\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.DIV:
                    writer.WriteLine("DIV\t/\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.RES:
                    writer.WriteLine("RES\t%\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.MENOR:
                    writer.WriteLine("MENOR\t<\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.MENOREQ:
                    writer.WriteLine("MENOREQ\t<=\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.MAYOR:
                    writer.WriteLine("MAYOR\t>\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.MAYOREQ:
                    writer.WriteLine("MAYOREQ\t>=\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.IGUALDAD:
                    writer.WriteLine("IGUALDAD\t=\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.DIFERENTEDE:
                    writer.WriteLine("DIFERENTEDE\t<>\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.ASIGNACION:
                    writer.WriteLine("ASIGNACION\t:=\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.PARENIZQ:
                    writer.WriteLine("PARENIZQ\t(\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.PARENDERE:
                    writer.WriteLine("PARENDERE\t)\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.LLAVEIZQ:
                    writer.WriteLine("LLAVEIZQ\t{\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.LLAVEDER:
                    writer.WriteLine("LLAVEDER\t}\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.COMMENT:
                    writer.WriteLine("COMMENT\t//\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.MULTICOMMENT:
                    writer.WriteLine("MULTICOMMENT\t/**/\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.PLUSPLUS:
                    writer.WriteLine("PLUSPLUS\t++\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.MENOSMENOS:
                    writer.WriteLine("MENOSMENOS\t--\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.COMA:
                    writer.WriteLine("COMA\t,\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.PUNTOCOMA:
                    writer.WriteLine("PUNTOCOMA\t;\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;

                case Globals.Global.TokenType.ID:
                    writer.WriteLine("ID\t"+ tokenString + "\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;

                case Globals.Global.TokenType.NREAL:
                    writer.WriteLine("NREAL\t"+ tokenString + "\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;

                case Globals.Global.TokenType.ENTERO:
                    writer.WriteLine("ENTERO\t" + tokenString + "\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;

                case Globals.Global.TokenType.ERROR:
                    writerEr.WriteLine(tokenString + "\t" + Globals.lineno + "\t" + Globals.linepos);
                    break;
                case Globals.Global.TokenType.ENDFILE:
                    writer.WriteLine("ENDFILE\t" + token+"\t"+ Globals.lineno + "\t" + Globals.linepos);
                    break;
                default:
                    writer.WriteLine("Unknown token: " + tokenString);
                    break;

            }
            writer.Close();
            writerEr.Close();
        }
    }
}
