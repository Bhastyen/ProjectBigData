
library(igraph)
library(igraphdata)
library(network)
library(sna)
library(ndtv)
library(visNetwork)
library(extrafont)

rm(list=ls(all=TRUE))
getwd()
setwd("D:\\Documents\\GitHub\\Java\\BigData\\ProjectBigData")

gn <- read.graph("data/graph_tweet_par_an.txt", format="ncol", directed=TRUE)
wgt = E(gn)$weight
tkplot(gn, edge.arrow.size=1,vertex.size = 50,vertex.label.cex=2, edge.label.cex = 2,edge.label=wgt,layout=layout.kamada.kawai,vertex.color="orange",label=TRUE,family="Arial Black")
