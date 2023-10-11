using Microsoft.Win32;
using System;
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
using System.IO;
using System.Xml;
using ICSharpCode.AvalonEdit.Highlighting;
using ICSharpCode.AvalonEdit.Highlighting.Xshd;
using static System.Windows.Forms.LinkLabel;
using System.Diagnostics;
using ICSharpCode.AvalonEdit;
using ICSharpCode.AvalonEdit.Document;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.TextBox;
using System.ComponentModel;

namespace CompiladoresProy
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    /// 

    public class Model : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler? PropertyChanged;
        private int _linea = 1;
        private int _colum = 1;
        public int Linea
        {
            get { return _linea; }
            set
            {
                _linea= value;
                OnPropertyChanged(nameof(Linea));

            }

        }

        public int Colum
        {
            get { return _colum; }
            set
            {
                _colum=value;
                OnPropertyChanged(nameof(Colum));
            }
        }

        //public event PropertyChangedEventHandler PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public partial class MainWindow : Window
    {
        OpenFileDialog openFileDialog, filePath;
        SaveFileDialog saveFileDialog, saveSalida;
        string archAnalizarLex;
        private bool compilado = false;

        //Style avalonstyles;
        public int linea { get; set; }
        public int colum { get; set; }
        private Model values=new Model();
        public MainWindow()
        {
            linea = 0;
            colum = 0;
            DataContext = values;
            this.saveFileDialog = new SaveFileDialog();
            this.openFileDialog = new OpenFileDialog();
            this.filePath = new OpenFileDialog();
            this.saveSalida = new SaveFileDialog();
            InitializeComponent();
            XmlReader reader = XmlReader.Create("../../../Controlador/palabras.xml");//xshd
            areatexto.SyntaxHighlighting = HighlightingLoader.Load(reader, HighlightingManager.Instance);
            areatexto.TextArea.Caret.PositionChanged += onCursorPositionChanged;
        }

       
        private void onCursorPositionChanged(object sender, EventArgs e)
        {
            int caretOffset=areatexto.TextArea.Caret.Offset;
            DocumentLine caretLine=areatexto.Document.GetLineByOffset(caretOffset);
            linea = caretLine.LineNumber;
            colum = caretOffset - caretLine.Offset + 1;

            values.Linea = linea;
            values.Colum = colum;

            //Debug.WriteLine("Linea: {0}, Columna: {1}",caretLine.LineNumber,caretOffset-caretLine.Offset+1);
            //this.cursor.Text = ("Linea: , Columna: "+ caretLine.LineNumber + caretOffset - caretLine.Offset + 1);
            
        }

        private void abrirarchivo(object sender, RoutedEventArgs e)
        {
            //OpenFileDialog openFile = new OpenFileDialog();
            openFileDialog.Filter = "Texto|*.txt";


            if (openFileDialog.ShowDialog() == true)
            {
                this.saveFileDialog.FileName = this.openFileDialog.FileName;
                this.areatexto.Text = File.ReadAllText(this.saveFileDialog.FileName);


            }
        }

        private void guardar(object sender, RoutedEventArgs e)
        {
            this.saveFileDialog.Filter = "Text file (*.txt)|*.txt";
            if (File.Exists(this.saveFileDialog.FileName) || File.Exists(this.openFileDialog.FileName))
            {
                if (File.Exists(this.saveFileDialog.FileName))
                    File.WriteAllText(this.saveFileDialog.FileName, this.areatexto.Text);
                else File.WriteAllText(this.openFileDialog.FileName, this.areatexto.Text);
            }
            else
            {
                if (this.saveFileDialog.ShowDialog() == true)
                {
                    this.openFileDialog.FileName = this.saveFileDialog.FileName;
                    File.WriteAllText(this.saveFileDialog.FileName, this.areatexto.Text);
                }
            }
        }

        private void guardarcomo(object sender, RoutedEventArgs e)
        {
            this.openFileDialog.Filter = "Text file (*.txt)|*.txt";
            if (File.Exists(this.openFileDialog.FileName) || File.Exists(this.saveFileDialog.FileName))
            {
                if (File.Exists(this.openFileDialog.FileName))
                    File.WriteAllText(this.openFileDialog.FileName, this.areatexto.Text);
                else File.WriteAllText(this.saveFileDialog.FileName, this.areatexto.Text);
            }
            else
            {
                if (this.openFileDialog.ShowDialog() == true)
                {
                    this.saveFileDialog.FileName = this.openFileDialog.FileName;
                    File.WriteAllText(this.openFileDialog.FileName, this.areatexto.Text);
                }
            }
        }

        private void salir(object sender, RoutedEventArgs e)
        {
            Environment.Exit(0);
        }

        private void LexicoCodigo(object sender, RoutedEventArgs e)
        {

            
            //Se lee el archivo de Lexico (Tokens)
            //OpenFileDialog openFile = new OpenFileDialog();
            string text = File.ReadAllText(Directory.GetCurrentDirectory() + "\\archToken.txt");
            this.codigofinal.Text = text;


            string errores="";
            errores = "Carácter\tLinea\t\tColumna\n";
            errores+= File.ReadAllText(Directory.GetCurrentDirectory() + "\\archError.txt");
            this.textoerr.Text = errores;

            this.frame.Navigate(new System.Uri("./Lexico/tablaLexico.xaml", UriKind.RelativeOrAbsolute));


        }

        
        private void ejecutarLexico(string file)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "cmd.exe",

                Arguments = "/c "+ Directory.GetCurrentDirectory() + "\\AnalizadorLexico\\AnalizadorLexico\\bin\\Debug\\net6.0\\AnalizadorLexico "+file,

                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            Process process = new Process
            {
                StartInfo = startInfo
            };
            process.Start();
            string output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
            this.codigofinal.Text = output;
        }

        private void eventoSintactico(object sender, RoutedEventArgs e)
        {
            string errores = "";
            errores += File.ReadAllText(Directory.GetCurrentDirectory() + "\\archErrorSintactico.txt");
            this.textoerr.Text = errores;
            this.frame.Navigate(new System.Uri("./Sintactico/ArbolSintactico.xaml", UriKind.RelativeOrAbsolute));
        }




        private void Compi(object sender, RoutedEventArgs e)
        {
            if (File.Exists(this.saveFileDialog.FileName))
            {
                this.archAnalizarLex = this.saveFileDialog.FileName;
                this.ejecutarLexico(this.archAnalizarLex);
                this.ejecutarSintactico();

            }
            else if (File.Exists(this.openFileDialog.FileName))
            {
                this.archAnalizarLex = this.openFileDialog.FileName;
                this.ejecutarLexico(this.archAnalizarLex);
                this.ejecutarSintactico();
            }
            else
            {
                MessageBox.Show("Guarda tu archivo antes de ejecutarlo");
            }
        }

        private void ejecutarSintactico()
        {
            
            string ruta = Directory.GetCurrentDirectory();
            Process process;



            string coman = "/c python " + ruta + "\\parse.py ";
            Debug.WriteLine(coman);
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "cmd.exe",
                Arguments = coman,
                RedirectStandardOutput = false,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            process = new Process
            {
                StartInfo = startInfo
            };
            process.Start();
        }

        

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            //pruebas

        }

        private void cerrar(object sender, RoutedEventArgs e)
        {
            if (this.openFileDialog.FileName == null || this.openFileDialog.FileName == "")
            {
                if (this.areatexto.Text != "")
                {
                    this.saveFileDialog.Filter = "Text file (*.txt)|*.txt";

                    if (this.saveFileDialog.ShowDialog() == true)
                    {
                        

                        File.WriteAllText(this.saveFileDialog.FileName, this.areatexto.Text);

                    }
                }
                this.areatexto.Text = "";
                this.saveFileDialog.FileName = "";
                this.openFileDialog.FileName = "";
                return;
            }

            string txt = File.ReadAllText(this.openFileDialog.FileName);
            if (txt == this.areatexto.Text)
            {

            }
            else
            {
                if (MessageBox.Show("¿Deseas guardar tu archivo?", "", MessageBoxButton.YesNo) == MessageBoxResult.Yes)
                {
                    File.WriteAllText(this.openFileDialog.FileName, this.areatexto.Text);
                    MessageBox.Show("Guardando");

                }

            }
            this.areatexto.Text = "";
            this.saveFileDialog.FileName = "";
            this.openFileDialog.FileName = "";


        }





    }
}
