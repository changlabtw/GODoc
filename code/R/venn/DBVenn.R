target = "ALL"
mode = 1
#first = paste("/Users/blueswen/Documents/protein/DB/org/function-",target,".tsv",sep = "")
#second = paste("/Users/blueswen/Documents/protein/DB/t0/function-",target,".tsv",sep = "")
#third = paste("/Users/blueswen/Documents/protein/DB/t1/function-",target,".tsv",sep = "")
first = "/Users/blueswen/Documents/protein/data/CAFATrainingData/Swiss-Prot/id1"
second = "/Users/blueswen/Documents/protein/Supplementary_data/data/SwissProt-t0/id.txt"
third = "/Users/blueswen/Documents/protein/Supplementary_data/data/SwissProt-t1/id.txt"

if (mode == 1){
  first = c(readLines(first))
  second = c(readLines(second))
  third = c(readLines(third))
}else if (mode == 2){
  first = unique(read.csv(first,sep = "\t",header = FALSE)$V1)
  second = unique(read.csv(second,sep = "\t",header = FALSE)$V1)
  third = unique(read.csv(third,sep = "\t",header = FALSE)$V1)
}else if (mode == 3){
  first = unique(read.csv(first,sep = "\t",header = FALSE)$V2)
  second = unique(read.csv(second,sep = "\t",header = FALSE)$V2)
  third = unique(read.csv(third,sep = "\t",header = FALSE)$V2)
}

input <-list(first, second, third)
names(input)<-c("GO_org","GO_t0","GO_t1")
venn(input)

if (mode == 1){
  title(paste(target," Pair Amount",sep = ""))
}else if (mode == 2){
  title(paste(target," Sequence Amount",sep = ""))
}else if (mode == 3){
  title(paste(target," GO Amount",sep = ""))
}
