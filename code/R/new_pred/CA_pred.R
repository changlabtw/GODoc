#!/usr/bin/env Rscript

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
test_tfpssm<-args[3]
CA_dim<-as.numeric(args[4])
test_label<-args[5]

train_tfpssm <- "/Users/blueswen/Documents/protein/pps/R/new_pred/model_tfpssm"
train_label <- "/Users/blueswen/Documents/protein/pps/R/new_pred/function.tsv"
test_tfpssm <- "/Users/blueswen/Documents/protein/pps/R/new_pred/query_merge"
CA_dim <- 36
test_label <- "/Users/blueswen/Documents/protein/pps/R/new_pred/query_function.tsv"
#test_label <- NA
######################
# load data
######################
data<-read.csv(train_tfpssm, header=FALSE)
if(is.na(data[1,ncol(data)]))
{
  data<-data[,-ncol(data)] #remove the last useless column, ie, proteinID,class,0.23,...,034,
}
data <- data[complete.cases(data),] #remove vector with na
train_id<-as.vector(data[,1])
train_fea<-data[,c(2:length(data))]

train_label <- read.table(train_label, header = FALSE)

data<-read.csv(test_tfpssm, header=FALSE)
if(is.na(data[1,ncol(data)]))
{
  data<-data[,-ncol(data)] #remove the last useless column,
}
unpred_id <-as.vector(data[!complete.cases(data),1]) #save unpredictable id
data <- data[complete.cases(data),] #remove vector with na
test_id<-as.vector(data[,1])
test_fea<-data[,c(2:length(data))]

if(!is.na(test_label)){
  test_label <- read.table(test_label, header = FALSE)
}

m<-rbind(train_fea,test_fea)
sup_i<-nrow(train_fea)+1

######################
# Correspondence Analysis
######################
m.CA<-CA(m, ncp=CA_dim, row.sup=sup_i:nrow(m), graph=FALSE)
train_vec<-m.CA$row$coord
test_vec <-m.CA$row.sup$coord

# 1 nearest neighbor prediction
pred_id<-test_id
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
   pred_id[i]<-train_id[sim_index]
}

## calculate recall, precision, F-measure
df <- data.frame(org=test_id,pred=pred_id)
org_cs <- c()
pred_cs <- c()
for(i in 1:length(test_id)){
  if(is.na(test_label)){
    org_c <- "NA"
  }
  else{
    org_c <- test_label[,2][which(test_label[,1] %in% df[,1][i])]
  }
  pred_c <- train_label[,2][which(train_label[,1] %in% df[,2][i])]
  org_cs <- append(org_cs, paste(org_c, collapse = ","))
  pred_cs <- append(pred_cs, paste(pred_c, collapse = ","))
}
if(length(unpred_id)>0){
  for(i in 1:length(unpred_id)){
    if(is.na(test_label)){
      org_c <- "NA"
    }
    else{
      org_c <- test_label[,2][which(test_label[,1] %in% df[,1][i])]
    }
    pred_c <- "NA"
    test_id <- append(test_id, unpred_id[i])
    pred_id <- append(pred_id, "NA")
    org_cs <- append(org_cs, paste(org_c, collapse = ","))
    pred_cs <- append(pred_cs, paste(pred_c, collapse = ","))
  } 
}

######################
# data output
######################
# output 1NN prediction
output_res<-cbind(as.vector(test_id),as.vector(pred_id),as.vector(org_cs),as.vector(pred_cs))
colnames(output_res)<-c("ID","pred_ID","org_class","pred_class")
#write.table(output_res, file="1NN_res.tsv", quote = FALSE, sep="\t", row.names = F)

#output test vec
na_vec <- rep(NA,ncol(test_vec))
if(length(unpred_id)>0){
  for(i in 1:length(unpred_id)){
    test_vec <- rbind(test_vec,na_vec)
  } 
}
test_vec <- cbind(test_id,test_vec)
#write.table(test_vec, file="test_vec.tsv", quote = FALSE, sep="\t", row.names = F, col.names = F)

#output train vec
train_vec <- cbind(train_id,train_vec)
#write.table(train_vec, file="train_vec.tsv", quote = FALSE, sep="\t", row.names = F, col.names = F)
