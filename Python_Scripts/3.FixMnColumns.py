#!/usr/bin/env python3
import os, sys, glob

MN_RESIDUE_START = 9001  # starting residue number for Mn ions

def process_file(input_file):
    output_file = "haddock_ready_" + os.path.basename(input_file)
    mn_counter = 0

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            # Identify Mn ions robustly (element field or atom name)
            is_mn = (
                line.startswith("HETATM") and
                (
                    line[76:78].strip().upper() == "MN" or
                    line[12:16].strip().upper().startswith("MN")
                )
            )

            if is_mn:
                atom_serial = int(line[6:11])       # cols 7–11
                chain_id    = line[21]             # col 22
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                occ = float(line[54:60])
                bfac = float(line[60:66])

                new_resnum = MN_RESIDUE_START + mn_counter
                mn_counter += 1

                new_line = (
                    f"HETATM{atom_serial:5d} "
                    f"{'MN+2':>4} "
                    f"{'MN2':>3} {chain_id}"
                    f"{new_resnum:4d}    "
                    f"{x:8.3f}{y:8.3f}{z:8.3f}"
                    f"{occ:6.2f}{bfac:6.2f}          MN\n"
                )
                outfile.write(new_line)
                outfile.write("TER\n")
            else:
                outfile.write(line)

    print(f"Saved: {output_file}")

def main():
    # If files are provided as args, use them; otherwise, auto-match typical names
    files = sys.argv[1:]
    if not files:
        files = sorted(glob.glob("fold_*_8mn_model_*.pdb"))
    if not files:
        print("No matching PDB files found.")
        return
    for f in files:
        process_file(f)

if __name__ == "__main__":
    main()
