import requests
import re
import json
import feedparser
from nameparser import HumanName


doi_url='http://dx.doi.org'
def doi_formatter( doi, doi_base=doi_url ):
    return '/'.join((doi_base,doi))


def get_doi_bibtex( doi, short_name=None ):
    #To do, better exception handling on the request
    header={'Accept': 'application/x-bibtex'}
    data=requests.get(doi_formatter(doi), headers=header)
    bibtex = data.text + "\n"
    return replace_short_name( bibtex, short_name )


arxiv_url = "http://export.arxiv.org/api/query"
def get_arxiv_bibtex( arxiv_number, short_name=None):
    params={'id_list':arxiv_number}
    atom_data=requests.get(arxiv_url, params=params)
    data=feedparser.parse(atom_data.text)
    bibtex = parse_arxiv_bibtex( data )
    return replace_short_name(bibtex, short_name)


biorxiv_doi = "10.1101/{bid}"
def biorxiv_doi_formatter( biorxiv_id, biorxiv_base=biorxiv_doi ):
    return biorxiv_base.format(bid=biorxiv_id)

def get_biorxiv_bibtex( biorxiv_id, short_name=None):
    # to do: Bring biorxiv formatting into parity with arxiv formatting, using eprint.
    bibtex = get_doi_bibtex( biorxiv_doi_formatter(biorxiv_id) )
    biorxiv_info = "\teprinttype={{BiorXiv}},\n" \
                   "\teprint={{{bid}}}\n}}\n".format(bid=biorxiv_id)
    bibtex = bibtex[:-2] + biorxiv_info
    return replace_short_name( bibtex, short_name )


def doi_is_biorxiv( doi ):
    biorxiv_regex = "(?P<doi_prefix>10\.\d{4,}\.?\d*)\/(?P<doi_suffix>.*)"
    biorxiv_doi_test = re.search( biorxiv_regex, doi )
    if ( biorxiv_doi_test.groupdict()['doi_prefix'] == '10.1101' ) and \
        ( re.match('^\d*$', biorxiv_doi_test.groupdict()['doi_suffix']) is not None ):
        return True, biorxiv_doi_test.groupdict()['doi_suffix']
    else:
        return False, None


bibtex_functions = {
    'biorxiv':get_biorxiv_bibtex,
    'doi':get_doi_bibtex,
    'arxiv':get_arxiv_bibtex,
}

def refid_to_bib(ref, short_name=None):
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
    return bibtex_functions[ref_type](oid, short_name)


def replace_short_name(bibtex, short_name):
    if short_name is not None:
        oldreg = re.search('^@.*\{(?P<old_name>.*),', bibtex)
        old_name = oldreg.groupdict()['old_name']
        bibtex.replace( old_name, short_name )        
    return bibtex


month_map = {
    1:'jan',
    2:'feb',
    3:'mar',
    4:'apr',
    5:'may',
    6:'jun',
    7:'jul',
    8:'aug',
    9:'sep',
    10:'oct',
    11:'nov',
    12:'dec'
    }

def format_bibtex_entry(short_name,
                        authors,
                        title,
                        year,
                        month,
                        eprinttype,
                        eprint,
                        article_url):
    bibtex_header = '@article{'
    bibtex_base = "{header}{short_name},\n" \
        "\tauthor = {{{authors}}},\n" \
        "\ttitle = {{{title}}},\n" \
        "\tdate = {{{year}}},\n" \
        "\tmonth = {{{month}}},\n" \
        "\teprinttype = {{{eprinttype}}},\n" \
        "\teprint = {{{eprint}}},\n" \
        "\turl = {{{url}}}\n}}\n"
    bibtex = bibtex_base.format( header=bibtex_header,
                    short_name=short_name,
                    authors=authors,
                    title=title,
                    year=year,
                    month=month,
                    eprinttype=eprinttype,
                    eprint=eprint,
                    url=article_url)
    return bibtex

def parse_arxiv_bibtex( data ):
    #todo: exceptions versioning
    ind = 0
    
    title = data['entries'][ind]['title']

    eprinttype='arXiv'
    id_parser = re.search('http://arxiv.org/abs/(?P<id_str>.*)', data['entries'][ind]['id'])
    eprint=id_parser.groupdict()['id_str']

    author_list = [HumanName(author['name']) for author in data['entries'][ind]['authors']]
    author_str_list = []
    for author in author_list:
        if len(author.middle) == 0:
            author_str_list.append('{}, {}'.format(author.last, author.first))
        else:
            author_str_list.append('{}, {} {}'.format(author.last, author.first, author.middle ))
    authors = ' and '.join(author_str_list)

    year = data['entries'][ind]['published_parsed'].tm_year
    month = month_map[data['entries'][ind]['published_parsed'].tm_mon]

    article_url = data['entries'][0]['link']

    default_short_name = author_list[0].last.replace(' ',"_") + '_' + str(year)

    bibtex = format_bibtex_entry(default_short_name,
                                authors,
                                title,
                                year,
                                month,
                                eprinttype,
                                eprint,
                                article_url)
    return bibtex
