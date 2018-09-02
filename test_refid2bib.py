from refid2bib import *

doi_biorxiv = "https://doi.org/10.1101/406314"
doi_arxiv = "arXiv:1801.04381"
doi_general = "DOI: 10.1126/science.1260088"

print( 'General example:')
print( refid_to_bib(doi_general) )

print( 'Arxiv example:')
print( refid_to_bib(doi_arxiv) )

print( 'Biorxiv example:')
print( refid_to_bib(doi_biorxiv) )

print( 'General example forward order:')
print( refid_to_bib(doi_general, lastname_first=False ) )

print( 'Arxiv example forward order:')
print( refid_to_bib(doi_arxiv, lastname_first=False ) )

print( 'Biorxiv example forward order:')
print( refid_to_bib(doi_biorxiv, lastname_first=False ) )
