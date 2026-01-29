using System.IO;

string filePath = "matrix.txt";

//načte po řádcích do pole 3x3 prvních 9 hodnot z pole lines (-> matice levých stran)
static int[,] GetLeftSide(int[,] matrix, string[] lines)
{
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            matrix[i, j] = int.Parse(lines[j + i * 3]);
        }
    }
    return matrix;
}

//načte do pole 1x3 poslední 3 hodnoty z pole lines (-> sloupcový vektor pravých stran)
static int[] GetRightSide(int[] vector, string[] lines)
{
    for (int i = 0; i < 3; i++)
    {
        vector[i] = int.Parse(lines[i + 9]);
    }
    return vector;
}

//předané matici 3x3 vypočtete derminant Sarussovým pravidlem
static int SarrusRule(int[,] matrix)
{
    int Plus1 = matrix[0, 0] * matrix[1, 1] * matrix[2, 2];
    int Plus2 = matrix[1, 0] * matrix[2, 1] * matrix[0, 2];
    int Plus3 = matrix[2, 0] * matrix[0, 1] * matrix[1, 2];
    int Plus = Plus1 + Plus2 + Plus3;

    int Minus1 = matrix[0, 2] * matrix[1, 1] * matrix[2, 0];
    int Minus2 = matrix[1, 2] * matrix[2, 1] * matrix[0, 0];
    int Minus3 = matrix[2, 2] * matrix[0, 1] * matrix[1, 0];
    int Minus = -Minus1 - Minus2 - Minus3;

    return (Plus + Minus);
}

//vytvoří kopii předané matice 3x3, nahradí sloupec na daném indexu hodnotamy z předaného pole 1x3
static int[,] CrammerMatrix(int[,] matrix, int[] vector, int columnIndex)
{
    int[,] matrixCopy = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            matrixCopy[i, j] = matrix[i, j];
        }
    }

    for (int i = 0; i < 3; i++)
    {
        matrixCopy[i, columnIndex] = vector[i];
    }
    return matrixCopy;
}

string[] lines = File.ReadAllLines(filePath);

int[,] leftSide = { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
int[] rightSide = { 0, 0, 0 };

//matice levých stran a sloupcový vektor pravých stran
leftSide = GetLeftSide(leftSide, lines);
rightSide = GetRightSide(rightSide, lines);

//determinanty
int DetA = SarrusRule(leftSide);
int DetX = SarrusRule(CrammerMatrix(leftSide, rightSide, 0));
int DetY = SarrusRule(CrammerMatrix(leftSide, rightSide, 1));
int DetZ = SarrusRule(CrammerMatrix(leftSide, rightSide, 2));

//výsledky
int x = DetX / DetA;
int y = DetY / DetA;
int z = DetZ / DetA;

Console.WriteLine("x = " + x + ", y = " + y + ", z = " + z);
