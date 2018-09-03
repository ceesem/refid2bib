from refid2bib.core import get_biorxiv_bibtex, get_doi_bibtex, get_arxiv_bibtex, get_pmid_bibtex
import re

bibtex_functions = {
    'biorxiv':get_biorxiv_bibtex,
    'doi':get_doi_bibtex,
    'arxiv':get_arxiv_bibtex,
    'pmid':get_pmid_bibtex}

def refid2bib(ref, short_name=None, lastname_first=True, ref_type=None):

    tests = {'doi':'^doi: ?|^https://doi.org/',
             'biorxiv':'^biorxiv ?|^biorxiv:',
             'arxiv': '^arxiv:|^https://arxiv.org/abs/',
             'pmid': '^pmid: ?|^(?=pmc\d*)',
    }
    
    if ref_type in tests.keys():
        query = re.search( tests[ref_type], ref.lower() )
        oid = ref[query.span()[1]:]
    else:
        for c, q in tests.items():
            query = re.search( q, ref.lower() )
            if query is not None:
                oid = ref[query.span()[1]:]
                ref_type = c
                break
        else:            
            raise ValueError( 'Cannot assign reference type for {}'.format(ref) )

    return bibtex_functions[ref_type](oid, short_name=short_name, lastname_first=lastname_first)


