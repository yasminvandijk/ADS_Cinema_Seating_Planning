using ADS_CinemaSeating.CinemaLayout;
using System;
using System.Diagnostics;

namespace Offline_BestFit_BigFirst
{
    class Program
    {
        /// <summary>
        /// places biggest groups first, at the first place where they create the least amount of new unavailable seats
        /// </summary>
        static void Main(string[] args)
        {
            long timeout_ms = 30 * 60 * 1000;            
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            
            // read nr of rows and columns from input
            int.TryParse(Console.ReadLine(), out int nrRows);
            int.TryParse(Console.ReadLine(), out int nrCols);

            Cinema cinema = new Cinema(nrRows, nrCols);

            // read cinema layout from input
            for (int y = 0; y < nrRows; y++)
            {
                string line = Console.ReadLine();
                for (int x = 0; x < nrCols; x++)
                {
                    switch (line[x])
                    {
                        case '0':
                            cinema.SetSeat(y, x, Seat.NoSeat);
                            break;
                        case '1':
                            cinema.SetSeat(y, x, Seat.Empty);
                            break;
                    }
                }
            }

            cinema.UpdateAvailableSeats();

            // read nr of groups for each groupSize
            int[] groupAmounts = new int[8];

            string[] amounts = Console.ReadLine().Split();
            for (int i = 0; i < 8; i++)
            {
                int.TryParse(amounts[i], out groupAmounts[i]);
            }

            // find a seating for each group, starting with the biggest groups
            for (int i = 7; i >= 0; i--)
            {
                // check if total runtime exceeds timeout
                if (stopwatch.ElapsedMilliseconds > timeout_ms)
                {
                    break;
                }

                int groupSize = i + 1;

                for (int j = 0; j < groupAmounts[i]; j++)
                {
                    // check if total runtime exceeds timeout
                    if (stopwatch.ElapsedMilliseconds > timeout_ms)
                    {
                        break;
                    }

                    (int y, int x, int size) seating = cinema.FindBestSeating(groupSize);

                    if (seating != (0, 0, 0))
                    {
                        cinema.SetGroup(seating.y, seating.x, groupSize);
                    }
                    else
                    {
                        break;
                    }
                }
            }

            cinema.PrintOutput();
        }
    }
}
