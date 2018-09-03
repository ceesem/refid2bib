from refid2bib import *

doi_biorxiv = "https://doi.org/10.1101/406314"
doi_arxiv = "arXiv:1801.04381"
doi_general = "DOI: 10.1126/science.1260088"
pmid = 'PMID: 25056931'
pmc_id = 'PMC3711719'

print( 'General example:')
print( refid2bib(doi_general) )

print( 'Arxiv example:')
print( refid2bib(doi_arxiv) )

print( 'Biorxiv example:')
print( refid2bib(doi_biorxiv) )

print( 'pmid example:')
print( refid2bib(pmid) )

print( 'PMC example:')
print( refid2bib(pmc_id) )

print( 'Arxiv example custom short name:')
print( refid2bib(doi_general, short_name='my_custom_name' ) )

print( 'General example switched name order:')
print( refid2bib(doi_general, lastname_first=False ) )
