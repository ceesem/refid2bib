from refid2bib.core import *

bibtex_functions = {
    'biorxiv':get_biorxiv_bibtex,
    'doi':get_doi_bibtex,
    'arxiv':get_arxiv_bibtex,
}

def refid2bib(ref, short_name=None, lastname_first=True):
    doi_test = re.search('^doi: ?|^https://doi.org/', ref.lower())
    biorxiv_test = re.search('^biorxiv ?|^biorxiv:', ref.lower())
    arxiv_test = re.search('^arxiv:|^https://arxiv.org/abs/', ref.lower())

    if doi_test is not None:
        doi_id = ref[doi_test.span()[1]:]
        is_biorxiv, bioxiv_id = doi_is_biorxiv( doi_id )
        if is_biorxiv:
            oid = bioxiv_id
            ref_type = 'biorxiv'
        else:
            oid = doi_id
            ref_type = 'doi'
    elif biorxiv_test is not None:
        oid = ref[biorxiv_test.span()[1]:]
        ref_type = 'biorxiv'
    elif arxiv_test is not None:      
        oid = ref[arxiv_test.span()[1]:]
        ref_type = 'arxiv'
    else:
        raise ValueError( 'Cannot assign reference type for {}'.format(ref) )
    return bibtex_functions[ref_type](oid, short_name=short_name, lastname_first=lastname_first)

