from refid2bib import refid2bib

doi_biorxiv = "https://doi.org/10.1101/406314"
doi_arxiv = "arXiv:1801.04381"
doi_general = "DOI: 10.1126/science.1260088"

print( 'General example:')
print( refid2bib(doi_general) )

print( 'Arxiv example:')
print( refid2bib(doi_arxiv) )

print( 'Biorxiv example:')
print( refid2bib(doi_biorxiv) )

print( 'General example forward order:')
print( refid2bib(doi_general, short_name='custom_name_test', lastname_first=False ) )

print( 'Arxiv example forward order:')
print( refid2bib(doi_arxiv, short_name='custom_name_test', lastname_first=False ) )

print( 'Biorxiv example forward order:')
print( refid2bib(doi_biorxiv, short_name='custom_name_test', lastname_first=False ) )
