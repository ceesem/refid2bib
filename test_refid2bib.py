from refid2bib import refid2bib


def test_doi():
    """DOI example:"""
    assert refid2bib("DOI: 10.1126/science.1260088") is not None


def test_arxiv():
    """Arxiv example:"""
    assert refid2bib("arXiv:1801.04381") is not None


def test_arxiv2():
    """Arxiv example:"""
    assert refid2bib('arxiv://1907.10138') is not None


def test_biorxiv():
    """Biorxiv example:"""
    assert refid2bib("https://doi.org/10.1101/406314") is not None


def test_biorxiv2():
    """Biorxiv example: tests regression of bugfix for issue #1"""
    """Hello! I've been using this library for a while, and I just started testing some functionality I hadn't needed 
    when I noticed that the biorxiv id doesn't currently work as described on the README. If I enter an id expression 
    with a colon in it like "biorxiv:570689", I get an error because the code ends up constructing a DOI with colon 
    in it. I think this is because the regular expression 'biorxiv':'^biorxiv ?|^biorxiv:' in the tests always 
    matches the first expression before the second one. It might just work to swap the two cases in the regex. """
    assert refid2bib("bioRxiv: 464909") is not None


def test_pmid():
    """pmid example:"""
    assert refid2bib('PMID: 25056931') is not None


def test_pmc():
    """PMC example:"""
    assert refid2bib('PMC3711719') is not None


def test_doi_explicit():
    """Doi example, specified reference type:"""
    assert refid2bib("DOI: 10.1126/science.1260088", ref_type='doi') is not None


def test_arxiv_custom_short_name():
    """Arxiv example, custom short name:"""
    assert refid2bib("arXiv:1801.04381", short_name='my_custom_name') is not None


def test_switching_name_order():
    """General example, switched name order:"""
    assert refid2bib("DOI: 10.1126/science.1260088", lastname_first=False) is not None


if __name__ == '__main__':
    import pytest
    pytest.main()
