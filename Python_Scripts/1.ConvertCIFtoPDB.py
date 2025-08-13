from Bio.PDB import MMCIFParser, PDBIO
import os
import glob

def convert_cif_to_pdb(cif_file):
    parser = MMCIFParser(QUIET=True)
    io = PDBIO()

    try:
        structure = parser.get_structure("model", cif_file)
        output_file = cif_file.replace(".cif", ".pdb")
        io.set_structure(structure)
        io.save(output_file)
        print(f"✅ Converted: {cif_file} → {output_file}")
    except Exception as e:
        print(f"❌ Failed to convert {cif_file}: {e}")

def main():
    cif_files = glob.glob("*.cif")
    if not cif_files:
        print("No CIF files found in this directory.")
        return

    for cif in cif_files:
        convert_cif_to_pdb(cif)

if __name__ == "__main__":
    main()
