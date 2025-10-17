from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.MMCIFParser import MMCIFParser


def print_chains(structure_file: str):
    if structure_file.endswith(".cif"):
        parser = MMCIFParser(QUIET=True)
    elif structure_file.endswith(".pdb"):
        parser = PDBParser(QUIET=True)
    else:
        raise ValueError("Unsupported file format. Please provide a .pdb or .cif file.")
    structure = parser.get_structure("structure", structure_file)
    model = structure[0]
    chains = [chain.id for chain in model]
    print("Chains:", chains)
