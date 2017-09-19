#!/usr/bin/env python2.7

from collections import defaultdict

#file_mapping = "Mus_musculus.GRCm38.89.head10.gtf"
# file_mapping = "../mapping-gtf_ensembl89/Mus_musculus.GRCm38.89.gtf"
# file_mapping = "./gene_mapping.GRCh38.ens_v90/Homo_sapiens.GRCh38.90.gtf"
file_mapping = "Homo_sapiens.GRCh38.90.gtf"

#file_mapping = "../gtf-cellranger/refdata-cellranger-mm10-1.2.0.genes.gtf"
#file_mapping = "refdata-cellranger-mm10-1.2.0.genes.head10.gtf"

dict_mapping_ensembl2gene_name = defaultdict(list)
dict_mapping_gene_name2ensembl = defaultdict(list)



dict_lines_could_no_map = {}

with open(file_mapping, 'r') as fh_in:
	for line in fh_in:
		if line.startswith("#"):
			continue
		fields = line.strip().split("\t")
		#print fields
		attribute_field = fields[8]
		attributes = attribute_field.strip(";").split(";") # we strip the trailing ";" avoid an 'empty' last field
		tmp_entry_attributes_dict = {}
		for attribute in attributes: # PROCESSING: gene_id "ENSMUSG00000102693"; gene_version "1"; gene_name "4933401J01Rik"; gene_source "havana"; gene_biotype "TEC";
			tag_value_pair = attribute.strip(" ").split(" ")
			#print tag_value_pair
			tag = tag_value_pair[0]
			value = tag_value_pair[1]
			tmp_entry_attributes_dict[tag] = value
		#print "tmp_entry_attributes_dict", tmp_entry_attributes_dict
		try:
			gene_id = tmp_entry_attributes_dict["gene_id"].replace('"', '') # e.g. ENSMUSG00000102693
			gene_name = tmp_entry_attributes_dict["gene_name"].replace('"', '') # e.g. 4933401J01Rik
			dict_mapping_ensembl2gene_name[gene_id].append(gene_name)
			dict_mapping_gene_name2ensembl[gene_name].append(gene_id)
		except:
			dict_lines_could_no_map[line] = 0 # saving value
		
# 		if not gene_name in mapping_dict:
# 			mapping_dict[gene_name] = [ensembl_id]
# 		else:
# 			n_douple_mapping += 1
# 			print "Douple mapping..."
# 			mapping_dict[gene_name].append(ensembl_id)



### Taking unique genes AND alphanumeric sorting 
for gene_id in dict_mapping_ensembl2gene_name:
	dict_mapping_ensembl2gene_name[gene_id] = sorted(list(set(dict_mapping_ensembl2gene_name[gene_id])))

for gene_name in dict_mapping_gene_name2ensembl:
	dict_mapping_gene_name2ensembl[gene_name] = sorted(list(set(dict_mapping_gene_name2ensembl[gene_name])))



with open("gtf.map_out.ensembl2gene_name.txt", 'w') as fh_out:
	for gene_id, dummy in sorted(dict_mapping_ensembl2gene_name.items(), key=lambda (k, v): int(len(v)), reverse=True): # THIS WORKS
	#for gene_id in sorted(dict_mapping_ensembl2gene_name, key=lambda k: len(dict_mapping_ensembl2gene_name[k]), reverse=True): # THIS WORKS
	#for gene_id in dict_mapping_ensembl2gene_name: # no sorting
		fh_out.write(str(len(dict_mapping_ensembl2gene_name[gene_id])) + "\t" + gene_id + "\t" + "\t".join(dict_mapping_ensembl2gene_name[gene_id]) + "\n" )



with open("gtf.map_out.gene_name2ensembl.txt", 'w') as fh_out:
	for gene_name, dummy in sorted(dict_mapping_gene_name2ensembl.items(), key=lambda (k, v): int(len(v)), reverse=True): # THIS WORKS
	#for gene_name in sorted(dict_mapping_gene_name2ensembl, key=lambda k: len(dict_mapping_gene_name2ensembl[k]), reverse=True): # THIS WORKS
	#for gene_name in dict_mapping_gene_name2ensembl: # no sorting
		fh_out.write(str(len(dict_mapping_gene_name2ensembl[gene_name])) + "\t" + gene_name + "\t" + "\t".join(dict_mapping_gene_name2ensembl[gene_name]) + "\n" )


with open("gtf.map_out.lines_could_not_map.txt", 'w') as fh_out:
	for line in dict_lines_could_no_map:
		fh_out.write(line + "\n" )

print len(dict_lines_could_no_map)

print "DONE"


