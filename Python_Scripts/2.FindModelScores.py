import os
import glob
import json
import re

def extract_plddt_from_pdb(pdb_file):
    plddt_scores = []
    with open(pdb_file) as f:
        for line in f:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                try:
                    b_factor = float(line[60:66].strip())
                    plddt_scores.append(b_factor)
                except ValueError:
                    continue
    if plddt_scores:
        return sum(plddt_scores) / len(plddt_scores)
    else:
        return None

def extract_scores_from_json(json_file):
    try:
        with open(json_file) as f:
            data = json.load(f)
            iptm = data.get("iptm", None)
            ptm = data.get("ptm", None)
            return iptm, ptm
    except Exception:
        return None, None

def main():
    cif_files = glob.glob("*_model_*.cif")
    if not cif_files:
        print("No model CIF files found in this directory.")
        return

    results = []

    for cif in cif_files:
        # Match base name and model index
        match = re.match(r"(.+?)_model_(\d+)\.cif", cif)
        if not match:
            continue

        base_name = match.group(1)
        model_index = match.group(2)

        model_tag = f"{base_name}_model_{model_index}"
        json_file = f"{base_name}_summary_confidences_{model_index}.json"
        pdb_file = f"{model_tag}.pdb"

        if not os.path.exists(json_file):
            print(f"⚠️  JSON file not found for {cif}, skipping...")
            continue

        avg_plddt = None
        if os.path.exists(pdb_file):
            avg_plddt = extract_plddt_from_pdb(pdb_file)
        else:
            print(f"⚠️  PDB file not found for {model_tag}, pLDDT will be N/A")

        iptm, ptm = extract_scores_from_json(json_file)

        results.append({
            "Model": model_tag,
            "pLDDT": round(avg_plddt, 2) if avg_plddt is not None else "N/A",
            "ipTM": round(iptm, 3) if iptm is not None else "N/A",
            "pTM": round(ptm, 3) if ptm is not None else "N/A"
        })

    if not results:
        print("No complete results found.")
        return

    results = sorted(results, key=lambda x: x["pLDDT"] if isinstance(x["pLDDT"], float) else 0, reverse=True)

    print("\n Model Comparison Summary:")
    print(f"{'Model':<40} {'pLDDT':>10} {'ipTM':>10} {'pTM':>10}")
    print("-" * 70)
    for r in results:
        print(f"{r['Model']:<40} {r['pLDDT']:>10} {r['ipTM']:>10} {r['pTM']:>10}")

if __name__ == "__main__":
    main()
