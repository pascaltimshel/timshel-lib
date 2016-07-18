############### SYNOPSIS ###################
# Mapping of gene lists: FROM ncbi entrez ids TO ensembl gene names

### DESCRIPTION
# ...

### OUTPUT: 
# ....

### REMARKS:
# ....


############################################

### Installation
# source("https://bioconductor.org/biocLite.R")
# biocLite("biomaRt")
library(biomaRt)
library(dplyr)


rm(list=ls())

wd <- "XXXX"
setwd(wd)


# ======================================================================= #
# ==============================  biomaRt  ============================== #
# ======================================================================= #

### Inspect/explore the options for filters and attributes
listMarts()
ensembl <- useMart(biomart = "ensembl", dataset = "mmusculus_gene_ensembl") # IMPORTANT to save "mart"
attributePages(ensembl) 
  # ^ OBS: you can only qury a single "page" a at time using getBM(). 
  # I.e. you cannot get feature data and homolog data in a single getBM() call.
tmp.attr <- listAttributes(ensembl) # ~1280 attributes
tmp.attr
tmp.filters <- listFilters(ensembl) # ~265 filers (e.g. entrezgene)
tmp.filters
filterType("entrezgene",ensembl)

### Filters to use
# entrezgene: EntrezGene ID
# entrezgene_transcript_name: EntrezGene transcript name ID
# transcript_gencode_basic: basic GENCODE transcript annotation?

### Features - MUST have
# ensembl_gene_id
# external_gene_name (Associated Gene Name): gene name!
# external_gene_source: e.g. "MGI Symbol"

### Features - species specific [only returns something for species specific genes!]
# HUMAN: "hgnc_symbol", "hgnc_id"
# MOUSE: mgi_id/mgi_symbol/mgi_description

### Features - POTENTIAL
# ensembl_transcript_id
# ensembl_exon_id

### Features - biology
# description [unique for each ensembl_gene_id]: description of gene function + more
# name_1006 [multi-entry]: GO Term Name [note that the feature "namespace_1003" is the GO domain, e.g. cellular component, biological process, and molecular function]
# gene_biotype [?unique?]: protein_coding, unprocessed_pseudogene, pseudogene, and ~40 more possible values
# wikigene_description [?unique?]: not so well covered
# source: "ensembl_havana","ensembl", "havana", "insdc", "mirbase", ..?
# status:  "KNOWN", "KNOWN_BY_PROJECTION", "NOVEL".. ?
# hsapiens_homolog_ensembl_gene or hsapiens_homolog_associated_gene_name [multi-entry]: returns multiple entries for homolog genes

# ======================================================================= #
# ===============   INITIAL NOTES ABOUT biomaRt USAGE  ================== #
# ======================================================================= #

# 1) if a requested feature for a given "entry" contains multiple values, then the entry will be "multi-row" - one for each value in feature. 
    # The other features will be duplicated.
    # Example #1: if a ensembl_gene_id maps to multiple entrezgene (EntrezGene ID), the ensembl_gene_id will be duplicated/copied for each entrezgene.
    # Example #2: when requestion GO annotation (e.g. name_1006), most genes have multiple GO annotations. For each gene, each GO annotation will have its own entry/row with the ensembl_gene_id duplicated.
# 2) attributePages(ensembl) 
  #  You can only qury a single "page" a at time using getBM(). 
  # I.e. you cannot get feature data and homolog data in a single getBM() call.


# ======================================================================= #
# ==============================   ALL GENES   ========================== #
# ======================================================================= #

### Get all Ensembl Gene IDs
df.BM.all.ids <- getBM(attributes = c("ensembl_gene_id"), mart=ensembl)
nrow(df.BM.all.ids)# 48034
str(df.BM.all.ids)

### Features page
df.BM.all.feature <- getBM(attributes = c("ensembl_gene_id", 
                                  "entrezgene", 
                                  "external_gene_name",
                                  "chromosome_name",
                                  "transcript_count",
                                  "gene_biotype",
                                  "source",
                                  "status",
                                  "description", 
                                  "name_1006"), mart=ensembl)
  # ^^ name_1006: go name - takes a *loooong time* to download
str(df.BM.all.feature)

### Homolog page
df.BM.all.homolog <- getBM(attributes = c("ensembl_gene_id", 
                                  "hsapiens_homolog_ensembl_gene", 
                                  "hsapiens_homolog_associated_gene_name",
                                  "hsapiens_homolog_orthology_confidence"), mart=ensembl)
str(df.BM.all.homolog)


### Collapsing multi-entries - using dplyr summarise_each()
df.BM.all.feature.collapsed <- df.BM.all.feature %>% group_by(ensembl_gene_id) %>% summarise_each(funs(paste0(unique(.), collapse=";"))) # collapse each "multi-row entry" for all columns in the data frame
df.BM.all.homolog.collapsed <- df.BM.all.homolog %>% group_by(ensembl_gene_id) %>% summarise_each(funs(paste0(unique(.), collapse=";"))) # collapse each "multi-row entry" for all columns in the data frame
### Collapsing multi-entries - did *NOT* work properly
# df.x <- df.BM.all %>% group_by(ensembl_gene_id) %>% mutate(go=paste0(name_1006,collapse=";")) # not the thing I want. keeps the multi-row representation

### Checks
any(duplicated(df.BM.all.feature.collapsed$ensembl_gene_id)) # --> False
any(duplicated(df.BM.all.homolog.collapsed$ensembl_gene_id)) # --> False
nrow(df.BM.all.feature.collapsed) # --> 22708
nrow(df.BM.all.homolog.collapsed) # --> 48034


###------------- Merge df.BM.all* ------------- ###
### step1: we use the "df.BM.all.ids" to ensure that all ensembl_gene_id will be in the data frame
df.BM.all.merged.collapsed <- df.BM.all.ids %>% left_join(df.BM.all.feature.collapsed)
### step2
df.BM.all.merged.collapsed <- df.BM.all.merged.collapsed %>% left_join(df.BM.all.homolog.collapsed)
###-------------------------------------------- ###


### Write table
file.ensmbl_annotation <- "biomaRt-annotation-mmusculus_gene_ensembl-v84.txt" 
write.table(df.BM.all.merged.collapsed, file=file.ensmbl_annotation, col.names=T, row.names=F, quote=F, sep="\t")

