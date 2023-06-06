import os
import sys
import shutil
import json
import numpy as np

# constants
ANG2BOHR = 1.8897259886

ELEMENTS = [
    "Bq",
    "H ",                                                                                                                                                                                     "He",
    "Li", "Be",                                                                                                                                                 "B ", "C ", "N ", "O ", "F ", "Ne",
    "Na", "Mg",                                                                                                                                                 "Al", "Si", "P ", "S ", "Cl", "Ar",
    "K ", "Ca", "Sc", "Ti", "V ", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",                                                                                     "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y ", "Zr", "Nb", "Mo", "Te", "Ru", "Rh", "Pd", "Ag", "Cd",                                                                                     "In", "Sn", "Sb", "Te", "I ", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W ", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U ", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
]


# load configure
with open("gauick.json") as f:
    settings = json.load(f)


# create temp dir
if os.path.exists("tmp"):
    shutil.rmtree("tmp")

os.mkdir("tmp")
os.chdir("tmp")

# prepare input file
quick_inp = f"{settings['job']} DIPOLE"

(layer, InputFile, OutputFile, MsgFile, FChkFile, MatElFile) = sys.argv[1:]

atoms = []
coords = []
with open(InputFile, "r") as fi:
    (atoms, derivs, charge, spin) = [int(x) for x in fi.readline().split()]

    quick_inp += f" CHARGE={charge} MULT={spin}"

    if derivs == 1:
        quick_inp += " GRADIENT"

    quick_inp += "\n\n"

    for i in range(0, atoms):
        arr = fi.readline().split()
        atom = ELEMENTS[int(arr[0])]
        coord = [f"{(float(x) / ANG2BOHR)}" for x in arr[1:4]]
        quick_inp += f" {atom}"
        quick_inp += " " * 4
        quick_inp += (" " * 4).join(coord)
        quick_inp += "\n"


with open("mol.in", "w") as f:
    f.write(quick_inp)

print(">>> Starting QUICK Calculation...")
os.system(f"{settings['exec']} mol.in")
print(">>> QUICK Calculation Done!")
print(">>> Extracting QUICK output...")

with open("mol.out") as f:
    line = f.readline()

    while line:
        if line.startswith(" TOTAL ATOM NUMBER"):
            num_atoms = int(line.split()[4])
            grad = np.zeros((num_atoms * 3))

        if line.startswith(" TOTAL ENERGY"):
            energy = float(line.split()[-1])

        if line.startswith(" @ Begin Gradient Calculation"):
            for i in range(5):
                line = f.readline()

            for i in range(num_atoms * 3):
                line = f.readline()
                grad[i] = float(line.split()[-1])

        if line.startswith("    DIPOLE (DEBYE)"):
            line = f.readline()
            dipole = [float(x) for x in f.readline().split()]

        line = f.readline()

with open(OutputFile, "w") as f:
    f.writelines(f"{energy:20.12E}{dipole[0]:20.12E}{dipole[1]:20.12E}{dipole[2]:20.12E}\n")
    
    if derivs == 1:
        grad = np.reshape(grad, (num_atoms, 3))
        np.savetxt(f, grad, fmt="%20.12E", delimiter="")

print(">>> Done!")