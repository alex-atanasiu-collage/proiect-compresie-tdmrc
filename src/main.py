import soundpredictors
import textpredictors

if __name__ == "__main__":
    # TODO write main code for module
    print("Proiect TDMRC - Compresie bazata pe predictori")
    print("``````````````````````````````````````````````")
    print(" * Atanasiu Alexandru-Marian")
    print(" * Baloi Bogdan-Cristian")
    print(" * Damian Petrisor Alin")
    print(" * Panaitescu Cristian")

    modules = [soundpredictors, textpredictors]

    # TODO run test from each module
    for module in modules:
        module.test()
