############### SYNOPSIS ###################
# Get biomaRt annotation

### DESCRIPTION
# ...

### OUTPUT: 
# ....

### REMARKS:
# ....

### REFERENCE:
# Ensembl biomaRt guide: http://www.ensembl.org/info/data/biomart/biomart_r_package.html

############################################

### Installation
# source("https://bioconductor.org/biocLite.R")
# biocLite("biomaRt")
library(biomaRt)
library(dplyr)


rm(list=ls())

wd <- "<INSERT WORKING DIRECTORY HERE>"
setwd(wd)


# ======================================================================= #
# ==============================  biomaRt  ============================== #
# ======================================================================= #
### Set version variable
#ENSEMBL_VERSION = NULL # for newest version
ENSEMBL_VERSION = 84 # for specific version

### List marts
listMarts() #  list BioMart databases
listEnsembl(verbose=T) # list BioMart databases hosted by Ensembl. 
listEnsembl(version=ENSEMBL_VERSION)

### List data sets
listDatasets(mart=useEnsembl(biomart="ensembl", version=ENSEMBL_VERSION), verbose=T) # here we see the dataset "hsapiens_gene_ensembl" listed.

### Connect to the BioMart database and dataset hosted by Ensembl
ensembl = useEnsembl(biomart="ensembl", dataset="hsapiens_gene_ensembl", version=ENSEMBL_VERSION, verbose=T)


### List options for filters and attributes
attributePages(ensembl) 
  # ^ OBS: you can only qury a single "page" a at time using getBM(). 
  # I.e. you cannot get feature data and homolog data in a single getBM() call.
ensembl.attr <- listAttributes(ensembl); ensembl.attr # ~1280 attributes
ensembl.filters <- listFilters(ensembl); ensembl.filters # ~265 filers (e.g. entrezgene)
filterType("entrezgene",ensembl)



# ======================================================================= #
# ==============================   ALL GENES   ========================== #
# ======================================================================= #

# SEE "biomart-gene_annotation-mmusculus.R" for working with multiple pages

### Get all Ensembl Gene IDs
df.BM.all.ids <- getBM(attributes = c("ensembl_gene_id"), mart=ensembl)
nrow(df.BM.all.ids) # 66203 for ensembl_v84
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
  # ^^ name_1006: GO name - takes a *loooong time* to download
str(df.BM.all.feature)
nrow(df.BM.all.feature) 

### Collapsing multi-entries - using dplyr summarise_each()
df.BM.all.feature.collapsed <- df.BM.all.feature %>% group_by(ensembl_gene_id) %>% summarise_each(funs(paste0(unique(.), collapse=";"))) # collapse each "multi-row entry" for all columns in the data frame
nrow(df.BM.all.feature.collapsed)

### Merge df.BM.all ###
### we use the "df.BM.all.ids" to ensure that all ensembl_gene_id will be in the data frame
df.BM.all.merged.collapsed <- df.BM.all.ids %>% left_join(df.BM.all.feature.collapsed)

### CHECKS
stopifnot(nrow(df.BM.all.ids) == nrow(df.BM.all.merged.collapsed)) # *we want to make sure that we have all genes included*

### Write table
file.ensmbl_annotation <- sprintf("biomaRt-annotation-hsapiens_ensembl-v%s.txt.gz", ifelse(is.null(ENSEMBL_VERSION), "NEWEST_RELEASE_CHECK_R_SCRIPT", ENSEMBL_VERSION))
file.ensmbl_annotation.gz <- gzfile(file.ensmbl_annotation, 'w')
write.table(df.BM.all.merged.collapsed, file=file.ensmbl_annotation.gz, col.names=T, row.names=F, quote=F, sep="\t")
close(file.ensmbl_annotation.gz)
