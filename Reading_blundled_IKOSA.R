##################################################################
# This code was designed to extract data from .csv files which contain
# cellular morphology measurements such as:
#"bbox_area","area_ratio","perimeter",....
# circularity","solidity","eccentricity","equivalent_diameter"
# general plots are made
##########################################################################

#################################################################################
#   Find the list of files that contain the measurements
#    -They were the output of a software called IKOSA
#    -Each file has the prefix "results_"
#################################################################################
aa<- getwd()
bb <- list.files(aa) ## List all files
piv <- grep("IKOSA_",bb)
cc <- list.files(paste(aa,"/",bb[piv],sep=""),pattern = "results_", recursive = TRUE) ## lists all the files that contain the results. goes through the subfolders

for (kk in 1:length(cc)) {
path_results<-cc[kk]
path_results_full <- paste(aa,"/",bb[piv],"/",path_results,sep="")    ###### Getting the full name/location of the file

#################################################################################
#   
#   Reading the files
#    - QC of the column
#    - Extracting the columns of the desired measurements 
#################################################################################

r_x <- read.csv(path_results_full)
flag <- sum(is.infinite(r_x[,19]))
print(flag)             ##### Safety check - finding the number of realizations in the .csv file
names_table <- names(r_x) #### Extracting the names

if (flag>0){
  warning("Infinite values found in circularity")
  r_x[is.infinite(r_x[,19]),]<-0    ##### Marking the infinite values with "0"
  m_pos <- which(r_x[,19] == 0,arr.in =  TRUE)
  r_x <- r_x[-c(m_pos),] #### Filtering the marked values
  print("Inifine values have been removed")
}

flag_1 <- sum(r_x[,19] > 3) ### Reference for abnormally large values for circularity 


if (flag_1>0){
  warning("Abnormaly high values found in circularity")
  r_x[r_x[,19] > 3,] <- 0 ##### Marking the large values with "0"
  m_pos <- which(r_x[,19] == 0,arr.in =  TRUE)  
  r_x <- r_x[-c(m_pos),] #### Filtering the marked values
  print("Abnromaly high values removed")
}



## Find the column with the name of the searched variable
## Variables to study
var_t<- c("bbox_area","area_ratio","perimeter","circularity","solidity","eccentricity","equivalent_diameter")
size <- dim(r_x)

Result_table <- matrix(data=NA,nrow=size[1], ncol=length(var_t))
stat_summary <- matrix(data=NA, nrow=length(var_t), ncol=6)
Quantiles_summary <- matrix(data=NA,nrow=length(var_t), ncol = length(seq(0,1,0.025)))
id_list <- rep(kk,size[1])



#################################################################################
#   
#   Data processing
#    - Statistical summary
#    - Extracting the columns of the desired measurements 
#################################################################################


for(i in 1:length(var_t)){
  if(grep(var_t[i],names_table)){
    temp <- grep(var_t[i],names_table)
    data_temp <- r_x[[temp[1]]]
    Result_table[,i]<- data_temp
    ## statistical evaluation
    stat_summary[i,]<- c(mean(data_temp),sd(data_temp),var(data_temp),min(data_temp),max(data_temp),median(data_temp))
    Quantiles_summary[i,] <-  quantile(data_temp,probs = seq(0,1,0.025))
  }  
}


#### Store the statistical summary into their designated valiables 

if (kk==1){
  Overall_result=Result_table
  Overall_stat = stat_summary
  Overall_id = id_list
  }else {
  Overall_result <- rbind(Overall_result,Result_table)
  Overall_stat <- rbind(Overall_stat,stat_summary)
  Overall_id <- append(Overall_id,id_list)
  
  }
  
}

var_s=c("mean","sd","var","min","max","median")

colnames(Overall_result)=var_t
Min_1=length(var_t)*length(cc)
Min_2=length(var_t)

#### Assign the statistical values to their corresponding names

for (j in 1:length(var_s)){
  for (jj in 1:length(var_t)){

  name=paste("Overall_",var_s[j],"_",var_t[jj],sep="")
  assign(name, Overall_stat[seq(jj,Min_1,Min_2),j])
}
}



#################################################################################
#   
#   Plotting and saving
#    
#     
#################################################################################





name_cat <- sub("/*","",sub(".*_","",cc[1]))
colnames(Overall_result)=c(var_t)
rownames(Overall_stat)=rep(var_t , times=length(cc))


df <- data.frame(ID=Overall_id, circ= Overall_result[,4], per= Overall_result[,3])
df$ID <- as.factor(df$ID)
image = ggplot(df, aes(x=ID, y=circ)) + geom_boxplot() +  geom_jitter(shape=1,position=position_jitter(0.2))

ggsave(file = "Summary_plot.svg", plot = image, width=20, height=8)



