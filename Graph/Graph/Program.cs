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
            //graph = Firstfit(input, graph);
            graph.PrintGraph();


            #endregion
            //Console.WriteLine();
            //graph.PrintGraph();

            //Console.WriteLine();
            Console.ReadLine();
            //graph.GetTranspose();
        }

        public static Graph Firstfit(int[] inputs, Graph graph)
        {
            Node node = graph.nodes[0, 0];
            int go = 0;
            for (int i = 0; i < 8; i++)
            {
                if (i < graph.columns)
                {
                    if (graph.nodes[0, i].isSeat)
                    {
                        graph.nodes[0, i].Occupied = true;
                        go++;
                    }

                    else break;
                }


            }

            return graph;
        }
        public static int Overlapcount(Node[] nodes, Graph gra)
        {
            int go = 0;
            for (int i = 0; i < nodes.Length; i++)
            {
                for (int j = 0; j < gra.nodes[nodes[i].idx, nodes[i].idy].edges.Count; j++)
                {
                    if (gra.nodes[nodes[j].idx, nodes[j].idy].isSeat) go++;
                }

            }
            return go;
        }/*
        public static int Place(Node[] nodes, Graph gra)
        {
                int[] dist = new int[V]; // The output array. dist[i] 
                                         // will hold the shortest 
                                         // distance from src to i 

                // sptSet[i] will true if vertex 
                // i is included in shortest path 
                // tree or shortest distance from 
                // src to i is finalized 
                bool[] sptSet = new bool[V];

                // Initialize all distances as 
                // INFINITE and stpSet[] as false 
                for (int i = 0; i < V; i++)
                {
                    dist[i] = int.MaxValue;
                    sptSet[i] = false;
                }

                // Distance of source vertex 
                // from itself is always 0 
                dist[src] = 0;

                // Find shortest path for all vertices 
                for (int count = 0; count < V - 1; count++)
                {
                    // Pick the minimum distance vertex 
                    // from the set of vertices not yet 
                    // processed. u is always equal to 
                    // src in first iteration. 
                    int u = minDistance(dist, sptSet);

                    // Mark the picked vertex as processed 
                    sptSet[u] = true;

                    // Update dist value of the adjacent 
                    // vertices of the picked vertex. 
                    for (int v = 0; v < V; v++)

                        // Update dist[v] only if is not in 
                        // sptSet, there is an edge from u 
                        // to v, and total weight of path 
                        // from src to v through u is smaller 
                        // than current value of dist[v] 
                        if (!sptSet[v] && graph[u, v] != 0 && dist[u] != int.MaxValue && dist[u] + graph[u, v] < dist[v])
                            dist[v] = dist[u] + graph[u, v];
                }

                // print the constructed distance array 
                printSolution(dist);
            
        }
    }*/
    }

 
   /* void BellmanFord(Graph graph, int src)
    {
        int V = graph.V, E = graph.E;
        int[] dist = new int[V];

        // Step 1: Initialize distances from src to all other 
        // vertices as INFINITE 
        for (int i = 0; i < V; ++i)
            dist[i] = int.MaxValue;
        dist[src] = 0;

        // Step 2: Relax all edges |V| - 1 times. A simple 
        // shortest path from src to any other vertex can 
        // have at-most |V| - 1 edges 
        for (int i = 1; i < V; ++i)
        {
            for (int j = 0; j < E; ++j)
            {
                int u = graph.edge[j].src;
                int v = graph.edge[j].dest;
                int weight = graph.edge[j].weight;
                if (dist[u] != int.MaxValue && dist[u] + weight < dist[v])
                    dist[v] = dist[u] + weight;
            }
        }
    }*/



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