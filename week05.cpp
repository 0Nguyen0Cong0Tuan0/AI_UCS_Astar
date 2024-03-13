#include <iostream>
#include <cstdlib>
#include <cstring>
using namespace std;


static int headSize = sizeof(int) + sizeof(int) + sizeof(int);

struct PhanSo {
    double tu;
    double mau;
};

istream& operator>> (istream& fin, PhanSo& a)
{
    fin >> a.tu >> a.mau;
    return fin;
}

ostream& operator<< (ostream& fout, PhanSo& a)
{
    fout << a.tu << "/" <<  a.mau;
    return fout;
}

struct aStruct {
    int row;
    int col;
    int sizeData;
    void* Data[1];
};

int nRow(void** aData)
{
    aStruct* as = (aStruct*)((char*)aData - headSize);
    if (as != nullptr)
        return as->row;
    return 0;
}

int nCol(void** aData)
{
    aStruct* as = (aStruct*)((char*)aData - headSize);
    if (as != nullptr)
        return as->col;
    return 0;
}

void arr2D_Input(PhanSo** a) 
{
    int row = nRow((void**)a);
    int col = nCol((void**)a);

    cout << "Enter " << row * col << " elements for the array:" << endl;
    for (int i = 0; i < row; i++) 
    {
        for (int j = 0; j < col; j++) 
            cin >> a[i][j];
    }
}

void arr2D_Output(PhanSo** a) 
{
    int row = nRow((void**)a);
    int col = nCol((void**)a);

    cout << "2D Array:" << endl;
    for (int i = 0; i < row; i++) 
    {
        for (int j = 0; j < col; j++)
            cout << a[i][j] << " ";
        cout << endl;
    }
}

void free2D(void** aData)
{
    if(aData != nullptr)
    {
        void* p = (char*)aData - headSize;
        free(p);
    }
}

void alloc2D(void*** a, int row, int col, int sizeData) {
    if (row <= 0 || col <= 0 || sizeData <= 0)
        return;

    int sizeofRow = col * sizeData;
    int sz1 = row * sizeof(void*);
    int sz2 = row * sizeofRow;

    void* buf = calloc(headSize + sz1 + sz2, 1);
    if (buf == nullptr)
        return;

    aStruct* as = (aStruct*)buf;
    as->row = row;
    as->col = col;
    as->sizeData = sizeData;

    buf = (char*)buf + headSize + sz1;
    as->Data[0] = (char*)(buf);

    for (int i = 1; i < row; i++) {
        buf = (char*)buf + sizeofRow;
        memcpy(&as->Data[i], &buf, sizeof(int*));
    }

    *a = (void**)(as->Data);
}

int main() 
{
    int m, n;
    PhanSo** a;
    cout << "Input rows and cols: ";
    cin >> m >> n;
    alloc2D((void***)&a, m, n, sizeof(PhanSo));
    arr2D_Input(a);
    arr2D_Output(a);
    free2D((void**)a);

    return 0;
}
