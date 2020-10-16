using System;
using System.Collections.Generic;
using System.Text;
using System.Diagnostics;
using ADS_CinemaSeating.CinemaLayout;
using System.Linq;

namespace ADS_CinemaSeating.Algorithms
{
    class PartialSolution
    {
        public Cinema Cinema { get; set; }
        public int[] GroupAmounts { get; set; }
    }
    
    /// <summary>
    /// finds the optimal solution through a branch and bound strategy
    /// new partial solutions are created by placing groups, or marking a single seat as unused
    /// the search space is bounded by checking whether a partial solution can still improve on 
    /// the best found solution so far
    /// </summary>
    class Offline_Branch_And_Bound
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

            // keep a list of partial solutions
            MaxPriorityQueue<PartialSolution> queue = new MaxPriorityQueue<PartialSolution>();
            queue.Add(cinema.NrOccupiedSeats, new PartialSolution { Cinema = cinema, GroupAmounts = groupAmounts });

            // best found solution so far
            Cinema bestFoundCinema = cinema;

            // set a limit on the total size of the queue to not fill up the memory completely
            int maxQueueSize = 1000000000 / (nrRows * nrCols);

            // fill the cinema using a branch and bound method
            while (!queue.Empty())
            {
                // check if total runtime exceeds timeout
                if (stopwatch.ElapsedMilliseconds > timeout_ms)
                {
                    break;
                }

                // make sure the queue doesn't exceed the maximum size
                queue.TrimQueueSize(maxQueueSize);

                PartialSolution partialSolution = queue.Get();

                // bound condition
                if (partialSolution.Cinema.MaxScore < bestFoundCinema.NrOccupiedSeats)
                {
                    continue;
                }

                // check if this solution is better than the best solution found so far
                if (partialSolution.Cinema.NrOccupiedSeats > bestFoundCinema.NrOccupiedSeats)
                {
                    bestFoundCinema = partialSolution.Cinema.GetCopy();
                }
                
                // get a group of empty seats
                (int rowIndex, int colIndex, int seatGroupSize) seating = partialSolution.Cinema.FindFirstSeating(1);

                if (seating == (0, 0, 0))
                {
                    continue;
                }

                // attempt to fit every group
                for (int i = Math.Min(8, seating.seatGroupSize); i > 0; i--)
                {
                    if (partialSolution.GroupAmounts[i - 1] > 0)
                    {
                        // create and add a new partial solution by placing group of size i
                        // copy cinema
                        Cinema newCinema = partialSolution.Cinema.GetCopy();
                        // copy groupamounts
                        int[] newGroupAmounts = new int[8];
                        for (int x = 0; x < 8; x++)
                        {
                            newGroupAmounts[x] = partialSolution.GroupAmounts[x];
                        }
                        // place group in cinema copy
                        newCinema.SetGroup(seating.rowIndex, seating.colIndex, i);
                        // update groupamounts copy
                        newGroupAmounts[i - 1]--;
                        PartialSolution newSolution = new PartialSolution()
                        {
                            Cinema = newCinema,
                            GroupAmounts = newGroupAmounts
                        };
                        queue.Add(newCinema.NrOccupiedSeats, newSolution);
                    }
                }
                // create a new partial solution by marking one seat as unavailable
                partialSolution.Cinema.MarkSeatAsUnused(seating.rowIndex, seating.colIndex);
                queue.Add(partialSolution.Cinema.NrOccupiedSeats, partialSolution);
            }

            stopwatch.Stop();

            TestResult result = new TestResult()
            {
                Cinema = bestFoundCinema,
                RunTime_ms = stopwatch.ElapsedMilliseconds
            };

            return result;
        }
    }
}
