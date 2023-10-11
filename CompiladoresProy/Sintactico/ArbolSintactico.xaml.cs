using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Forms;
using Newtonsoft.Json;
using CompiladoresProy.Recursos;

namespace CompiladoresProy.Sintactico
{
    /// <summary>
    /// Lógica de interacción para ArbolSintactico.xaml
    /// </summary>


    enum NodoKind { 
    STKD=1, 
    EXPD=2
    }
    enum SentenciaKind {
    IFKD = 1,
    WHILEKD=2,
    DOKD=3,
    UNTILKD=4,
    CINKD=5,
    COUTKD=6,
    ASIGKD=7,
    MAINKD=10,
    DECKD=11,
    TYPEDEFIKD=12,
    ELSEKD=14
    }
    enum ExpresionKind {
    OPERKD = 1,
    CONSTKD=2,
    CONSTFKD=3,
    IDKD=4
    }
    enum DeclaracionKind {
    INTKD = 1,
    REALKD = 2,
    BOOLEANKD=3,
    VOIDKD=4
    }

    public class NodoArbol
    {
        public string valor = "";
        public int nodoKind;
        public int kind;
        public int type;
        public NodoArbol ?firstChild;
        public NodoArbol ?secondChild;
        public NodoArbol ?thirdChild;
        public NodoArbol ?sibling;
    }
    public partial class ArbolSintactico : Page
    {
        public ArbolSintactico()
        {
            InitializeComponent();
            string archJson = File.ReadAllText("arbolSin.json");
            JToken raizNodo = JToken.Parse(archJson);
            NodoArbol raiz = JsonConvert.DeserializeObject<NodoArbol>(archJson) ?? new NodoArbol();
            TreeViewItem raizIt = ConstruccionArbol(raiz);
            arbolSin.Items.Add(raizIt);

            foreach(object it in arbolSin.Items)
            {
                if(it is TreeViewItem treeViewItem)
                {
                    ExpandirArbol(treeViewItem);
                }
            }
        }
        private void ExpandirArbol(TreeViewItem item)
        {
            item.IsExpanded = true;
            foreach (object childItem in item.Items)
            {
                if (childItem is TreeViewItem childTreeViewItem)
                {
                    ExpandirArbol(childTreeViewItem);
                }
            }
        }
        private TreeViewItem ConstruccionArbol(NodoArbol nodo)
        {
            TreeViewItem it = new TreeViewItem();
            string val = "";

            if(nodo != null)
            {
                switch (nodo.nodoKind)
                {
                    case (int)NodoKind.STKD:
                        switch (nodo.kind)
                        {
                            case (int)SentenciaKind.IFKD:
                                val = "IF";
                                break;
                            case (int)SentenciaKind.WHILEKD:
                                val = "WHILE";
                                break;
                            case (int)SentenciaKind.DOKD:
                                val = "DO";
                                break;
                            case (int)SentenciaKind.UNTILKD:
                                val = "UNTIL";
                                break;
                            case (int)SentenciaKind.CINKD:
                                val=$"READ:{nodo.valor}";
                                break;
                            case (int)SentenciaKind.COUTKD:
                                val = $"WRITE{nodo.valor}";
                                break;
                            case (int)SentenciaKind.ASIGKD:
                                val = "ASSIGN TO: " + nodo.valor;
                                break;
                            case (int)SentenciaKind.MAINKD:
                                val = "MAIN";
                                break;
                            case (int)SentenciaKind.DECKD:
                                val = "DEC";
                                break;
                            case (int)SentenciaKind.TYPEDEFIKD:
                                val = "TYPE";
                                break;
                            case (int)SentenciaKind.ELSEKD:
                                val = "ELSE";
                                break;
                            default:
                                val = "Unknow SentenciaKind node";
                                break;
                        }
                        break;
                    case (int)NodoKind.EXPD:
                        switch (nodo.kind)
                        {
                            case (int)ExpresionKind.OPERKD:
                                val = Global.tk[int.Parse(nodo.valor)];
                                break;
                            case (int)ExpresionKind.CONSTKD:
                                val=nodo.valor; break;
                            case (int)ExpresionKind.IDKD:
                                val=nodo.valor;
                                break;

                        }
                        break;
                    default:
                        val = "Unknow node kind";
                        break;
                }

                it.Header = val;
                List<NodoArbol>children= new List<NodoArbol>();
                if(nodo.firstChild!=null) children.Add(nodo.firstChild);
                if(nodo.secondChild!=null) children.Add(nodo.secondChild);
                if(nodo.thirdChild!=null) children.Add(nodo.thirdChild);

                foreach (NodoArbol childNodo in children)
                {
                    TreeViewItem childItem = ConstruccionArbol(childNodo);
                    it.Items.Add(childItem);

                    NodoArbol sibling = childNodo.sibling;
                    while(sibling!=null)
                    {
                        TreeViewItem sb = ConstruccionArbol(sibling);
                        it.Items.Add(sb);
                        sibling=sibling.sibling;
                    }
                }
            }
           

            return it;
        }

        
    }
}
