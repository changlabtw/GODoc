#!/bin/env Rscript

#####
# require for Correspondence Analysis
#####
library("FactoMineR")

######################
# read inputs
######################
args<-commandArgs(TRUE)
train_tfpssm<-args[1]
train_label<-args[2]
NUM_FOLD<-as.numeric(args[3])
nfold_list <- args[4]

train_tfpssm <- "~/Documents/protein/pps/R/new_train/model_tfpssm"
train_label <- "~/Documents/protein/pps/R/new_train/function.tsv"
NUM_FOLD <- 5
nfold_list <- "~/Documents/protein/pps/R/new_train/fold_list"

######################
# load data
######################
data<-read.csv(train_tfpssm, header=FALSE)
if(is.na(data[1,ncol(data)]))
{
  data<-data[,-ncol(data)] #remove the last useless column, ie, proteinID,class,0.23,...,034,
}
data <- data[complete.cases(data),] #remove vector with na
#remove duplicatd protein by id
data<-data[!duplicated(data[1]),]
id<-data[,1]
fea<-data[,c(2:length(data))]

label <- read.table(train_label, header = FALSE)

nlist <- list()
nfold_file <- readLines(nfold_list)

for(line in nfold_file){
  tmplist <- c()
  fold <- strsplit(line,'\t')
  for(entry in fold[[1]]){
    tmplist <- union(tmplist, strsplit(entry,',')[[1]][[1]])
  }
  nlist <- append(nlist, list(tmplist))
}

######################
# Correspondence Analysis
######################
m.CA<-CA(fea, graph=FALSE)
CA_dim<-min(which(m.CA$eig$"cumulative percentage of variance" > 95)) #select the number of CA deminsion which covers more than 95% variance
print(paste("# of deminsions with cumulative percentage > 95% =",CA_dim))

############################################
# perform n-fold cross validation
############################################
index <- 1:nrow(data)
pred_id <- id

for( fold in 1:length(nlist)){
  print(paste("start:",fold,"-fold"))
  train_i <-c()
  test_i <- c()
  for( i in 1:length(id)){
    if(id[[i]] %in% nlist[[fold]]){
      test_i <- append(test_i, i)
    }
    else{
      train_i  <- append(train_i, i)
    }
  }
  print(paste("train number:",length(train_i)))
  print(paste("test number:",length(test_i)))
  train_id <-id[train_i]
  
  tmp_d <-rbind(fea[train_i,],fea[test_i,])
  fold.CA <-CA(tmp_d, ncp=CA_dim, row.sup=((length(train_i)+1):nrow(tmp_d)), graph=FALSE)
  
  train_vec<-fold.CA$row$coord
  test_vec <-fold.CA$row.sup$coord
  
  ### nearest neighbor prediction ###  
  for(i in 1:nrow(test_vec))
  {
    sim <- -Inf
    sim_index<-1
    for(j in 1:nrow(train_vec))
    {
      tmp_sim<-sqrt(sum((test_vec[i,] - train_vec[j,]) ^ 2))*(-1)
      if(tmp_sim > sim)
      {
        sim<-tmp_sim
        sim_index<-j
      }
    }
    ## assing ans
    pred_id[test_i[i]]<-train_id[sim_index]
  }
  ## calculate recall, precision, F-measure
  df <- data.frame(org=id[test_i],pred=pred_id[test_i])
  r <- 0
  p <- 0
  
  for(i in 1:length(test_i)){
    org_c <- label[,2][which(label[,1] %in% df[,1][i])]
    pred_c <- label[,2][which(label[,1] %in% df[,2][i])]
    r <- r + length(intersect(org_c,pred_c))/length(pred_c)
    p <- p + length(intersect(org_c,pred_c))/length(org_c)
  }
  r <- r/length(test_i)
  p <- p/length(test_i)
  f <- (2*r*p)/(r+p)
  print(paste("recall: ",r))
  print(paste("precision: ",p))
  print(paste("F-measure: ",f))
  #print(paste(" correct num =", sum(pred_id[test_i]==id[test_i]), "/", nrow(test_vec)))
}


print("Total")
df <- data.frame(org=id,pred=pred_id)
r <- 0
p <- 0
org_cs <- c()
pred_cs <- c()
for(i in 1:nrow(df)){
  org_c <- label[,2][which(label[,1] %in% df[,1][i])]
  pred_c <- label[,2][which(label[,1] %in% df[,2][i])]
  org_cs <- append(org_cs, paste(org_c, collapse = ','))
  pred_cs <- append(pred_cs, paste(pred_c, collapse = ","))
  r <- r + length(intersect(org_c,pred_c))/length(pred_c)
  p <- p + length(intersect(org_c,pred_c))/length(org_c)
}
r <- r/nrow(df)
p <- p/nrow(df)
f <- (2*r*p)/(r+p)
print(paste("recall: ",r))
print(paste("precision: ",p))
print(paste("F-measure: ",f))

### output result ####
output_res<-cbind(as.vector(id),as.vector(pred_id),as.vector(org_cs),as.vector(pred_cs))
colnames(output_res)<-c("ID","pred_ID","org_class","pred_class")
#write.csv(output_res,file="1NN_res.csv",quote = FALSE)