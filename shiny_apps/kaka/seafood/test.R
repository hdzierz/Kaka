tree <- read.csv(paste('http://10.1.4.56:8080/api/seafood/tree/?fmt=csv/', sep=''), header=TRUE)




gs <- unique(tree$Level.1)

tr <- list()
for(g in gs){
  its2 <- tree[tree$Level.1==g,]
  gs2 <- unique(its2$Level.2)
  subtr2 <- list()
  for(g2 in gs2){
    its3 <- tree[its2$Level.2==g2,]
    gs3 <- unique(its3$Level.3)
    subtr3 <- list()
    for(g3 in gs3){
      its4 <- tree[its3$Level.3==g3,]
      gs4 <- unique(its4$Level.4)
      subtr4 <- list()
      for(g4 in gs4){
        its5 <- tree[its4$Level.4==g4,]
        gs5 <- unique(its4$Level.5)
        subtr5 <- list()
        for(g5 in gs5){
          subtr5[[g5]] <- ""
        }
      }
    }
    subtr2[[it2]] <- subtr3
  }
  tr[[g]] <- subtr2
}

print(tr)

