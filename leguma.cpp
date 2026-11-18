#include "leguma.h"

Leguma::Leguma(const char* n, int t, int c, int p){
    this->nume = new char[strlen(n) + 1];
    strcpy(nume, n);
    this->timpCultivare = t;
    this->costPlantare = c;
    this->pretVanzare = p;
}

Leguma::Leguma(const Leguma& l){
    this->timpCultivare = l.timpCultivare;
    this->costPlantare = l.costPlantare;
    this->pretVanzare = l.pretVanzare;
    if(l.nume != nullptr){
        this->nume = new char[strlen(l.nume) + 1];
        strcpy(this->nume, l.nume);
    }
    else this->nume = nullptr;
}

Leguma& Leguma::operator=(const Leguma& l){
    if(this == &l) return* this;
    if(this->nume != nullptr) delete[] this->nume;
    this->timpCultivare = l.timpCultivare;
    this->costPlantare = l.costPlantare;
    this->pretVanzare = l.pretVanzare;
    if(l.nume != nullptr){
        this->nume = new char[strlen(l.nume) + 1];
        strcpy(this->nume, l.nume);
    }
    else this->nume = nullptr;

    return *this;
}

Leguma::~Leguma(){
    if(this->nume != nullptr) delete[] this->nume;
}

const char* Leguma::getNume() const{
    return this->nume;
}

int Leguma::getTimpCultivare() const{
    return this->timpCultivare;
}

int Leguma::getCostPlantare() const{
    return this->costPlantare;
}

int Leguma::getPretVanzare() const{
    return this->pretVanzare;
}

void Leguma::setNume(const char* n){
    if(this->nume != nullptr) delete[] this->nume;
    if(n != nullptr){
        this->nume = new char[strlen(n) + 1];
        strcpy(this->nume, n);
    }
    else this->nume = nullptr;
}

void Leguma::setTimpCultivare(int t){
    this->timpCultivare = t;
}

void Leguma::setCostPlantare(int c){
    this->costPlantare = c;
}

void Leguma::setPretVanzare(int p){
    this->pretVanzare = p;
}
