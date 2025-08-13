import os

# Direct RGD-contacting residues
key_residues_a = {150, 218}                      # αV (Chain A)
key_residues_b = {121, 122, 123, 214, 215, 220}  # β3 (Chain B)

# Prompt user for multiple input files
input_files = input("Enter one or more PDB filenames (space-separated): ").strip().split()

for input_file in input_files:
    base_name = os.path.basename(input_file)
    output_file = f"renumbered_{base_name}"
    model_name = os.path.splitext(base_name)[0]
    keyres_output_file = f"KeyRes_{model_name}.txt"

    new_lines = []
    residue_map = {}
    keyres_renumbered_A = {}
    keyres_renumbered_B = {}
    res_id_counter = None

    # Step 1: Find max residue number in Chain A
    with open(input_file) as f:
        lines = f.readlines()
        last_res_a = max([
            int(line[22:26])
            for line in lines
            if line.startswith("ATOM") and line[21] == "A"
        ])
        res_id_counter = last_res_a

    # Step 2: Renumber Chain B and record key residues
    for line in lines:
        if not line.startswith("ATOM"):
            new_lines.append(line)
            continue

        chain = line[21]
        resnum = int(line[22:26])
        res_uid = (chain, resnum)

        if chain == "B":
            if res_uid not in residue_map:
                res_id_counter += 1
                residue_map[res_uid] = res_id_counter

                if resnum in key_residues_b:
                    keyres_renumbered_B[resnum] = res_id_counter

            new_resnum = residue_map[res_uid]
            newline = (
                line[:21] + "A" +
                f"{new_resnum:4d}" + line[26:]
            )
        else:
            if resnum in key_residues_a:
                keyres_renumbered_A[resnum] = resnum
            newline = line

        new_lines.append(newline)

    # Step 3: Save renumbered PDB
    with open(output_file, "w") as f:
        f.writelines(new_lines)

    # Step 4: Print and save key residues
    print(f"\n🔎 Key RGD-binding residues for {input_file}:")

    with open(keyres_output_file, "w") as keyfile:
        keyfile.write("Chain A (original → new):\n")
        for orig in sorted(keyres_renumbered_A):
            print(f"αV: {orig} → {keyres_renumbered_A[orig]}")
            keyfile.write(f"αV: {orig:<5} → {keyres_renumbered_A[orig]}\n")

        keyfile.write("\nChain B (original → new in merged A):\n")
        for orig, new in sorted(keyres_renumbered_B.items()):
            print(f"β3: {orig} → {new}")
            keyfile.write(f"β3: {orig:<5} → {new}\n")

    print(f"\n✅ Done processing: {input_file}")
    print(f"Renumbered PDB: {output_file}")
    print(f"Key residues file: {keyres_output_file}")
