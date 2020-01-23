
#install.packages('tm')
#install.packages('XML')
#install.packages('SnowballC')
#install.packages('NLP')
#install.packages('slam')
#install.packages('ggplot2')
#install.packages('wordcloud')
install.packages('cluster')
install.packages('fpc')

library(igraph)
library(igraphdata)
library(network)
library(sna)
library(ndtv)
library(visNetwork)
library(extrafont)
library(tm)
library(XML)
library(SnowballC)
library(NLP)
library(slam)
library(ggplot2)
library(wordcloud)
library(cluster)
library(fpc)

rm(list=ls(all=TRUE))
getwd()
setwd("D:\\Documents\\GitHub\\Java\\BigData\\ProjectBigData")

docs <- Corpus(DirSource("data/documents_messages/2016"))
docs

class(docs)
docsEdit <-tm_map(docs,removeWords,stopwords("english"))
length(docsEdit)

dtm <-DocumentTermMatrix(docsEdit)

freq <- colSums(as.matrix(dtm))
length(freq)
ord <-order(freq)
ord

freq[tail(ord,50)]
freq[head(ord)]

freq<-sort(freq,decreasing=TRUE)
f<- head(freq,30)
f
wf<-data.frame(word = names(freq),freq=freq)
head(wf)
barplot(freq[0:50],col=c("#FF6633", "#FFFF33"))
barplot(f[0:15],col=c("#FF6633", "#FFFF33"))
barplot(f[16:30],col=c("#FF6633", "#FFFF33"),cex.names=0.9)

wordcloud(names(freq),freq,max.word = 70)

d<- dist(t(dtm),method="euclidian")
fit <-hclust(d=d,method="ward.D2")
fit

plot(fit)
plot.new()
plot(fit,hang=-1)
groups <-cutree(fit,k=5)
rect.hclust(fit,k=5,border="red")