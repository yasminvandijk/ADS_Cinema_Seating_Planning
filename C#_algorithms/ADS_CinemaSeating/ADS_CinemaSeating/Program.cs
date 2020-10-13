using ADS_CinemaSeating.Algorithms;
using ADS_CinemaSeating.CinemaLayout;
using System;
using System.Diagnostics;
using System.IO;

namespace ADS_CinemaSeating
{
    class Program
    {
        static string online_cases_folderpath = "../../../Test_Cases/Online/";
        static string online_results_folderpath = "../../../Test_Results/Online/";
        static string[] online_filenames = new string[]
            {
                "Online01.txt",
                "Online02.txt",
                "Online03.txt",
                "Online04.txt",
                "Online05.txt",
                "Online06.txt",
                "Online07.txt",
                "Online08.txt",
                "Online09.txt",
                "Online10.txt",
                "Online11.txt",
                "Online12.txt",
                "Online13.txt",
                "Online14.txt",
                "Online15.txt",
                "Online16.txt",
                "Online17.txt",
                "Online18.txt"
            };

        static string offline_cases_folderpath = "../../../Test_Cases/Offline/";
        static string offline_results_folderpath = "../../../Test_Results/Offline/";
        static string[] offline_filenames = new string[] {
            "Exact01.txt",
            "Exact02.txt",
            "Exact03.txt",
            "Exact04.txt",
            "Exact05.txt",
            "Exact06.txt",
            "Exact07.txt",
            "Exact08.txt",
            "Exact09.txt",
            "Exact10.txt",
            "Exact11.txt",
            "Exact12.txt",
            "Exact13.txt",
            "Exact14.txt",
            "Exact15.txt",
            "Exact16.txt",
            "Exact17.txt",
            "Exact18.txt",
            "Exact19.txt",
            "Exact20.txt",
            "Exact21.txt"
        };

        static void Main(string[] args)
        {
            long timeout_ms = 30 * 60 * 1000;

            Run_Online_FirstFit(timeout_ms);
            Run_Online_BestFit(timeout_ms);

            Run_Offline_FirstFit_SmallFirst(timeout_ms);
            Run_Offline_FirstFit_BigFirst(timeout_ms);
            Run_Offline_BestFit_SmallFirst(timeout_ms);
            Run_Offline_BestFit_BigFirst(timeout_ms);

            Run_Offline_Branch_And_Bound(timeout_ms);
        }

        private static void Run_Online_FirstFit(long timeout_ms)
        {
            Console.WriteLine("online first fit");
            StreamWriter streamWriter = new StreamWriter(online_results_folderpath + "online_first_fit.csv");
            streamWriter.WriteLine("testcase, nr occupied seats, runtime (ms)");

            foreach (string filename in online_filenames)
            {
                TestResult result = Online_FirstFit.Solve(online_cases_folderpath + filename, timeout_ms);
                Console.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
                streamWriter.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
            }

            Console.WriteLine();
            streamWriter.Close();
        }

        private static void Run_Online_BestFit(long timeout_ms)
        {
            Console.WriteLine("online best fit");
            StreamWriter streamWriter = new StreamWriter(online_results_folderpath + "online_best_fit.csv");
            streamWriter.WriteLine("testcase, nr occupied seats, runtime (ms)");

            foreach (string filename in online_filenames)
            {
                TestResult result = Online_BestFit.Solve(online_cases_folderpath + filename, timeout_ms);
                Console.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
                streamWriter.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
            }

            Console.WriteLine();
            streamWriter.Close();
        }

        private static void Run_Offline_FirstFit_SmallFirst(long timeout_ms)
        {
            Console.WriteLine("exact first fit small first");
            StreamWriter streamWriter = new StreamWriter(offline_results_folderpath + "offline_first_fit_small_first.csv");
            streamWriter.WriteLine("testcase, nr occupied seats, runtime (ms)");

            foreach (string filename in offline_filenames)
            {
                TestResult result = Offline_FirstFit_SmallFirst.Solve(offline_cases_folderpath + filename, timeout_ms);
                Console.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
                streamWriter.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
            }

            Console.WriteLine();
            streamWriter.Close();
        }

        private static void Run_Offline_FirstFit_BigFirst(long timeout_ms)
        {
            Console.WriteLine("exact first fit big first");
            StreamWriter streamWriter = new StreamWriter(offline_results_folderpath + "offline_first_fit_big_first.csv");
            streamWriter.WriteLine("testcase, nr occupied seats, runtime (ms)");

            foreach (string filename in offline_filenames)
            {
                TestResult result = Offline_FirstFit_BigFirst.Solve(offline_cases_folderpath + filename, timeout_ms);
                Console.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
                streamWriter.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
            }

            Console.WriteLine();
            streamWriter.Close();
        }

        private static void Run_Offline_BestFit_SmallFirst(long timeout_ms)
        {
            Console.WriteLine("exact best fit small first");
            StreamWriter streamWriter = new StreamWriter(offline_results_folderpath + "offline_best_fit_small_first.csv");
            streamWriter.WriteLine("testcase, nr occupied seats, runtime (ms)");

            foreach (string filename in offline_filenames)
            {
                TestResult result = Offline_BestFit_SmallFirst.Solve(offline_cases_folderpath + filename, timeout_ms);
                Console.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
                streamWriter.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
            }

            Console.WriteLine();
            streamWriter.Close();
        }

        private static void Run_Offline_BestFit_BigFirst(long timeout_ms)
        {
            Console.WriteLine("exact best fit big first");
            StreamWriter streamWriter = new StreamWriter(offline_results_folderpath + "offline_best_fit_big_first.csv");
            streamWriter.WriteLine("testcase, nr occupied seats, runtime (ms)");

            foreach (string filename in offline_filenames)
            {
                TestResult result = Offline_BestFit_BigFirst.Solve(offline_cases_folderpath + filename, timeout_ms);
                Console.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
                streamWriter.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
            }

            Console.WriteLine();
            streamWriter.Close();
        }

        private static void Run_Offline_Branch_And_Bound(long timeout_ms)
        {
            Console.WriteLine("exact branch and bound");
            StreamWriter streamWriter = new StreamWriter(offline_results_folderpath + "offline_branch_and_bound.csv");
            streamWriter.WriteLine("testcase, nr occupied seats, runtime (ms)");

            foreach (string filename in offline_filenames)
            {
                TestResult result = Offline_Branch_And_Bound.Solve(offline_cases_folderpath + filename, timeout_ms);
                Console.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");
                streamWriter.WriteLine($"{filename}, {result.Cinema.NrOccupiedSeats}, {result.RunTime_ms}");

                result.Cinema.PrintCinema();
            }

            Console.WriteLine();
            streamWriter.Close();
        }
    }
}
