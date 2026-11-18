#include "patrat.h"

Patrat::Patrat(int l, int u, int ziP, int ziC, bool liber)
{
    legumaCurenta = -1;
    ultimaLegumaPlantata = -1;
    ziPlantare = 0;
    ziCulegere = -1000000;
    eLiber = true;
}


Patrat::Patrat(const Patrat& p){
    this->legumaCurenta = p.legumaCurenta;
    this->ultimaLegumaPlantata = p.ultimaLegumaPlantata;
    this->ziPlantare = p.ziPlantare;
    this->ziCulegere = p.ziCulegere;
    this->eLiber = p.eLiber;
}

Patrat& Patrat::operator=(const Patrat& p){
    if(this == &p) return *this;
    this->legumaCurenta = p.legumaCurenta;
    this->ultimaLegumaPlantata = p.ultimaLegumaPlantata;
    this->ziPlantare = p.ziPlantare;
    this->ziCulegere = p.ziCulegere;
    this->eLiber = p.eLiber;
    return *this;
}

Patrat::~Patrat(){}

int Patrat::getLegumaCurenta() const{
    return this->legumaCurenta;
}

int Patrat::getUltimaLegumaPlantata() const{
    return this->ultimaLegumaPlantata;
}

int Patrat::getZiPlantare() const{
    return this->ziPlantare;
}

int Patrat::getZiCulegere() const{
    return this->ziCulegere;
}

bool Patrat::ePatratulLiber() const{
    return this->eLiber;
}

void Patrat::planteaza(int indexLeguma, int ziCurenta){
    this->legumaCurenta = indexLeguma;
    this->ziPlantare = ziCurenta;
    this->eLiber = false;
}

void Patrat::culege(int ziCurenta){
    this->ultimaLegumaPlantata = this->legumaCurenta;
    this->legumaCurenta = -1;
    this->eLiber = true;
    this->ziCulegere = ziCurenta;
}
