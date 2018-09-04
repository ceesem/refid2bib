# refid2bib

A simple tool get get bibtex entries based on a variety of common academic ids. It's not the only such thing out there (I was largely inspired by [doi2bib](https://www.doi2bib.org)), but I wanted something that could handle [Biorxiv](https://www.biorxiv.org) citations in a manner that was parallel with [arXiv](https://www.arxiv.org) citations.

## How to use:

### From a python console/notebook:

There's only one function to use, `refid2bib`, which will attempt to intuit your request. It can handle DOIs, Arxiv Ids, Pubmed ids, PMC ids, and Biorxiv ids. See `test_refid2bib.py` for various examples.

For example, a typical doi copied from Pubmed:
```
from refid2bib import refid2bib
doi = "DOI: 10.1126/science.1260088"
bibtex = refid2bib(doi)
print(bibtex)
```
will return
```
@article{Chen_2015,
    doi = {10.1126/science.1260088},
    url = {https://doi.org/10.1126%2Fscience.1260088},
    year = 2015,
    month = {jan},
    publisher = {American Association for the Advancement of Science ({AAAS})},
    volume = {347},
    number = {6221},
    pages = {543--548},
    author = {Chen, F. and Tillberg, P. W. and Boyden, E. S.},
    title = {Expansion microscopy},
    journal = {Science}
}
```

To specify the reference name that will be used, use the `short_name` parameter like so
```
doi = "https://doi.org/10.1126/science.1260088"
custom_name = 'my_custom_name'
bibtex = refid2bib(doi, short_name=custom_name)
print(bibtex)
```
to return:
```
@article{my_custom_name,
    doi = {10.1126/science.1260088},
    ...
```


For author names if you would prefer to use (First Middle Last Suffix) order instead of the default (Last Suffix, First Middle), set the `lastname_first` parameter to `False`.
```
doi = "https://doi.org/10.1126/science.1260088"
bibtex = refid2bib(doi, lastname_first=False)
print(bibtex)
```
This returns the same thing, but now the author line is:
```
    author = {F. Chen and P. W. Tillberg and E. S. Boyden},
```

### From the command line:

`refid2bib` can be run as a function with a reference passed as an argument like so:

```
python -m refid2bib https://doi.org/10.1101/406314
```

Note that the custom name and author name order options are not yet implemented in the command line version.

## Format Detection

Case does not matter for any reference.

_DOI:_
    A doi needs to either start with `https://doi.org/` or have a leading `doi: ` (with or without the space). The id is taken to be everything after the slash of the URL or the space/colon. For example,`doi: 10.1126/science.1260088` or `https://doi.org/10.1126/science.1260088`.

_Biorxiv:_
    Biorxiv entries are detected if they start with a `biorxiv: ` (with or without the space) or have a DOI that corresponds to Biorxiv (i.e. a CSHL 10.1101 prefix and a purely numeric suffix). This mode adds eprint and eprinttype entries to the bibtex output, similar to Arxiv entries. For example, `biorxiv:376830` or `https://doi.org/10.1101/376830`. These are returned as `@online` types, not articles.

_ArXiv:_
    Arxiv entries are detected if they start with `arxiv:` (no space) or from the URL directly `https://arxiv.org/abs/`. For example, `arXiv:1801.04381` or `https://arxiv.org/abs/1801.04381`. These are returned as `@online` types, not articles.

_Pubmed:_
    Either pubmed ids or PMC ids will work, either from `pmid: ` (with or without space) or `PMC` (no space) respectively. For example, `PMID: 25056931` or `PMC3711719`.
