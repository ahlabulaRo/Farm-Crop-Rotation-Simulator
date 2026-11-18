#ifndef FERMA_H_INCLUDED
#define FERMA_H_INCLUDED

#include "leguma.h"
#include "patrat.h"
#define SAME 4 
#define FRIENDLY 1 
#define MAX_ZILE 1000
#define MAX_LEGUME 20

struct Actiune{
    int zi;
    char tip[10];         /// planteaza sau culege
    int linie, coloana;
    int indexLeguma;
};

class Ferma{
private:
    Leguma* legume;
    Patrat** matrice;
    int** permisiuni;

    int dimensiune;
    int numarZile;
    int bani;
    int numarLegume;
    Actiune* vectorActiuni;
    int numarActiuni;
    int dp[MAX_ZILE+1][MAX_LEGUME+1][2]; /// dynamic programming - pentru memorizare

    ///metode private
    bool poatePlanta(int linie, int coloana, int indexLeguma, int ziCurenta);
    bool esteMatura(int linie, int coloana, int ziCurenta);
    void planteaza(int linie, int coloana, int indexLeguma, int ziCurenta);
    void recolteaza(int linie, int coloana, int ziCurenta);
    int dfsPatrat(int linie, int coloana, int ziCurenta, int ultimaLeguma, bool liber);
    int calculeazaProfitMaxim();
public:
    Ferma();
    ~Ferma();

    Leguma* getVectorLegume() const;
    Patrat** getMatrice() const;
    int** getPermisiuni() const;
    int getDimensiune() const;
    int getNumarZile() const;
    int getBani() const;
    int getnumarLegume() const;
    Actiune* getVectorActiuni() const;
    int getNumarActiuni() const;

    void citireDinFisier(const char* numeFisier);
    void afisareInFisier(const char* numeFisier);
    void simulare();
};

#endif // FERMA_H_INCLUDED
