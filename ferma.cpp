#include "ferma.h"

Ferma::Ferma(){
    this->dimensiune = 0;
    this->numarZile = 0;
    this->bani = 0;
    this->numarLegume = 0;
    this->legume = nullptr;
    this->matrice = nullptr;
    this->permisiuni = nullptr;
    this->vectorActiuni = nullptr;
    this->numarActiuni = 0;
}

Ferma::~Ferma(){
    if(legume != nullptr) delete[] legume;

    if(matrice != nullptr){
        for(int i=0;i<dimensiune;i++) delete[] matrice[i];
        delete[] matrice;
    }

    if(this->permisiuni != nullptr){
        for(int i=0;i<numarLegume;i++) delete[] permisiuni[i];
        delete[] permisiuni;
    }

    if(this->vectorActiuni != nullptr) delete[] vectorActiuni;
}

void Ferma::citireDinFisier(const char* numeFisier){
    FILE* f = fopen(numeFisier, "r");
    if(!f){
        std::cerr << "Nu s-a putut deschide fisierul de citire!" << std::endl;
        exit(1);
    }
    ///Citire date initiale ferma
    int dubluraDimensiune;
    fscanf(f, "%d %d %d %d %d", &dimensiune, &dubluraDimensiune, &numarZile, &bani, &numarLegume);
    if(dimensiune > 99 || numarZile > 1000 || numarLegume > 20){
        std::cerr << "Date invalid in fisier!" << std::endl;
        fclose(f);
        exit(1);
    }

    ///Citire vector legume
    legume = new Leguma[numarLegume];
    char nume[31];
    int timp,cost,pret;
    for(int i=0;i<numarLegume;i++){
        fscanf(f, "%s %d %d %d", nume, &timp, &cost, &pret);
        legume[i] = Leguma(nume, timp, cost, pret);
    }

    ///Skip la cuvantul "Rotatie" + citire numar rotatii
    char bufferRotatii[20];
    int numarRotatii;
    fscanf(f, "%s %d", bufferRotatii, &numarRotatii);

    ///Alocare vector de permisiuni si initializare cu 0
    permisiuni = new int*[numarLegume];
    for(int i=0;i<numarLegume;i++){
        permisiuni[i] = new int[numarLegume];
        for(int j=0;j<numarLegume;j++)
            permisiuni[i][j] = 0;
    }
    ///Matrice de adiacenta = permisiuni + citirea permisiunilor
    char leguma1[31], leguma2[31];
    for(int i=0;i<numarRotatii;i++){
        fscanf(f, "%s %s", leguma1, leguma2);

        int idx1 = -1, idx2 = -1;
        for(int j=0;j<numarLegume;j++){
            if(strcmp(legume[j].getNume(), leguma1) == 0) idx1 = j;
            if(strcmp(legume[j].getNume(), leguma2) == 0) idx2 = j;
        }

        if(idx1 == -1 || (idx2 == -1 && strcmp(leguma2, "N/A") != 0) ){
            std::cerr << "Eroare: Leguma necunoscuta in Rotatie!" << std::endl;
            fclose(f);
            exit(1);
        }

        if(strcmp(leguma2, "N/A") == 0){
            for(int j=0;j<numarLegume;j++) permisiuni[idx1][j] = 1;
        }
        else permisiuni[idx1][idx2] = 1;
    }

    ///Alocare matrice de patrate
    matrice = new Patrat*[dimensiune];
    for(int i=0;i<dimensiune;i++) matrice[i] = new Patrat[dimensiune];

    ///Alocare Actiuni
    int dimensiuneaMaxima = 2 * dimensiune * dimensiune * numarZile;
    vectorActiuni = new Actiune[dimensiuneaMaxima];
    this->numarActiuni = 0;
    fclose(f);
}

Leguma* Ferma::getVectorLegume() const{
    return this->legume;
}

Patrat** Ferma::getMatrice() const{
    return this->matrice;
}

int** Ferma::getPermisiuni() const{
    return this->permisiuni;
}

int Ferma::getDimensiune() const{
    return this->dimensiune;
}

int Ferma::getNumarZile() const{
    return this->numarZile;
}

int Ferma::getBani() const{
    return this->bani;
}

int Ferma::getnumarLegume() const{
    return this->numarLegume;
}

Actiune* Ferma::getVectorActiuni() const{
    return this->vectorActiuni;
}

int Ferma::getNumarActiuni() const{
    return this->numarActiuni;
}


///metode private implementari

bool Ferma::poatePlanta(int linie, int coloana, int indexLeguma, int ziCurenta){
    Patrat &p = matrice[linie][coloana];

    /// daca patratul nu e liber nu plantam
    if(!p.ePatratulLiber())
        return false;

    int ultima = p.getUltimaLegumaPlantata();

    /// daca e prima plantare pe acest patrat, plantam o leguma N/A
    if(ultima == -1){
        /// ca sa aiba N/A trebuie sa aiba toate permisiunile 1
        bool areNA = true;
        for (int i=0;i<numarLegume;i++){
            if (permisiuni[indexLeguma][i] == 0){
                areNA = false;
                break;
            }
        }
        return areNA;
    }

    /// daca e aceiasi leguma ca precedenta
    if(ultima == indexLeguma){
        /// verificam daca exista auto-rotatie
        if (permisiuni[indexLeguma][ultima] == 0)
            return false;

        // dacă rotația permite, verificăm și pauza SAME (4 zile după culegere)
        return (ziCurenta - p.getZiCulegere() >= SAME);
    }

    /// leguma diferita -> trebuie sa treaca cel putin o zi de la culegere
    if(permisiuni[indexLeguma][ultima] == 1){
        return (ziCurenta - p.getZiCulegere() >= FRIENDLY);
    }

    ///daca nu respecta nimic de mai sus, nu se planteaza
    return false;
}


bool Ferma::esteMatura(int linie, int coloana, int ziCurenta){
    Patrat& p = matrice[linie][coloana];

    /// daca patratul e gol atunci automat nu exista o planta matura
    if(p.ePatratulLiber()) return false;

    int indexLeguma = p.getLegumaCurenta();
    int ziPlantare = p.getZiPlantare();
    int timpCultivare = legume[indexLeguma].getTimpCultivare();

    return ziCurenta - ziPlantare >= timpCultivare;
}

void Ferma::planteaza(int linie, int coloana, int indexLeguma, int ziCurenta){
    if(!poatePlanta(linie, coloana, indexLeguma, ziCurenta)) return;

    /// plantam in patratul respectiv
    matrice[linie][coloana].planteaza(indexLeguma, ziCurenta);

    /// scadem costul de plantare din suma totala
    bani -= legume[indexLeguma].getCostPlantare();

    /// ne ocupam de actiuni pentru afisare
    vectorActiuni[numarActiuni].zi = ziCurenta;
    strcpy(vectorActiuni[numarActiuni].tip, "planteaza");
    vectorActiuni[numarActiuni].linie = linie;
    vectorActiuni[numarActiuni].coloana = coloana;
    vectorActiuni[numarActiuni].indexLeguma = indexLeguma;
    numarActiuni++;
}

void Ferma::recolteaza(int linie, int coloana, int ziCurenta){
    Patrat &p = matrice[linie][coloana];
    int indexLeguma = p.getLegumaCurenta();

    /// daca patratul nu e liber sau leguma nu este matura nu recoltam
    if(p.ePatratulLiber() || !esteMatura(linie, coloana, ziCurenta)) return;

    /// adaugam pretul de vanzare la suma totala
    bani += legume[indexLeguma].getPretVanzare();

    p.culege(ziCurenta);

    /// ne ocupam de actiuni pentru afisare
    vectorActiuni[numarActiuni].zi = ziCurenta;
    strcpy(vectorActiuni[numarActiuni].tip, "culege");
    vectorActiuni[numarActiuni].linie = linie;
    vectorActiuni[numarActiuni].coloana = coloana;
    vectorActiuni[numarActiuni].indexLeguma = indexLeguma;
    numarActiuni++;
}

int Ferma::dfsPatrat(int linie, int coloana, int ziCurenta, int ultimaLeguma, bool liber){
    if(ziCurenta > numarZile)
        return 0;

    int ult = ultimaLeguma + 1;
    int lib = liber ? 1 : 0;

    if(dp[ziCurenta][ult][lib] != -1)
        return dp[ziCurenta][ult][lib];

    int maxProfit = 0;

    /// nu plantam nimic si mergem la ziua urmatoare
    maxProfit = dfsPatrat(linie, coloana, ziCurenta + 1, ultimaLeguma, true);

    /// incercam sa plantam in ziua curenta si verificam pentr toate legumele
    for(int i=0;i<numarLegume;i++){
        if(poatePlanta(linie, coloana, i, ziCurenta)){
            int timpCultivare = legume[i].getTimpCultivare();
            int ziRecoltare = ziCurenta + timpCultivare;

            /// putem recolta inainte de final
            if(ziRecoltare <= numarZile){
                int cost = legume[i].getCostPlantare();
                int profit = legume[i].getPretVanzare() - cost;

                /// profitul viitor de după recoltare
                int profitTotal = profit + dfsPatrat(linie, coloana, ziRecoltare, i, false);

                if(profitTotal > maxProfit) maxProfit = profitTotal;
            }
        }
    }

    dp[ziCurenta][ult][lib] = maxProfit;
    return maxProfit;
}

/* ///de test
int Ferma::calculeazaProfitMaxim(){
    int totalProfit = 0;

    ///resetam tridimensionaultl pentru fiecare patrat in parte
    for(int zi=0;zi<=numarZile;zi++)
        for(int ult=0; ult <= numarLegume;ult++)
            for(int lib=0;lib<=1;lib++)
                dp[zi][ult][lib] = -1;

    for(int i=0;i<dimensiune;i++){
        for(int j=0;j<dimensiune;j++){
            totalProfit += dfsPatrat(i, j, 1, -1, true);
        }
    }

    return totalProfit;
}
*/

void Ferma::simulare(){
    /// resetarea dp -ului la -1 pt dfs
    for(int zi=0;zi<=numarZile;zi++)
        for(int ult=0;ult<=numarLegume;ult++)
            for(int lib=0;lib<=1;lib++)
                dp[zi][ult][lib] = -1;

    for(int zi=1;zi<=numarZile;zi++){
        /// culegem legumele mature
        for(int i=0;i<dimensiune;i++){
            for(int j=0;j<dimensiune;j++){
                if(esteMatura(i, j, zi)){
                    recolteaza(i, j, zi);
                }
            }
        }

        /// plantam pe sloturile libere din patrat aplicand dfs
        for(int i=0;i<dimensiune;i++){
            for(int j=0;j<dimensiune;j++){
                if(!matrice[i][j].ePatratulLiber())
                    continue;

                int legumaOptima = -1;
                int scorMax = -1000000000;

                for(int k=0;k<numarLegume;k++) {
                    int cost = legume[k].getCostPlantare();
                    int timp = legume[k].getTimpCultivare();
                    int pret = legume[k].getPretVanzare();

                    /// trebuie sa putem planta, sa avem destui bani sa cumparam leguma si sa fie matura
                    if(!poatePlanta(i, j, k, zi))
                        continue;
                    if(bani < cost)
                        continue;
                    if(zi + timp > numarZile)
                        continue;

                    int profitNet = pret - cost;

                    /// profit estimat de dfs
                    int profitViitor = dfsPatrat(i, j, zi + timp, k, false);

                    int scorTotal = profitNet + profitViitor;

                    if(scorTotal > scorMax){
                        scorMax = scorTotal;
                        legumaOptima = k;
                    }
                }

                if(legumaOptima != -1){
                    planteaza(i, j, legumaOptima, zi);
                }
            }
        }
    }
}

void Ferma::afisareInFisier(const char* numeFisier){
    FILE* f = fopen(numeFisier, "w");
    if(!f) exit(1);

    for(int i=0;i<numarActiuni;i++){
        int z = vectorActiuni[i].zi;
        int l = vectorActiuni[i].linie;
        int c = vectorActiuni[i].coloana;
        const char* tip = vectorActiuni[i].tip;

        if(strcmp(tip, "planteaza") == 0){
            fprintf(f, "%d %s %02dx%02d %s\n", z, tip, l, c, legume[vectorActiuni[i].indexLeguma].getNume());
        }
        else{
            fprintf(f, "%d %s %02dx%02d\n",z, tip, l, c);
        }
    }

    fprintf(f, "SUMA_FINALA: %d\n", bani);
    fclose(f);
}

