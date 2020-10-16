using ADS_CinemaSeating.CinemaLayout;
using System;
using System.Diagnostics;

namespace Online_BestFit
{
    class Program
    {
        static void Main(string[] args)
        {
            long timeout_ms = 30 * 60 * 1000;
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();

            // read nr of rows and columns from file
            int.TryParse(Console.ReadLine(), out int nrRows);
            int.TryParse(Console.ReadLine(), out int nrCols);

            Cinema cinema = new Cinema(nrRows, nrCols);

            // read cinema layout from file
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

            // read groupsizes from input
            while (true)
            {
                // check if total runtime exceeds timeout
                if (stopwatch.ElapsedMilliseconds > timeout_ms)
                {
                    break;
                }

                int.TryParse(Console.ReadLine(), out int groupSize);
                if (groupSize == 0) { break; }

                (int y, int x, int size) seating = cinema.FindBestSeating(groupSize);

                if (seating != (0, 0, 0))
                {
                    cinema.SetGroup(seating.y, seating.x, groupSize);
                    Console.WriteLine($"{seating.y + 1}, {seating.x + 1}");
                }
                else
                {
                    Console.WriteLine($"0, 0");
                }
            }
        }
    }
}
