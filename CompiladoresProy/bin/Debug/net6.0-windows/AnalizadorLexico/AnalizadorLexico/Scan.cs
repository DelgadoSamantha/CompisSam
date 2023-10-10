using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static AnalizadorLexico.Globals.Global;

namespace AnalizadorLexico
{
    class Scan
    {
        public class Scaan
        {
            public static int BUFLEN = 256;

            public static char[] lineBuf = new char[BUFLEN];
            public static int bufsize = 0;
            public static string ruta = Directory.GetCurrentDirectory()+"\\archToken.txt";
            public static string rutaErr = Directory.GetCurrentDirectory()+"\\archError.txt";
            public static int MAXTOKENLEN = 40;
            public static List<char> tokenString = new List<char>();
            public static string line;
            public static char[]? linea;
            public static StreamReader? sr;
            public static string reader;
            public static string? t;
            public static char c;
            public static int save = Globals.TRUE;
            public static Globals.Global.TokenType currentToken = Globals.Global.TokenType.ENDFILE;
            //public static int except = Globals.FALSE;

            public static void Main(string[] args)
            {
                if (File.Exists(ruta))
                {
                    File.Delete(ruta);
                }
                if (File.Exists(rutaErr))
                {
                    File.Delete(rutaErr);
                }

                //Console.WriteLine(args[0]);
                if (args.Length >= 1)
                {
                    reader = args[0];
                    sr = new StreamReader(reader);
                    //getNextChar();
                    //getToken();
                    while (getToken() != Globals.Global.TokenType.ENDFILE)
                    {

                    }
                    //getNextChar();
                    sr.Close();
                }
            }

            


            public enum StateType
            {
                INICIO, //estado inicial
                //EPOSIBLECOMM estado de posible comentario
                ECOMENTARIO,//estado de comentario
                ECOMENMULTIPLE, //estado de comentario multiple
                ECOMENSIMPLE, //estado de comentario simple
                EPOSIBLECOMMULTIPLE, //estado de posible comentario multiple
                EENTEROS, //estado de enteros
                EPOSIBLENUMREAL, //estado de posible numero real
                EENTEROREAL, //estado de entero real
                EIDENTIFICADOR, //estado de identificador
                EASIGNACION, //estado de asignacion
                ESIGNOMAS, //estado de signo mas
                EINCREMENTABLE, //estado incrementable
                ESIGNOMENOS, //estado de signo menos
                EDECREMENTABLE, //estado decrementable
                ESIGNOMAYOREQ, //estado de signo mayor que
                EMAYORIGUAL, //estado de mayor igual
                ESIGNOMENOREQ, //estado de signo menor que
                EMENORIGUAL, //estado de menor igual
                EDIFERENTEDE, //estado de diferente de
                HECHO //estado terminal
            }
            public static char getNextChar()
            {
                //Console.WriteLine(ruta);
                //except=Globals.FALSE; 
                //Thread.Sleep(1000);
                try
                {

                    //Continue to read until you reach end of file
                    
                    if (!(Globals.linepos < bufsize))
                    {


                        Globals.lineno++;
                        line = sr.ReadLine();


                        if (line != null)
                        {
                            //if (!string.IsNullOrWhiteSpace(line))
                            //{
                                bufsize = line.Length;
                                bufsize++;
                                line += '\n';
                                Globals.linepos = 0;
                                return line[Globals.linepos++];
                            //}
                            
                        }
                        else
                        {
                            return '\0';
                        }
                    }
                    else
                    {

                        return line[Globals.linepos++];
                    }


                    //close the file
                    //sr.Close();
                    //Console.ReadLine();
                }
                catch (Exception e)
                {
                    //except = Globals.TRUE;
                   
                    Console.WriteLine("Exception: " + e.Message);
                }
                return '\n';// Retorna cuando hay una excepcion 
                
            }

            //public static Globals.Global.TokenType reservedWords[Globals.MAXRESERVED]
            public static Dictionary<string, Globals.Global.TokenType> reservedWords = new Dictionary<string, TokenType>()
            {
                {"if",Globals.Global.TokenType.IF},
                {"then",Globals.Global.TokenType.THEN},
                {"else",Globals.Global.TokenType.ELSE},
                {"end",Globals.Global.TokenType.END},
                {"repeat",Globals.Global.TokenType.REPEAT},
                {"until",Globals.Global.TokenType.UNTIL},
                {"main",Globals.Global.TokenType.MAIN},
                {"do",Globals.Global.TokenType.DO},
                {"while",Globals.Global.TokenType.WHILE},
                {"cin",Globals.Global.TokenType.CIN},
                {"cout",Globals.Global.TokenType.COUT},
                {"boolean",Globals.Global.TokenType.BOOLEAN},
                {"int",Globals.Global.TokenType.INT},
                {"real",Globals.Global.TokenType.REAL}
            };



            public static Globals.Global.TokenType reservedLookup(string s)
            {
               
                foreach (KeyValuePair<string, Globals.Global.TokenType> rw in reservedWords)
                {
                       
                    if (String.Equals(s, rw.Key))
                    {
                        return rw.Value;
                    }
                }
                
                return Globals.Global.TokenType.ID;
            }


            public static Globals.Global.TokenType getToken()
            {

                //int tokenStringIndex = 0;
                
                
                //char[] c= new char[1000]; // array de caracteres de longitud 1000
                StateType state = StateType.INICIO;

                while (state != StateType.HECHO)
                {


                    if (save == Globals.TRUE)
                    {
                        c = getNextChar();
                        //Console.WriteLine("c-> "+ c);
                    }

                    switch (state)
                    {
                        case StateType.INICIO:
                            save = Globals.TRUE;

                            while ((c == ' ') || (c == '\t') || (c == '\n') /*|| except==Globals.TRUE*/)
                            {
                                c=getNextChar();
                            }

                            //tokenString.Add(c);
                            

                            if (Char.IsDigit(c))
                            {
                                state = StateType.EENTEROS;
                                tokenString.Add(c);
                            }
                            else if (Char.IsLetter(c) || c == '_')
                            {
                                state = StateType.EIDENTIFICADOR;
                                tokenString.Add(c);
                            }
                            else if (c == ':')
                            {
                                state = StateType.EASIGNACION;
                                tokenString.Add(c);
                            }
                            else if (c == '+')
                            {
                                state = StateType.ESIGNOMAS;
                                tokenString.Add(c);
                            }
                            else if (c == '-')
                            {
                                state = StateType.ESIGNOMENOS;
                                tokenString.Add(c);
                            }
                            else if (c == '>')
                            {
                                state = StateType.ESIGNOMAYOREQ;
                                tokenString.Add(c);
                            }
                            else if (c == '<')
                            {
                                state = StateType.ESIGNOMENOREQ;
                                tokenString.Add(c);
                            }
                            else if (c == '/')
                            {
                                state = StateType.ECOMENTARIO; //posible comentario
                                tokenString.Add(c);
                            }
                            else if (c == '=')
                            {
                                currentToken = Globals.Global.TokenType.IGUALDAD;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (c == '*')
                            {
                                currentToken = Globals.Global.TokenType.MULTI;
                                state = StateType.HECHO;
                                tokenString.Add(c); 
                            }
                            else if (c == '(')
                            {
                                currentToken = Globals.Global.TokenType.PARENIZQ;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (c == ')')
                            {
                                currentToken = Globals.Global.TokenType.PARENDERE;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (c == '{')
                            {
                                currentToken = Globals.Global.TokenType.LLAVEIZQ;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (c == '}')
                            {
                                currentToken = Globals.Global.TokenType.LLAVEDER;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (c == ',')
                            {
                                currentToken = Globals.Global.TokenType.COMA;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (c == ';')
                            {
                                currentToken = Globals.Global.TokenType.PUNTOCOMA;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (c == '%')
                            {
                                currentToken = Globals.Global.TokenType.RES;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if(c == '\0')
                            {
                                currentToken = Globals.Global.TokenType.ENDFILE;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else if (Char.IsNumber(c) || c=='_' || Char.IsLetter(c))
                            {
                                state = StateType.EIDENTIFICADOR;
                                tokenString.Add(c);
                            }
                            else
                            {
                                currentToken= Globals.Global.TokenType.ERROR;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            break;

                        case StateType.EENTEROS:
                            if (c == '.')
                            {
                                state = StateType.EPOSIBLENUMREAL;
                                tokenString.Add(c);
                                save = Globals.TRUE;
                            }
                            else if (Char.IsDigit(c))
                            {
                                //Entra cuando es digito
                                tokenString.Add(c);
                            }
                            else
                            {
                                
                                //state = StateType.EENTEROS;
                                if (c != '\t')
                                {
                                    currentToken = Globals.Global.TokenType.ENTERO;
                                    state = StateType.HECHO;
                                    //save = Globals.FALSE;
                                    

                                }
                                save = Globals.FALSE;
                                //tokenString.Add(c); 
                            }
                            break;

                        case StateType.EPOSIBLENUMREAL:
                            if (Char.IsDigit(c))
                            {
                                state = StateType.EENTEROREAL;
                                //concatenar c
                                tokenString.Add(c);
                            }
                            else
                            {
                                state = StateType.HECHO;
                                currentToken = Globals.Global.TokenType.ERROR;
                                save = Globals.FALSE;
                            }
                            break;

                        case StateType.EENTEROREAL:
                            if (Char.IsDigit(c))
                            {
                                //state = StateType.EENTEROREAL;
                                //concatenar c
                                tokenString.Add(c);
                            }
                            else
                            {
                                save = Globals.FALSE;
                                currentToken = Globals.Global.TokenType.NREAL;
                                state = StateType.HECHO;
                            }
                            break;

                        case StateType.EIDENTIFICADOR:
                            //Console.WriteLine("test->"+Char.IsLetter(c)+"   c-> "+c);
                            if ((Char.IsLetter(c) || c == '_' || Char.IsDigit(c))/* && (c!='\n' || c!=' ')*/)
                            {
                                //state = StateType.EIDENTIFICADOR;
                                //concatenar c
                                tokenString.Add(c);
                                //save= Globals.TRUE;
                            }//else if (except==Globals.TRUE)
                            //{
                            //    save=Globals.TRUE;
                            //    except = Globals.FALSE;
                            //}
                            else
                            {
                                
                                //currentToken = reservedLookup(tokenString);
                                save = Globals.FALSE;
                                t = string.Join("", tokenString);
                                
                                currentToken = reservedLookup(t);
                                state = StateType.HECHO;
                            }
                            break;

                        case StateType.EASIGNACION:
                            if (c == '=')
                            { 
                                //concatenar c
                                currentToken = Globals.Global.TokenType.ASIGNACION;
                                state = StateType.HECHO;
                                tokenString.Add(c);
                            }
                            else
                            {
                                currentToken = Globals.Global.TokenType.ERROR;
                                state = StateType.HECHO;
                                save = Globals.FALSE;
                            }
                            break;

                        case StateType.ESIGNOMAS:
                            if (c == '+')
                            {
                                currentToken = Globals.Global.TokenType.PLUSPLUS;
                                state = StateType.HECHO;
                                //concatenar c
                                tokenString.Add(c);
                            }
                            else
                            {
                                currentToken = Globals.Global.TokenType.SUMA;
                                state = StateType.HECHO;
                                save = Globals.FALSE;
                            }
                            break;

                        case StateType.ESIGNOMENOS:
                            if (c == '-')
                            {
                                currentToken = Globals.Global.TokenType.MENOSMENOS;
                                state = StateType.HECHO;
                                //concatenar c
                                tokenString.Add(c);
                                
                            }
                            else
                            {
                                currentToken = Globals.Global.TokenType.RESTA;
                                state = StateType.HECHO;
                                save = Globals.FALSE;
                            }
                            break;

                        case StateType.ESIGNOMAYOREQ:
                            if (c == '=')
                            {
                                //concatenar c
                                //tokenString.Add(c);
                                currentToken = Globals.Global.TokenType.MAYOREQ;
                                state = StateType.HECHO;
                            }
                            else
                            {
                                save = Globals.FALSE;
                                currentToken = Globals.Global.TokenType.MAYOR;
                                state = StateType.HECHO;
                            }
                            break;

                        case StateType.ESIGNOMENOREQ:
                            if (c == '=')
                            {
                                
                                //concatenar c
                                //tokenString.Add(c);
                                currentToken = Globals.Global.TokenType.MENOREQ;
                                state = StateType.HECHO;
                            }
                            else if (c == '>')
                            {
                                
                                //concatenar c
                                //tokenString.Add(c);
                                currentToken = Globals.Global.TokenType.DIFERENTEDE;
                                state = StateType.HECHO;
                            }
                            else
                            {
                                currentToken = Globals.Global.TokenType.MENOR;
                                state = StateType.HECHO;
                                save = Globals.FALSE;
                            }
                            break;

                        case StateType.ECOMENTARIO:
                            if (c == '/')
                            {
                                tokenString.Clear();
                                c = getNextChar();
                                while (c != '\n')
                                {
                                    c = getNextChar();
                                }
                                state = StateType.INICIO;
                                save = Globals.TRUE;
                            }
                            else if (c == '*')
                            {
                                tokenString.Clear();
                                state = StateType.ECOMENMULTIPLE;
                                save = Globals.TRUE;

                            }
                            else
                            {
                                state = StateType.HECHO;
                                currentToken = Globals.Global.TokenType.DIV;
                                save = Globals.FALSE;
                            }
                            break;

                        case StateType.ECOMENMULTIPLE:
                            if (c == '/')
                            {
                                state = StateType.INICIO;
                            }
                            else if (c == '*')
                            {
                                //continue;
                            }
                            else if (c == '\0')
                            {
                                currentToken = Globals.Global.TokenType.ERROR;
                                state = StateType.HECHO;
                            }
                            else
                            {
                                state = StateType.EPOSIBLECOMMULTIPLE;
                            }
                            break;

                        case StateType.EPOSIBLECOMMULTIPLE:
                            if (c == '*')
                            {
                                state = StateType.ECOMENMULTIPLE;
                            }
                            else if (c == '\0')
                            {
                                state = StateType.HECHO;
                                currentToken = Globals.Global.TokenType.ERROR;
                            }
                            else
                            {
                                //continue;
                            }
                            break;

                        default:
                            currentToken = Globals.Global.TokenType.ERROR;
                            state = StateType.HECHO;
                            break;


                    }

                }

                string rutaes = Directory.GetCurrentDirectory();
                string token = string.Join("", tokenString);
                Console.WriteLine(currentToken+" "+token);

                //Util.printToken(currentToken, token, "C:\\Users\\itzia\\source\\repos\\AnalizadorLexico\\AnalizadorLexico\\bin\\Debug\\net6.0\\archToken.txt", "C:\\Users\\itzia\\source\\repos\\AnalizadorLexico\\AnalizadorLexico\\bin\\Debug\\net6.0\\archError.txt");
               
                Util.printToken(currentToken, token,rutaes+"\\archToken.txt",rutaes+"\\archError.txt");

                tokenString.Clear();

                return currentToken;

                
            }


        }

    }
}
