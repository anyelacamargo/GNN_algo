
l = c('readr', 'dplyr', 'igraph', 'plotly')
if (!require("pacman")) install.packages("pacman")

pacman::p_load(readr, dplyr, igraph, plotly)


library(readr)
library(dplyr)
library(igraph)
library(plotly)
library(e1071)


#' Plot graph using igraph
plot_inter <- function(ego_g){
  
  coords <- layout_with_fr(ego_g)
  nodes <- data.frame(
    id = V(ego_g)$name,
    x = coords[,1],
    y = coords[,2],
    color = V(ego_g)$color,
    type = V(ego_g)$type
  )
  edges <- as_data_frame(ego_g, what = "edges")
  
  edges$x0 <- coords[match(edges$from, nodes$id), 1]
  edges$y0 <- coords[match(edges$from, nodes$id), 2]
  edges$x1 <- coords[match(edges$to, nodes$id), 1]
  edges$y1 <- coords[match(edges$to, nodes$id), 2]
  edge_trace <- list(
    type = "scatter",
    mode = "lines",
    x = c(rbind(edges$x0, edges$x1, NA)),
    y = c(rbind(edges$y0, edges$y1, NA)),
    line = list(width = 1, color = "#888"),
    hoverinfo = "none"
  )
  node_trace <- list(
    type = "scatter",
    mode = "markers",
    x = nodes$x,
    y = nodes$y,
    text = nodes$id,
    hoverinfo = "text",
    marker = list(
      size = 10,
      color = nodes$color
    )
  )
  
  fig <- plot_ly()
  
  fig <- fig %>% add_trace(
    x = edge_trace$x,
    y = edge_trace$y,
    type = "scatter",
    mode = "lines",
    line = edge_trace$line,
    hoverinfo = "none"
  )
  
  fig <- fig %>% add_trace(
    x = node_trace$x,
    y = node_trace$y,
    type = "scatter",
    mode = "markers",
    text = node_trace$text,
    marker = node_trace$marker
  )
  #fig
  return(fig)
  
}

#' Setup graph
get_graph <- function(train, entity_types){
  
  g <- graph_from_data_frame(
    d = train,
    directed = TRUE
  )
  
  V(g)$type <- entity_types$type[match(V(g)$name, entity_types$entity)]
  deg <- degree(g)
  V(g)$color <- ifelse(V(g)$type == 'GENE', "yellow",
                       ifelse(V(g)$type == 'VARIANT', "red",
                            "blue"))
  return(g)

}


#' compute graph features
compute_graph_features <- function(train, entity_types) {
  
  
  g <- get_graph(train, entity_types)
 
  deg_in  <- degree(g, mode = "in")
  deg_out <- degree(g, mode = "out")
  
  degree_features <- list(
    in_mean   = mean(deg_in),
    in_median = median(deg_in),
    in_max    = max(deg_in),
    in_skew   = skewness(deg_in),
    
    out_mean   = mean(deg_out),
    out_median = median(deg_out),
    out_max    = max(deg_out),
    out_skew   = skewness(deg_out)
  )
  
 
  relation_dist <- table(train$relation)
  
  relation_features <- list(
    n_relations = length(relation_dist),
    relation_entropy = -sum((relation_dist/sum(relation_dist)) * 
                              log(relation_dist/sum(relation_dist)))
  )
  

  comp <- components(g, mode = "weak")
  
  connectivity_features <- list(
    n_components = comp$no,
    largest_component_size = max(comp$csize),
    component_ratio = max(comp$csize) / vcount(g)
  )
  
  
  global_features <- list(
    assortativity_degree = assortativity_degree(g, directed = TRUE),
    dyad_mutual = dyad_census(g)$mut,
    dyad_asym   = dyad_census(g)$asym,
    dyad_null   = dyad_census(g)$null
  )
  
 
  bet <- betweenness(g, directed = TRUE, normalized = TRUE)
  
  centrality_features <- list(
    betweenness_mean = mean(bet),
    betweenness_max  = max(bet),
    betweenness_skew = skewness(bet)
  )
  
 
  # FINAL FEATURE OBJECT
 
  features <- c(
    degree_features,
    relation_features,
    connectivity_features,
    global_features,
    centrality_features
  )
  
  return(list(
    graph = g,
    features = features
  ))
}


# Run the script
# Load data
pathname <- "data/"

train <- read_delim(paste(pathname, "train.txt", sep=''), delim = "\t", 
                    col_names = c("head", "tail", "relation"))
test <- read_delim(paste(pathname, "test.txt", sep=''), delim = "\t", 
                    col_names = c("head", "tail", "relation"))
valid <- read_delim(paste(pathname, "valid.txt", sep=''), delim = "\t", 
                    col_names = c("head", "tail", "relation"))

entity_types <- read_delim(paste(pathname,"entity2type.txt", sep=''), 
                           delim = "\t",
                           col_names = c("entity", "type"))
result = compute_graph_features(train, entity_types )
g <- result$graph
features <- result$features
print(features)

# Plots come interesting markers
pdf("graph.pdf")
# Check some knows genes
int_gene = list()
int_gene[['BIRC6']] = 'atheroslerosis'
int_gene[['CDKN2A']] = 'senescence'
int_gene[['CLOCK']] = 'senescence'
int_gene[['SIRT1']] = 'senescence'


for(gene_name in names(int_gene)[2]){
  ego_g <- make_ego_graph(g, order=1, nodes=gene_name)[[1]]
  plot(ego_g,
        vertex.size=6,
       vertex.label.cex=0.7)
 
} 
dev.off()

# Check for symmetry
df <- train
sort(table(df$relation), decreasing = TRUE)
head_deg <- sort(table(df$head), decreasing = TRUE)
head(head_deg, 20)
tail_deg <- sort(table(df$tail), decreasing = TRUE)
head(tail_deg, 20)
summary(as.numeric(head_deg))
summary(as.numeric(tail_deg))

disease_rel <- "GENE_DISEASE_ot_genetic_association"
disease_df <- df[df$relation == disease_rel, ]
sort(table(disease_df$tail), decreasing = TRUE)[1:20]
sum(duplicated(df))
p <- table(df$relation) / nrow(df)
-sum(p * log(p))
