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

                // TODO;
            }
        }
    }

    public class PartialSolution
    {
        public Cinema cinema { get; set; }
        public int[] nrGroupsRemaining { get; set; }
    }
}
