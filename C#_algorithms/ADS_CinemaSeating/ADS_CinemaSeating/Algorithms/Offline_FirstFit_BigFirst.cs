using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using ADS_CinemaSeating.CinemaLayout;

namespace ADS_CinemaSeating.Algorithms
{
    /// <summary>
    /// places biggest groups first, at the first place where they fit
    /// </summary>
    class Offline_FirstFit_BigFirst
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

            // read nr of groups for each groupSize
            int[] groupAmounts = new int[8];

            string[] amounts = streamReader.ReadLine().Split();
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

                    (int y, int x, int size) seating = cinema.FindFirstSeating(groupSize);

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
