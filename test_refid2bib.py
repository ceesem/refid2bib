from refid2bib import refid2bib

doi_biorxiv = "https://doi.org/10.1101/406314"
arxiv_id = "arXiv:1801.04381"
doi_general = "DOI: 10.1126/science.1260088"
pmid = 'PMID: 25056931'
pmc_id = 'PMC3711719'

print( 'DOI example:')
print( refid2bib(doi_general) )

print( 'Arxiv example:')
print( refid2bib(arxiv_id) )

print( 'Biorxiv example:')
print( refid2bib(doi_biorxiv) )

print( 'pmid example:')
print( refid2bib(pmid) )

print( 'PMC example:')
print( refid2bib(pmc_id) )

print( 'Doi example, specified reference type:')
print( refid2bib(doi_general, ref_type='doi') )

print( 'Arxiv example, custom short name:')
print( refid2bib(arxiv_id, short_name='my_custom_name' ) )

print( 'General example, switched name order:')
print( refid2bib(doi_general, lastname_first=False ) )
