#include "ferma.h"

int main(int argc, char** argv){
    if(argc < 3){
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file>\n";
        return 1;
    }

    Ferma f;
    f.citireDinFisier(argv[1]);
    f.simulare();
    f.afisareInFisier(argv[2]);

    return 0;
}
