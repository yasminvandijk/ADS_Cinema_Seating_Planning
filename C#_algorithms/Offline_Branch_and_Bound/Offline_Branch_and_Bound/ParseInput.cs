using System;
using System.Collections.Generic;
using System.Text;

namespace Offline_Branch_and_Bound
{
    class ParseInput
    {
        public static OfflineInput ParseOfflineInput()
        {
            // nr. rows
            if (!int.TryParse(Console.ReadLine(), out int rows)) 
            {
                throw new Exception("unable to parse number or rows from input");
            }
            
            // nr. columns
            if (!int.TryParse(Console.ReadLine(), out int columns))
            {
                throw new Exception("unable to parse number of columns from input");
            }

            // layout
            Seat[,] layout = new Seat[rows, columns];
            for (int y = 0; y < rows; y++)
            {
                string rowInput = Console.ReadLine();

                if (rowInput.Length < columns)
                {
                    throw new Exception($"number of characters in input for row {y + 1} does not match {columns}");
                }
                
                for (int x = 0; x < columns; x++)
                {
                    if (rowInput[x] == '0')
                    {
                        layout[y, x] = Seat.NoSeat;
                    }
                    else if (rowInput[x] == '1')
                    {
                        layout[y, x] = Seat.Empty;
                    }
                    else
                    {
                        throw new Exception($"unexpected character in input at row {y + 1} and column {x + 1}");
                    }
                }
            }

            // nr. of groups per group size
            string[] groupsInput = Console.ReadLine().Split(' ');
            int[] nrGroups = new int[groupsInput.Length];

            for (int i = 0; i < groupsInput.Length; i++)
            {
                if (!int.TryParse(groupsInput[i], out int nr))
                {
                    throw new Exception($"unable to parse {groupsInput[i]} to a number of groups");
                }

                nrGroups[i] = nr;
            }

            return new OfflineInput
            {
                cinema = new Cinema(rows, columns, layout),
                nrGroups = nrGroups
            };
        }
    }

    public class OfflineInput
    {
        public Cinema cinema { get; set; }
        public int[] nrGroups { get; set; }
    }
}
