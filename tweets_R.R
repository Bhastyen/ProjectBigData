# Title     : TODO
# Objective : TODO
# Created by: murph
# Created on: 2020-01-21

library(igraph)
library(igraphdata)
library(network)
library(sna)
library(ndtv)
library(visNetwork)
library(extrafont)

#install.packages('network')
#install.packages('sna')
#install.packages('ndtv')
#install.packages('visNetwork')
#install.packages('extrafont')

rm(list=ls(all=TRUE))
getwd()
setwd("D:\\Documents\\GitHub\\Java\\BigData\\ProjectBigData")
#gn <- read.table("data/graph_tweet.txt",sep=",",encoding="utf8")
gn <- read.graph("data/graph_tweet.txt", format="ncol", directed=TRUE)

#gn<-graph_from_data_frame(gn,directed=TRUE)
wgt = E(gn)$weight
tkplot(gn, edge.arrow.size=1,vertex.size = 50 ,edge.label=wgt,layout=layout.kamada.kawai,vertex.color="orange",label=TRUE,family="Arial Black")
#print(V(gn))


# watch degree distribution
deg <- degree(gn)
#tot <- vcount(gn)-1

#hist(gn)    # v=V(gn), mode="total", loops=TRUE)
#grid(col="white")
hist(deg, breaks=10, col="red", main="Histogram of node degree", border="black")    # v=V(gn), mode="total", loops=TRUE)
#grid(col="white")


