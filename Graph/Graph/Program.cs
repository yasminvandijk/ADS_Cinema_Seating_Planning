using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DAGALG
{
    class Program
    {

        static void Main(string[] args)
        {
            Graph graph;

            #region input
            int rows = Int32.Parse(Console.ReadLine());
            int columns = Int32.Parse(Console.ReadLine());
            graph = new Graph(rows, columns, rows * columns);
            int go = 0;

            for (int i = 0; i < rows; i++)
            {
                string split = Console.ReadLine();
                char[] str = split.ToCharArray();
                for (int j = 0; j < columns; j++)
                {
                    if (j + 1 < rows)
                        graph.AddEdge(i, j, i, j + 1);
                    if (j - 1 >= 0)
                        graph.AddEdge(i, j, i, j - 1);
                    if (i + 1 < columns)
                        graph.AddEdge(i, j, i + 1, j);
                    if (i + 2 < columns)
                        graph.AddEdge(i, j, i + 2, j);
                    if (i - 1 >= 0)
                        graph.AddEdge(i, j, i - 1, j);
                    if (i - 2 >= 0)
                        graph.AddEdge(i, j, i - 2, j);
                    if (i + 1 < columns && j + 1 < rows)
                        graph.AddEdge(i, j, i + 1, j + 1);
                    if (i - 1 >= 0 && j + 1 < rows)
                        graph.AddEdge(i, j, i - 1, j + 1);
                    if (i + 1 < columns && j - 1 >= 0)
                        graph.AddEdge(i, j, i + 1, j - 1);
                    if (j - 1 >= 0 && i - 1 >= 0)
                        graph.AddEdge(i, j, i - 1, j - 1);
                    if (str[j] == '1') graph.AddSeat(i, j);
                    go++;

                }
            }
            string spl = Console.ReadLine();
            char[] inu = spl.ToCharArray();
            int[] input = new int[inu.Length];
            //int[] Aint = Array.ConvertAll(A, c => (int)Char.GetNumericValue(c));
            graph.inputs = input;
            Console.WriteLine();
            graph = Fit(input, graph);
            graph.PrintGraph();


            #endregion
            //Console.WriteLine();
            //graph.PrintGraph();

            //Console.WriteLine();
            Console.ReadLine();
            //graph.GetTranspose();
        }

        public static Graph Fit(int[] inputs, Graph graph)
        {
            Node node = graph.nodes[0, 0];
            int go = 0;
            for (int i = 0; i <  graph.columns; i++)
            {
               for (int j = 0; j <  graph.rows; j++)
                {
                    if (graph.nodes[j, i].isSeat && graph.nodes[j,i].Blocked == false && graph.nodes[j,i].Occupied == false)
                    {
                        graph.nodes[j, i].Occupied = true;
                        Node[] n = new Node[1];
                        n[0] = graph.nodes[j, i];
                        graph = Overlap(n, graph);
                    }
                }


            }

            return graph;
        }

        ///registers the blocked seats
        public static Graph Overlap(Node[] nodes, Graph gra)
        {
            int go = 0;
            for (int i = 0; i < nodes.Length; i++)
            {
                for (int j = 0; j < gra.nodes[nodes[i].idx, nodes[i].idy].edges.Count; j++)
                {
                    if (gra.nodes[nodes[i].edges[j].idx, nodes[i].edges[j].idy].isSeat) gra.nodes[nodes[i].edges[j].idx, nodes[i].edges[j].idy].Blocked = true;
                }

            }
            return gra;
        }

        }

    class Graph
    {
        public int rows;
        public int columns;
        public int vertices;
        public int[] inputs = new int[8];
        public Node[,] nodes;

        public Graph(int rows, int columns, int vertices)
        {
            this.vertices = vertices;
            this.rows = rows;
            this.columns = columns;
            nodes = new Node[columns,rows];
            int go = 0;
            for (int i = 0; i < columns; i++)
            {
                for (int j = 0; j < rows; j++)
                {
                    nodes[i, j] = new Node(i, j, go);
                    go++;
                }
            }
        }

        public void AddEdge(int ax, int ay, int bx, int by)
        {
            nodes[ax, ay].edges.Add(nodes[bx, by]);
        }

        public void AddSeat(int i, int j)
        {
            nodes[i, j].isSeat = true;
        }


        public void PrintGraph()
        {
            int go = 0;
            for (int i = 0; i < nodes.GetLength(0); i++)
            {
                for (int j = 0; j < nodes.GetLength(1); j++)
                {
                    go++;
                    Console.WriteLine((go) + " | " + nodes[i, j].EdgesToString());
                }
            }

            Console.WriteLine();
            for (int i = 0; i < nodes.GetLength(0); i++)
            {
                for (int j = 0; j < nodes.GetLength(1); j++)
            {
                    if (nodes[i,j].Occupied == true)
                        Console.Write("x ");
                    else if (nodes[i,j].Blocked == true)
                        Console.Write("+ ");
                    else if (nodes[i, j].isSeat == true)
                        Console.Write("1 ");
                    else Console.Write("0 ");
                }
                Console.Write(Environment.NewLine + Environment.NewLine);
            }
        }
    }

    class Node
    {
        public int idx;
        public int idy;
        public int id;
        public bool isSeat = false;
        public bool Occupied;
        public bool Blocked;
        public List<Node> edges;
        public Node(int i, int j, int id)
        {
            idx = i;
            idy = j;
            edges = new List<Node>();
        }

        public string EdgesToString()
        {
            string r = "";
            foreach (Node n in edges)
            {
                r += " " + (n.idx) + "," + (n.idy) + " ";
            }

            return r;

        }
    }
}