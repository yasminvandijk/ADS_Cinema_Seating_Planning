using System;
using System.Collections.Generic;

namespace Offline_Branch_and_Bound
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            OfflineInput input = ParseInput.ParseOfflineInput();

            input.cinema.printCinema();
        }
    }

    public enum Seat
    {
        NoSeat,
        Empty,
        Occupied,
        Unavailable
    }

    public struct Location
    {
        public int x;
        public int y;
    }

    public class Cinema
    {
        public int rows;
        public int columns;
        public Seat[,] layout;
        public int totalPlaced = 0;
        public int totalEmptySeats;
        //Seatlist: List of Dictionaries where key = group size of chairs, value = index leftmost chair
        public Dictionary<int, int>[] seatList = new Dictionary<int, int>[rows];

        public Cinema(int rows, int columns, Seat[,] layout)
        {
            this.rows = rows;
            this.columns = columns;
            this.layout = layout;
            this.totalEmptySeats = countEmptySeats();
        }

        /// <summary>
        /// creates a copy of the given cinema
        /// </summary>
        /// <param name="cinema"></param>
        public Cinema(Cinema cinema)
        {
            rows = cinema.rows;
            columns = cinema.columns;
            layout = new Seat[rows, columns];

            for (int y = 0; y < rows; y++)
            {
                for (int x = 0; x < columns; x++)
                {
                    layout[y, x] = cinema.layout[y, x];
                }
            }
            totalEmptySeats = countEmptySeats();
        }

        public void initSeatList()
        {
            for (int i = 0; i < rows; i++)
            {
                seatList[i] = getAvailableSeats(i);
            }
        }

        public int countEmptySeats()
        {
            int r = 0;
            for (int i = 0; i < this.columns; i++)
            {
                for (int j = 0; j < this.rows; j++)
                {
                    if (layout[i, j] == Seat.Empty) r++;
                }
            }

            return r;
        }

        public void printCinema()
        {
            for (int i = 0; i < columns; i++)
            {
                for (int j = 0; j < rows; j++)
                {
                    if (this.layout[i, j] == Seat.NoSeat) Console.Write("0");
                    if (this.layout[i, j] == Seat.Empty) Console.Write("1");
                    if (this.layout[i, j] == Seat.Occupied) Console.Write("x");
                    if (this.layout[i, j] == Seat.Unavailable) Console.Write("+");
                }
                Console.WriteLine();
            }
        }

        public void printOutput()
        {
            for (int i = 0; i < columns; i++)
            {
                for (int j = 0; j < rows; j++)
                {
                    if (this.layout[i, j] == Seat.NoSeat) Console.Write("0");
                    if (this.layout[i, j] == Seat.Empty || this.layout[i, j] == Seat.Unavailable) Console.Write("1");
                    if (this.layout[i, j] == Seat.Occupied) Console.Write("x");
                }
                Console.Write(Environment.NewLine);
            }
        }

        public int score()
        {
            return totalPlaced + totalEmptySeats;
        }

        public Dictionary<int, int> getAvailableSeats(int row)
        {
            Dictionary<int, int> result = new Dictionary<int, int>();
            int ind = 0;
            while (ind < columns)
            {
                int seats = 0;
                int startind = ind;

                while (ind < columns && layout[row, ind] == Seat.Empty)
                {
                    ind += 1;
                    seats += 1;
                }

                if (seats > 0)
                {
                    result.Add(seats, startind);
                }
            }
            return result;
        }

        public void markUnavailable(int x, int y)
        {
            if (layout[x, y] == Seat.Empty)
            {
                layout[x, y] = Seat.Unavailable;
                totalEmptySeats -= 1;
            }
        }

        public void placeGroup(int x, int y, int size)
        {
            for (int i = 0; i < size; i++)
            {
                layout[x + i, y] = Seat.Occupied;
            }

            if (x > 0)
            {
                for (int u = 0; u < rows; u++)
                {
                    markUnavailable(x + u, y - 1);
                }
                if (x > 0)
                {
                    markUnavailable(x - 1, y - 1);
                }
                if (x + size < columns)
                {
                    markUnavailable(x+size, y-1);
                }
                
            }

            if (y + 1 < rows)
            {
                for (int v = 0; v < rows; v++)
                {
                    markUnavailable(x + v, y + 1);
                }
                if (x > 0)
                {
                    markUnavailable(x - 1, y + 1);
                }
                if (x + size < columns)
                {
                    markUnavailable(x + size, y + 1);
                }
            }

            if (x > 0)
            {
                markUnavailable(x - 1, y);
            }
            if (x > 1)
            {
                markUnavailable(x - 2, y);
            }
            if (x + size < columns)
            {
                markUnavailable(x+size, y);
            }
            if (x + size + 1 < columns)
            {
                markUnavailable(x + size + 1, y);
            }
        }

        public bool findSeating(int size)
        {
            if (size > columns) return false;

            for (int i = 0; i < rows; i++)
            {
                
            }
        }
    }
}
