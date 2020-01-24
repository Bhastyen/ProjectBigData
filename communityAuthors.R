# Title     : communityAuthors
# Objective : find community with reserchers
# Created by: bastien
# Created on: 18/01/2020

library(igraph)
library(igraphdata)

rm(list=ls(all=TRUE))
getwd()
setwd("C:\\Users\\basti\\Desktop\\Cours\\Informatique\\Master 2\\Semestre 1\\DataMining For BigData\\BigDataProject\\ProjectBigData")

# show the relationship between quoted authors
gn <- read.graph("edge_list_authors_references.txt", format="ncol", directed=FALSE)
wgt = E(gn)$weight
tkplot(gn, edge.arrow.size=1, vertex.size = 50, edge.label.cex = 2, vertex.label.cex = 2, edge.label=wgt, layout=layout.kamada.kawai, vertex.color=rgb(0.5,0,0), label=TRUE, family="Arial Black")

# show the relationship between authors of the articles
gn <- read.graph("edge_list_authors.txt", format="ncol", directed=FALSE)
wgt = E(gn)$weight
#tkplot(gn, edge.arrow.size=1, vertex.size = 50, edge.label.cex = 2, vertex.label.cex = 2, edge.label=wgt, layout=layout.kamada.kawai, vertex.color=rgb(0.4,1,0.4), label=TRUE, family="Arial Black")

# watch degree distribution
deg <- degree(gn)
#hist(deg, breaks=1:vcount(gn)-1, xlim=c(0, 15), col="red", main="Histogram of node degree", border="black")    # v=V(gn), mode="total", loops=TRUE)
#grid(col="white")

# watch community with cluster_edge_betweenness algorithm
ceb <- cluster_edge_betweenness(gn, directed=FALSE)
plot(ceb, gn)

# watch distribution about quoted authors in article
a <- read.csv("distribution_author_quoted.csv")
hist(a, col="red", breaks=1:10, xlim=c(0,10), main="Histogram of citations by authors top 10", border="black")