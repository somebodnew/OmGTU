using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApplication12
{
    class Program
    {
        static private int[,] Garr(int N){
            int[,] array = new int[N, N];
            for(int i = 0; i < N;i++)
            {
                for(int j = 0; j < N;j++) array[i,j] = Convert.ToInt32(Console.ReadLine());
            }
            return array;
        }
        static private int[] MaxA(int[,] A, int N)
        {
            int[] Marr = new int[N];
            for (int i = 0; i < N; i++)
            {
                int M = Int32.MinValue;
                for (int j = 0; j < N; j++) if(A[i,j]>M) M = A[i,j];
                Marr[i] = M;
            }
            
            return Marr;
        }
        static private int[] MinA(int[,] A, int N)
        {
            int[] Marr = new int[N];
            for (int i = 0; i < N; i++)
            {
                int M = Int32.MaxValue;
                for (int j = 0; j < N; j++) if (A[i, j] < M) M = A[i, j];
                Marr[i] = M;
            }

            return Marr;
        }
        static void Main(string[] args)
        {
            int N = Convert.ToInt32(Console.ReadLine()),count = 0;
            int[,] array = Garr(N);
            for (int i = 0; i < N; i++)
            {

                for (int j = 0; j < N; j++) Console.Write(array[i, j] + " ");
                Console.WriteLine();
            }
            Console.WriteLine();
            int[] MinArr = MinA(array, N), MaxArr = MaxA(array, N);
            for (int i = 0; i < N; i++)
            {
                if (MinArr[i] % 2 == 0 && MaxArr[i] % 2 == 0) count++;
            }
            Console.WriteLine(count);

        }
    }
}
