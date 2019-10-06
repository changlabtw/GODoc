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
NUM_FOLD<-as.numeric(args[2])

######################
# load data
######################
data<-read.csv(train_tfpssm, header=FALSE)
if(is.na(data[1,ncol(data)]))
{
  data<-data[,-ncol(data)] #remove the last useless column, ie, proteinID,class,0.23,...,034,
}
#sort data by class
data<-data[with(data, order(V2)),]
id<-data[,1]
class<-as.vector(data[,2])
fea<-data[,c(3:length(data))]

######################
# Correspondence Analysis
######################
m.CA<-CA(fea, graph=FALSE)
CA_dim<-min(which(m.CA$eig$"cumulative percentage of variance" > 95)) #select the number of CA deminsion which covers more than 95% variance
print(paste("# of deminsions with cumulative percentage > 95% =",CA_dim))

######################
# data output
######################
d<-cbind(id, class, m.CA$row$coord) #1:protein ID, 2:protein label
# output json format for CA 2D plot
out_str<-""
classes<-unique(class)
for(sel_class in classes)
{
 s_d<-subset(d, regexpr(sel_class, data$V2) > 0)

 # output x,y position
 out_str<-paste(out_str,"[\n data:[")
 for(i in 1:nrow(s_d))
 {
	out_str<-paste(out_str, "[", s_d[i,3], ",", s_d[i,4], "],")
 }
 out_str<-paste(out_str,"]\n")
 # output labels
 out_str<-paste(out_str,"labels:[")
 for(i in 1:nrow(s_d))
 {
	out_str<-paste(out_str, s_d[i,1], ",")
 }
 out_str<-paste(out_str,"]\n")
 # output localization site
 out_str<-paste(out_str,"loc:\"",sel_class,"\"\n");
 out_str<-paste(out_str,"],\n");
}
cat(out_str,file="plot_model.json")

############################################
# perform n-fold cross validation
############################################
index<-1:nrow(data)
pred_c<-class

for(fold in 0:(NUM_FOLD-1))
{
  print(paste("start:",fold+1,"-fold"))
  train_i <-index[index%%NUM_FOLD!=fold]
  test_i  <-index[index%%NUM_FOLD==fold]
  train_c <-class[train_i]
  
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
    pred_c[test_i[i]]<-train_c[sim_index]
  }
  print(paste(" correct num =", sum(pred_c[test_i]==class[test_i]), "/", nrow(test_vec)))
}

print("Total")
print(paste(" sum =",sum(pred_c==class)))
print(paste(" ACC =",100*mean(pred_c==class)))

### output result ####
output_res<-cbind(as.vector(id),as.vector(class),as.vector(pred_c),as.integer(pred_c==class))
colnames(output_res)<-c("name","family","pred_family","correct")
write.csv(output_res,file="1NN_res.csv",quote = FALSE)
pred_res<-as.data.frame(output_res)
pred_res$correct<-as.integer(as.vector(pred_res$correct))

######################################
# accuracy analysis
######################################
acc_F<-file("accuracy.csv")
outputLine<-"family,precision,recall"

for(f in classes)
{
	precision <- 100*mean(pred_res$correct[grep(f,pred_res$pred_family)])
	recall    <- 100*mean(pred_res$correct[grep(f,pred_res$family)])
	outputLine<-c(outputLine, paste(f,precision,recall,sep=","))
}

precision <- 100*mean(pred_res$correct[pred_res$pred_family != -1])
recall    <- 100*mean(pred_res$correct)
outputLine<-c(outputLine, paste("all",precision,recall,sep=","))

writeLines(outputLine, acc_F)
close(acc_F)

