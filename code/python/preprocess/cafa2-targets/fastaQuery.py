from Bio import SeqIO

fasta_file = "target.fasta"
list_file = "all.txt"
out_file = "out.fasta"
targetList = []

record_dict = SeqIO.index(fasta_file, "fasta")

with open(list_file) as f:
    targetList = f.read().splitlines()

with open(out_file, 'w') as f:
    for target in targetList:
        f.write(record_dict[target].format("fasta"))
        f.write('\n')
