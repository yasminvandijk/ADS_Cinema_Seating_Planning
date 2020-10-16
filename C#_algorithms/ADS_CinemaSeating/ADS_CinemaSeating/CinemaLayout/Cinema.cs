using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ADS_CinemaSeating.CinemaLayout
{
    public class Cinema
    {
        public List<(int colStartIndex, int seatGroupSize)>[] _availableSeats { get; private set; }

        public int NrOccupiedSeats { get; private set; }
        public int NrAvailableSeats { get; private set; }
        public int NrRows { get; private set; }
        public int NrCols { get; private set; }
        public Seat[,] Layout { get; private set; }

        public int MaxScore { get { return NrOccupiedSeats + NrAvailableSeats; } }

        public Cinema(int nrRows, int nrCols)
        {
            NrRows = nrRows;
            NrCols = nrCols;
            Layout = new Seat[nrRows, nrCols];
            
            _availableSeats = new List<(int, int)>[nrRows];
            for (int i = 0; i < nrRows; i++)
            {
                _availableSeats[i] = new List<(int, int)>();
            }
        }

        /// <summary>
        /// get a copy of this cinema
        /// </summary>
        /// <returns></returns>
        public Cinema GetCopy()
        {
            Cinema copy = new Cinema(NrRows, NrCols);
            // copy cinema layout
            for (int y = 0; y < NrRows; y++)
            {
                for (int x = 0; x < NrCols; x++)
                {
                    copy.SetSeat(y, x, Layout[y, x]);
                }
            }

            // copy available seats
            copy._availableSeats = new List<(int colStartIndex, int seatGroupSize)>[NrRows];
            for (int y = 0; y < NrRows; y++)
            {
                copy._availableSeats[y] = new List<(int colStartIndex, int seatGroupSize)>();
                for (int i = 0; i < _availableSeats[y].Count; i++)
                {
                    copy._availableSeats[y].Add(_availableSeats[y][i]);
                }
            }

            return copy;
        }

        /// <summary>
        /// update the available seats lists for all rows
        /// </summary>
        public void UpdateAvailableSeats()
        {
            for (int y = 0; y < NrRows; y++)
            {
                UpdateAvailableSeats(y, true);
            }
        }
        
        /// <summary>
        /// update available seats list for a given row
        /// </summary>
        /// <param name="rowIndex"></param>
        /// <param name="updateIfEmpty">update list if it is empty</param>
        private void UpdateAvailableSeats(int rowIndex, bool updateIfEmpty = false)
        {
            if (!updateIfEmpty && _availableSeats[rowIndex].Count == 0)
            {
                return;
            }
            
            _availableSeats[rowIndex].Clear();

            int colIndex = 0;

            while (colIndex < NrCols)
            {
                int startIndex = colIndex;
                int count = 0;

                while (colIndex < NrCols && Layout[rowIndex, colIndex] == Seat.Empty)
                {
                    colIndex++;
                    count++;
                }

                if (count > 0)
                {
                    _availableSeats[rowIndex].Add((startIndex, count));
                }
                colIndex++;
            }
        }

        /// <summary>
        /// set the seat type at a given row and column index
        /// </summary>
        /// <param name="rowIndex"></param>
        /// <param name="colIndex"></param>
        /// <param name="seatType"></param>
        public void SetSeat(int rowIndex, int colIndex, Seat seatType)
        {
            Layout[rowIndex, colIndex] = seatType;
            if (seatType == Seat.Empty)
            {
                NrAvailableSeats++;
            }
            else if (seatType == Seat.Occupied)
            {
                NrOccupiedSeats++;
            }
        }

        /// <summary>
        /// print cinema to the console, with unavailable seats as '+'
        /// </summary>
        public void PrintCinema()
        {
            Console.WriteLine();
            for (int y = 0; y < NrRows; y++)
            {
                for (int x = 0; x < NrCols; x++)
                {
                    switch (Layout[y, x])
                    {
                        case Seat.NoSeat:
                            Console.Write('0');
                            break;
                        case Seat.Empty:
                            Console.Write('1');
                            break;
                        case Seat.Occupied:
                            Console.Write('x');
                            break;
                        case Seat.Unavailable:
                            Console.Write('+');
                            break;
                    }
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        /// <summary>
        /// print cinema to the console in the required output format
        /// </summary>
        public void PrintOutput()
        {
            for (int y = 0; y < NrRows; y++)
            {
                for (int x = 0; x < NrCols; x++)
                {
                    switch (Layout[y, x])
                    {
                        case Seat.NoSeat:
                            Console.Write('0');
                            break;
                        case Seat.Empty:
                        case Seat.Unavailable:
                            Console.Write('1');
                            break;
                        case Seat.Occupied:
                            Console.Write('x');
                            break;
                    }
                }
                Console.WriteLine();
            }
        }

        /// <summary>
        /// place a group of the given size with the leftmost person at the row and column index
        /// </summary>
        /// <param name="rowIndex"></param>
        /// <param name="colIndex"></param>
        /// <param name="groupSize"></param>
        public void SetGroup(int rowIndex, int colIndex, int groupSize)
        {
            // mark seats as occupied
            for (int x = 0; x < groupSize; x++)
            {
                Layout[rowIndex, colIndex + x] = Seat.Occupied;
            }
            NrOccupiedSeats += groupSize;
            NrAvailableSeats -= groupSize;

            // mark 2 seats to the left and right as unavailable
            if (colIndex > 1)
            {
                MarkUnavailable(rowIndex, colIndex - 2);
            }
            if (colIndex > 0)
            {
                MarkUnavailable(rowIndex, colIndex - 1);
            }
            if (colIndex + groupSize < NrCols)
            {
                MarkUnavailable(rowIndex, colIndex + groupSize);
            }
            if (colIndex + groupSize + 1 < NrCols)
            {
                MarkUnavailable(rowIndex, colIndex + groupSize + 1);
            }

            UpdateAvailableSeats(rowIndex);

            // mark seats one row above as unavailable
            if (rowIndex > 0)
            {
                for (int x = 0; x < groupSize; x++)
                {
                    MarkUnavailable(rowIndex - 1, colIndex + x);
                }

                if (colIndex > 0)
                {
                    MarkUnavailable(rowIndex - 1, colIndex - 1);
                }
                if (colIndex + groupSize < NrCols)
                {
                    MarkUnavailable(rowIndex - 1, colIndex + groupSize);
                }

                UpdateAvailableSeats(rowIndex - 1);
            }

            // mark seats one row below as unavailable
            if (rowIndex + 1 < NrRows)
            {
                for (int x = 0; x < groupSize; x++)
                {
                    MarkUnavailable(rowIndex + 1, colIndex + x);
                }

                if (colIndex > 0)
                {
                    MarkUnavailable(rowIndex + 1, colIndex - 1);
                }
                if (colIndex + groupSize < NrCols)
                {
                    MarkUnavailable(rowIndex + 1, colIndex + groupSize);
                }

                UpdateAvailableSeats(rowIndex + 1);
            }
        }

        /// <summary>
        /// mark a seat at the given row and column index as unavailable
        /// </summary>
        /// <param name="rowIndex"></param>
        /// <param name="colIndex"></param>
        private void MarkUnavailable(int rowIndex, int colIndex)
        {
            if (Layout[rowIndex, colIndex] == Seat.Empty)
            {
                NrAvailableSeats--;
                Layout[rowIndex, colIndex] = Seat.Unavailable;
            }
        }

        /// <summary>
        /// mark one seat as unavailable at the given row and column index
        /// and update the available seat list for that row
        /// </summary>
        /// <param name="rowIndex"></param>
        /// <param name="colIndex"></param>
        public void MarkSeatAsUnused(int rowIndex, int colIndex)
        {
            MarkUnavailable(rowIndex, colIndex);
            UpdateAvailableSeats(rowIndex);
        }

        /// <summary>
        /// find the first group of adjacent available seats of size at least groupsize
        /// </summary>
        /// <param name="groupSize"></param>
        /// <returns></returns>
        public (int rowIndex, int colIndex, int seatGroupSize) FindFirstSeating(int groupSize)
        {
            // check if enough seats are remaining
            if (NrAvailableSeats < groupSize)
            {
                return (0, 0, 0);
            }
            
            // find the first place where this groups fits
            for (int y = 0; y < NrRows; y++)
            {
                (int colStartIndex, int seatGroupSize) seating = _availableSeats[y].FirstOrDefault(seats => seats.seatGroupSize >= groupSize);
                if (seating != (0, 0))
                {
                    return (y, seating.colStartIndex, seating.seatGroupSize);
                }
            }
            
            // no place is found
            return (0, 0, 0);
        }

        /// <summary>
        /// find the group of adjacent available seats of at least size groupsize
        /// which creates the least amount of new unavailable seats
        /// </summary>
        /// <param name="groupSize"></param>
        /// <returns></returns>
        public (int rowIndex, int colIndex, int seatGroupSize) FindBestSeating(int groupSize)
        {
            // check if enough seats are remaining
            if (NrAvailableSeats < groupSize)
            {
                return (0, 0, 0);
            }

            (int rowIndex, int colIndex, int seatGroupSize, int nrNewUnavailableSeats) bestSeating = (-1, -1, -1, int.MaxValue);
            
            // check every row
            for (int y = 0; y < NrRows; y++)
            {
                // check all seat groups
                for (int i = 0; i < _availableSeats[y].Count; i++)
                {
                    (int colStartIndex, int seatGroupSize) seatGroup = _availableSeats[y][i];
                    if (seatGroup.seatGroupSize >= groupSize)
                    {
                        // check all offsets
                        for (int offset = 0; offset <= seatGroup.seatGroupSize - groupSize; offset++)
                        {
                            int total = CalculateNrNewUnavailableSeats(y, seatGroup.colStartIndex + offset, groupSize);
                            if (total == 0)
                            {
                                // we can't do better than creating 0 new unavailable seats
                                return (y, seatGroup.colStartIndex + offset, seatGroup.seatGroupSize);
                            }
                            if (total < bestSeating.nrNewUnavailableSeats)
                            {
                                // better seating is found
                                bestSeating = (y, seatGroup.colStartIndex + offset, seatGroup.seatGroupSize, total);
                            }
                        }
                    }
                }
            }

            if (bestSeating.rowIndex != -1 && bestSeating.colIndex != -1)
            {
                return (bestSeating.rowIndex, bestSeating.colIndex, bestSeating.seatGroupSize);
            }

            // no place is found
            return (0, 0, 0);
        }

        /// <summary>
        /// calculate the number of new unavailable seats if a group of size groupsize
        /// were placed with the leftmost person at row and column index
        /// </summary>
        /// <param name="rowIndex"></param>
        /// <param name="colIndex"></param>
        /// <param name="groupSize"></param>
        /// <returns></returns>
        private int CalculateNrNewUnavailableSeats(int rowIndex, int colIndex, int groupSize)
        {
            int total = 0;

            // 2 seats to the left and right
            if (colIndex > 1)
            {
                if (Layout[rowIndex, colIndex - 2] == Seat.Empty)
                {
                    total++;
                }
            }
            if (colIndex > 0)
            {
                if (Layout[rowIndex, colIndex - 1] == Seat.Empty)
                {
                    total++;
                }
            }
            if (colIndex + groupSize < NrCols)
            {
                if (Layout[rowIndex, colIndex + groupSize] == Seat.Empty)
                {
                    total++;
                }
            }
            if (colIndex + groupSize + 1 < NrCols)
            {
                if (Layout[rowIndex, colIndex + groupSize + 1] == Seat.Empty)
                {
                    total++;
                }
            }

            // one row above
            if (rowIndex > 0)
            {
                for (int x = 0; x < groupSize; x++)
                {
                    if (Layout[rowIndex - 1, colIndex + x] == Seat.Empty)
                    {
                        total++;
                    }
                }
                if (colIndex > 0)
                {
                    if (Layout[rowIndex - 1, colIndex - 1] == Seat.Empty)
                    {
                        total++;
                    }
                }
                if (colIndex + groupSize < NrCols)
                {
                    if (Layout[rowIndex - 1, colIndex + groupSize] == Seat.Empty)
                    {
                        total++;
                    }
                }
            }

            // one row below
            if (rowIndex + 1 < NrRows)
            {
                for (int x = 0; x < groupSize; x++)
                {
                    if (Layout[rowIndex + 1, colIndex + x] == Seat.Empty)
                    {
                        total++;
                    }
                }
                if (colIndex > 0)
                {
                    if (Layout[rowIndex + 1, colIndex - 1] == Seat.Empty)
                    {
                        total++;
                    }
                }
                if (colIndex + groupSize < NrCols)
                {
                    if (Layout[rowIndex + 1, colIndex + groupSize] == Seat.Empty)
                    {
                        total++;
                    }
                }
            }

            return total;
        }
    }
}
