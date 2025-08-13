# batch_fix_t3_for_prodigy.py
# Usage: python batch_fix_t3_for_prodigy.py
# Processes all *_T3*.pdb files in the current folder.

import os
import glob

targets = sorted(glob.glob("*_T3*.pdb"))

if not targets:
    print("No *_T3*.pdb files found in the current directory.")
    raise SystemExit

def fix_file(inp):
    outp = "cleaned_" + os.path.basename(inp)
    changed = 0
    seen_b_t3 = 0

    with open(inp, "r") as f, open(outp, "w") as g:
        for line in f:
            if line.startswith(("ATOM", "HETATM")) and len(line) > 21:
                chain_id = line[21]
                resname = line[17:20].strip()

                # Only touch ligand atoms on chain B with residue name T3
                if chain_id == "B" and resname == "T3":
                    seen_b_t3 += 1
                    # Ensure HETATM in columns 1–6
                    line = "HETATM" + line[6:]
                    # Set residue name to LIG in columns 18–20
                    line = line[:17] + "LIG" + line[20:]
                    changed += 1

            g.write(line)

    print(f"{inp} -> {outp} | modified atoms: {changed} | B:T3 atoms found: {seen_b_t3}")
    if seen_b_t3 == 0:
        print("  [!] Warning: No chain B residue T3 records found. Check chain/resname.")
    return outp, changed, seen_b_t3

print("Fixing T3 ligands (chain B) for PRODIGY-LIG compatibility...\n")
for pdb in targets:
    fix_file(pdb)

print("\nDone. Upload the cleaned files to the web server and set:")
print("  Receptor chains: A")
print("  Ligand chain & identifier: B:LIG")
