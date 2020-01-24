
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

gn <- read.graph("data/graph_messages_auteurs_2018.txt", format="ncol")
wgt = E(gn)$weight
tkplot(gn, edge.arrow.size=1,vertex.size = 50 ,edge.label.cex = 2,vertex.label.cex = 2,edge.label=wgt,layout=layout.kamada.kawai,vertex.color=rgb(0.8,0.4,0.4),label=TRUE,family="Arial Black")
