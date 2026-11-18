#ifndef LEGUMA_H_INCLUDED
#define LEGUMA_H_INCLUDED

#include<iostream>
#include<cstring>
#include<stdlib.h>
#pragma once

class Leguma{
private:
    char* nume;
    int timpCultivare;
    int costPlantare;
    int pretVanzare;

public:
    Leguma(const char* n = "Generic", int t = 0, int c = 0, int p = 0);
    Leguma(const Leguma& l);
    Leguma& operator=(const Leguma& l);
    ~Leguma();

    const char* getNume() const;
    int getTimpCultivare() const;
    int getCostPlantare() const;
    int getPretVanzare() const;

    void setNume(const char* n);
    void setTimpCultivare(int t);
    void setCostPlantare(int c);
    void setPretVanzare(int p);
};

#endif // LEGUMA_H_INCLUDED
