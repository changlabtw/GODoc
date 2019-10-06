from Bio import SeqIO

fasta_file = "out.fasta"
handle = open(fasta_file, "rU")
records = list(SeqIO.parse(handle, "fasta"))
handle.close()

print len(records)
