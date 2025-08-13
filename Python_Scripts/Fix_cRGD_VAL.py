# save as clean_pdb_for_haddock.py, run: python3 clean_pdb_for_haddock.py in.pdb out.pdb
import sys
inp, outp = sys.argv[1], sys.argv[2]
def elem_from_name(atomname):
    a = atomname.strip()
    # 2-letter elements first
    for e in ("FE","CL","BR","NA","MG","ZN","CA","MN","CO","NI","CU","SE","SI","HG","CD","AL","SR","CS","KR","XE","RB"):
        if a.upper().startswith(e): return e
    return a[0].upper()
with open(inp) as f, open(outp,"w") as g:
    for line in f:
        if line.startswith(("ATOM","HETATM")):
            # Chain ID A (column 22). If you prefer blank, comment next line.
            line = line[:21] + "A" + line[22:]
            # Element (columns 77–78) from atom name (columns 13–16)
            elem = elem_from_name(line[12:16]).rjust(2)
            line = line[:76] + elem + line[78:]
        g.write(line)
