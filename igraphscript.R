library(igraph)

## giant.component <- function(graph, ...) {
##   cl <- clusters(graph, ...)
##   induced.subgraph(graph, which(cl$membership == which.max(cl$csize)-1)-1)
## }

retweetgraph <- read.graph("usersagwgc.gml", format = "gml")
retweetgraph <- set.vertex.attribute(retweetgraph, "Label", value = get.vertex.attribute(retweetgraph, "name"))


## cl = fastgreedy.community(as.undirected(retweetgraph))
## gc <- 

## gc <- giant.component(retweetgraph)
## Filter on out degree>1
#cores <- graph.coreness(retweetgraph, mode="all")
#filtered <- induced.subgraph(retweetgraph, which(cores>1)-1)



## Get shortest paths, do hierarchical clustering
sp <- shortest.paths(retweetgraph)
hc <- hclust(dist(sp))

## Plot dendogram
#plot(hc)


## Mark first 10 non-trivial partitions (i.e. ignore first)
for(i in 2:10) {
cluster <- as.character(cutree(hc, k=i))
#cluster[1] <- "0" #Probably don't need this?
retweetgraph <- set.vertex.attribute(retweetgraph, name=paste("HC",i,sep=""), value=cluster)
}


write.graph(retweetgraph, "igraphagw.gml", format="gml")
