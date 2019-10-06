import pandas

input_path = "../../../data/CAFATrainingData/Swiss-Prot/"
output_path = "./output/"

go_fun_File = input_path + "uniprot_sprot_function.dat"

outputname = "function"

GoTypes = ["F", "P", "C"] #MFO, BPO, CCO
SwissFormat = ["ID", "NCBI", "Accession", "GOAs"]

org_df = pandas.read_csv(go_fun_File, sep="\t", names=SwissFormat, engine="python")
df = pandas.DataFrame(columns = ["ID","GO","namespace"])

for i in range(1,len(org_df.index)):
    current_id = org_df.iloc[i,2].split(";")[0]
    current_goas = org_df.iloc[i,3].split(";")
    for current_goa in current_goas:
        current_go = current_goa.split(",")[0]
        current_namesapse = current_goa.split(",")[1]
        df.loc[len(df.index)] = [current_id,current_go,current_namesapse]

for gotype in GoTypes:
    go = (df[df["namespace"] == gotype]).ix[:,["ID","GO"]]
    go = go.drop_duplicates(["ID","GO"])
    go.to_csv(output_path + outputname + "-" + gotype + ".tsv", sep='\t', index=False, header=False)
