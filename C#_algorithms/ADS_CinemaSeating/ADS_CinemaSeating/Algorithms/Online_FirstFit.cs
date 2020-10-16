using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using ADS_CinemaSeating.CinemaLayout;

namespace ADS_CinemaSeating.Algorithms
{
    /// <summary>
    /// places groups on the first possible place where they fit,
    /// finds places by looking from top to bottom row, left to right
    /// </summary>
    class Online_FirstFit
    {
        public static TestResult Solve(string filepath, long timeout_ms)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            
            // read nr of rows and columns from file
            System.IO.StreamReader streamReader = new System.IO.StreamReader(filepath);
            int.TryParse(streamReader.ReadLine(), out int nrRows);
            int.TryParse(streamReader.ReadLine(), out int nrCols);

            Cinema cinema = new Cinema(nrRows, nrCols);

            // read cinema layout from file
            for (int y = 0; y < nrRows; y++)
            {
                string line = streamReader.ReadLine();
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

            // read groupsizes from file and fit them in the cinema
            while (true)
            {
                // check if total run time exceeds timeout
                if (stopwatch.ElapsedMilliseconds > timeout_ms)
                {
                    break;
                }
                
                int.TryParse(streamReader.ReadLine(), out int groupSize);
                if (groupSize == 0) { break; }

                (int y, int x, int size) seating = cinema.FindFirstSeating(groupSize);

                if (seating != (0, 0, 0))
                {
                    cinema.SetGroup(seating.y, seating.x, groupSize);
                }
            }

            stopwatch.Stop();

            TestResult result = new TestResult
            {
                Cinema = cinema,
                RunTime_ms = stopwatch.ElapsedMilliseconds
            };

            return result;
        }
    }
}
