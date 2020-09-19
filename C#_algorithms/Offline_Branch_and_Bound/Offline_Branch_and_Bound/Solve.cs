using System;
using System.Collections.Generic;
using System.Text;

namespace Offline_Branch_and_Bound
{
    public class Solve
    {
        /// <summary>
        /// attempts to find places for as many visitors as possible using a branch and bound strategy
        /// </summary>
        /// <param name="cinema">the initial cinema</param>
        /// <param name="nrGroups">the number of groups for each group size</param>
        /// <returns></returns>
        public static Cinema BranchAndBound(Cinema cinema, int[] nrGroups)
        {
            // keep track of best partial solution we have seen
            Cinema bestCinema = new Cinema(cinema);
            int maxNrPlaced = 0;

            // priority queue with partial solutions sorted on score in descending order
            MaxPriorityQueue<PartialSolution> queue = new MaxPriorityQueue<PartialSolution>();

            queue.Add(cinema.score(), new PartialSolution { cinema = cinema, nrGroupsRemaining = nrGroups });

            while(!queue.Empty())
            {
                PartialSolution partialSolution = queue.Get();

                // loop over all groupSizes
                for (int groupIndex = 0; groupIndex < partialSolution.nrGroupsRemaining.Length; groupIndex++)
                {
                    if (partialSolution.nrGroupsRemaining[groupIndex] > 0)
                    {
                        // bound; only check partial solution which could be better than the best solution found so far
                        if (partialSolution.cinema.score() > maxNrPlaced)
                        {
                            // branch; create new partial solutions
                            Cinema cinemaCopy = new Cinema(partialSolution.cinema);
                            if (cinemaCopy.findSeating(groupIndex + 1))
                            {
                                // new partial solution found
                                int[] nrGroupsRemainingCopy = (int[])partialSolution.nrGroupsRemaining.Clone();
                                nrGroupsRemainingCopy[groupIndex]--;

                                // check if this partial solution is better than best solution seen so far
                                if (cinemaCopy.totalPlaced > maxNrPlaced)
                                {
                                    bestCinema = new Cinema(cinemaCopy);
                                    maxNrPlaced = cinemaCopy.totalPlaced;
                                }

                                // add partial solution to the queue
                                queue.Add(cinemaCopy.score(), new PartialSolution { cinema = cinemaCopy, nrGroupsRemaining = nrGroupsRemainingCopy });
                            }
                        }
                    }
                }
            }

            return bestCinema;
        }
    }

    public class PartialSolution
    {
        public Cinema cinema { get; set; }
        public int[] nrGroupsRemaining { get; set; }
    }
}
