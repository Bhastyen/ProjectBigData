# Title     : communityAuthors
# Objective : find community with reserchers
# Created by: bastien
# Created on: 18/01/2020

library(igraph)
library(igraphdata)

rm(list=ls(all=TRUE))

gn <- read.graph("edge_list_authors.txt", format="ncol", directed=FALSE)
plot(gn, layout=layout.kamada.kawai)
print(V(gn))

#tkplot(gn)

print(diameter(gn))

# watch degree distribution
deg <- degree(gn)
hist(deg, breaks=1:vcount(gn)-1, xlim=c(0, 15), col="red", main="Histogram of node degree", border="black")    # v=V(gn), mode="total", loops=TRUE)
grid(col="white")

# watch community with cluster_edge_betweenness algorithm
ceb <- cluster_edge_betweenness(gn, directed=FALSE)
dendPlot(ceb, mode="hclust")
plot(ceb, gn)
#print("Length betweenness: ", length(ceb))

# watch community with cluster_label_prop algorithm
clp <- cluster_label_prop(gn)
plot(clp, gn)
#print("Length label: ", length(clp))

# watch community with  algorithm
#cfg <- cluster_fast_greedy(as.undirected(gn))
#plot(cfg, gn)
#print("Length label: ", length(cfg))
