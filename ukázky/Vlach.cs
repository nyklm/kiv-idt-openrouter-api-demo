using System.IO;
using System.Numerics;
using System.Runtime.InteropServices;
int Sarrus(int[,] matrix)
{
    int vypocet = (matrix[0, 0] * matrix[1, 1] * matrix[2, 2]) + (matrix[0, 1] * matrix[1, 2] * matrix[2, 0]) + (matrix[0, 2] * matrix[1, 0] * matrix[2, 1])
                  - (matrix[2, 0] * matrix[1, 1] * matrix[0, 2]) - (matrix[2, 1] * matrix[1, 2] * matrix[0, 0]) - (matrix[2, 2] * matrix[1, 0] * matrix[0, 1]);
    return (vypocet);
}
int[] Cramer(int[,] matrix)
{
    int[] res = new int[3]; 
    for (int e = 0; e < 3; e++){
        int[,] detxi = new int[3, 3];
        int s = 0;
        int r = 0;
        for (int i = 0; i <= 8; i++)
        {
            if (i < 9)
            {
                s = (i % 3);
                r = (i) / 3;

            }
            else
            {
                s = 3;
                r = i % 9;
            }
            detxi[s, r] = matrix[s,r];
        }
        detxi[e, 0] = matrix[3,0];
        detxi[e, 1] = matrix[3,1];
        detxi[e, 2] = matrix[3,2];
        res[e] = Sarrus(detxi);
    }
    return (res);
}
string[] data = new string[12];
string path = "C:\\Users\\vojta\\OneDrive\\Plocha\\škola\\ZCU\\idt\\du1\\matrix.txt";
data = File.ReadAllLines(path);
int[,] matrix = new int[4, 3];
int[] resdetxi = new int[3];
double vysledek;
int s = 0;
int r = 0;
for(int i = 0;i < data.Length; i++)
{
    if(i < 9)
    {
        s = (i % 3);
        r = (i) / 3;

    }
    else
    {
        s = 3;
        r = i % 9;
    }
    matrix[s, r] = int.Parse(data[i]);
}
resdetxi = Cramer(matrix);
int resdet = Sarrus(matrix);
if(resdet == 0)
{
    Console.WriteLine("Soustava nemá řešení nebo jich má nekonečně mnoho");

}
else
{
    Console.WriteLine("Soustava má jediné řešené");
    for (int i = 0; i < 3; i++)
    {
        vysledek = resdetxi[i] / resdet;
        Console.WriteLine("vysledek pro " + i + "rovnici je: " + vysledek);
    }
}
    
