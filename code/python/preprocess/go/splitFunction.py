import pandas

input_path = "../../../data/CAFATrainingData/GO/"
output_path = "./output/"

go_fun_File = input_path + "go_function.dat"

outputname = "function"

GoTypes = ["F", "P", "C"] #MFO, BPO, CCO
GOFormat = ["ID", "NCBI", "GO", "namespace", "code"]

df = pandas.read_csv(go_fun_File, sep="\t|,", names=GOFormat, engine="python")

for gotype in GoTypes:
    go = (df[df["namespace"] == gotype]).ix[:,["ID","GO"]]
    go = go.drop_duplicates(["ID","GO"])
    go.to_csv(output_path + outputname + "-" + gotype + ".tsv", sep='\t', index=False, header=False)
