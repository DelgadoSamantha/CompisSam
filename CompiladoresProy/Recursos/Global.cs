using System;
using System.Collections.Generic;
using System.ComponentModel.Design.Serialization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CompiladoresProy.Recursos
{
    public static class Global
    {
        public static readonly Dictionary<int, string> tk = new Dictionary<int, string>()
        {
            {19,"+"},
            {20,"-"},
            {21,"*"},
            {22,"/"},
            {23,"%"},
            {24,"<"},
            {25,"<="},
            {26,">"},
            {27,">="},
            {28,"="},
            {29,"<>"},
            {30,":="},
            {31,"("},
            {32,")"},
            {33,"}"},
            {34,"{"},
            {35,"++"},
            {36,"--"},
            {37,","},
            {38,";"},
            {16,"id"},
            {15,"real"},
            {14,"integer"}
        };
    }
}
