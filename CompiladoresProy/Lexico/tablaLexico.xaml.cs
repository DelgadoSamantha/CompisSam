using System;
using System.Collections.Generic;
using System.IO;
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

namespace CompiladoresProy.Lexico
{
    /// <summary>
    /// Lógica de interacción para tablaLexico.xaml
    /// </summary>
    
    public class Item
    {
        public string token { get; set; }
        public string lexema { get; set; }
    }

    public partial class tablaLexico : Page
    {
        private string file;
        public tablaLexico()
        {
            InitializeComponent();
            this.file = @"archToken.txt";
            this.fillDataGrid();
        }

        public async void fillDataGrid()
        {
            using (StreamReader reader = new StreamReader(this.file))
            {
                string line;
                char[] separador = { ' ', '\t' };
                while ((line = reader.ReadLine()) != null)
                {
                    string[] lines = line.Split(separador);
                    this.dataGrid.Items.Add(new Item() { token = lines[0], lexema = lines[1] });
                    await Task.Delay(10);
                }
            }
        }
    }
}
