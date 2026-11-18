#ifndef PATRAT_H_INCLUDED
#define PATRAT_H_INCLUDED

#include<iostream>
#include<cstring>
#include<stdlib.h>
#pragma once

class Patrat{
private:
    int legumaCurenta;        // indexul legumei curente
    int ultimaLegumaPlantata; // indexul legumei anterioare
    int ziPlantare;           // ziua in care se planteaza leguma curenta
    int ziCulegere;           // ziua in care a fost culeasa leguma anterioara
    bool eLiber;              // true - nu exista leguma plantata, false - exista
public:
    Patrat(int l = 0,int u = 0, int ziP = 0, int ziC = 0, bool liber = true);
    Patrat(const Patrat& p);
    Patrat& operator=(const Patrat& p);
    ~Patrat();

    int getLegumaCurenta() const;
    int getUltimaLegumaPlantata() const;
    int getZiPlantare() const;
    int getZiCulegere() const;
    bool ePatratulLiber() const;

    void planteaza(int indexLeguma, int ziCurenta);
    void culege(int ziCurenta);
};

#endif // PATRAT_H_INCLUDED
