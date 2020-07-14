import json
import re

import feedparser
import requests
from nameparser import HumanName

pmid_url = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={};format=json'


def pmid_formatter(pmid, pmid_base=pmid_url):
    return pmid_base.format(pmid)


def get_pmid_doi(pmid):
    data = requests.get(pmid_formatter(pmid))
    data.raise_for_status()
    data_dict = json.loads(data.text)
    return data_dict['records'][0]['doi']


def get_pmid_bibtex(pmid, short_name=None, lastname_first=True):
    doi = get_pmid_doi(pmid)
    return get_doi_bibtex(doi, short_name=short_name, lastname_first=lastname_first)


doi_url = 'http://dx.doi.org'


def doi_formatter(doi, doi_base=doi_url):
    return '/'.join((doi_base, doi))


def get_doi_bibtex(doi, short_name=None, lastname_first=True):
    # To do, better exception handling on the request
    header = {'Accept': 'application/x-bibtex'}
    data = requests.get(doi_formatter(doi), headers=header)
    data.raise_for_status()
    bibtex = data.text + "\n"
    if lastname_first:
        bibtex = invert_author_names(bibtex)

    is_biorxiv, biorxiv_id = doi_is_biorxiv(doi)
    if is_biorxiv:
        bibtex = fix_biorxiv_info(bibtex, biorxiv_id)
    return replace_short_name(bibtex, short_name)


def invert_author_names(bibtex):
    author_test = re.search("author = {(?P<author_str>.*)}", bibtex)
    author_str_original = author_test.groupdict()['author_str']
    author_str_inverted = parse_authors(author_str_original)
    return bibtex.replace(author_str_original, author_str_inverted)


arxiv_url = "http://export.arxiv.org/api/query"


def get_arxiv_bibtex(arxiv_number, short_name=None, lastname_first=True):
    params = {'id_list': arxiv_number}
    atom_data = requests.get(arxiv_url, params=params)
    data = feedparser.parse(atom_data.text)
    if 'id' in data['entries'][0]:
        bibtex = parse_arxiv_bibtex(data, lastname_first=lastname_first)
    else:
        raise Exception('Arxiv ID not found')
    return replace_short_name(bibtex, short_name)


biorxiv_doi = "10.1101/{bid}"


def biorxiv_doi_formatter(biorxiv_id, biorxiv_base=biorxiv_doi):
    return biorxiv_base.format(bid=biorxiv_id)


def get_biorxiv_bibtex(biorxiv_id, short_name=None, lastname_first=True):
    bibtex = get_doi_bibtex(biorxiv_doi_formatter(biorxiv_id),
                            short_name=short_name,
                            lastname_first=lastname_first)
    return bibtex


def fix_biorxiv_info(bibtex, biorxiv_id):
    biorxiv_info = "\teprinttype={{bioRxiv}},\n" \
                   "\teprint={{{bid}}},\n" \
                   "\thowpublished={{{hp}}}\n}}\n".format(bid=biorxiv_id,
                                                          hp='bioRxiv doi:10.1101/{}'.format(biorxiv_id))
    bibtex = bibtex.replace('@article{', '@online{', 1)
    return bibtex[:-3] + ',\n' + biorxiv_info


def doi_is_biorxiv(doi):
    biorxiv_regex = r"(?P<doi_prefix>10\.\d{4,}\.?\d*)\/(?P<doi_suffix>.*)"
    biorxiv_doi_test = re.search(biorxiv_regex, doi)
    if (biorxiv_doi_test.groupdict()['doi_prefix'] == '10.1101') and \
        (re.match(r'^\d*$', biorxiv_doi_test.groupdict()['doi_suffix']) is not None):
        return True, biorxiv_doi_test.groupdict()['doi_suffix']
    else:
        return False, None


def replace_short_name(bibtex, short_name):
    if short_name is not None:
        oldreg = re.search('^@.*{(?P<old_name>.*),', bibtex)
        old_name = oldreg.groupdict()['old_name']
        bibtex = bibtex.replace(old_name, short_name, 1)
    return bibtex


def parse_authors(authors, lastname_first=True):
    if isinstance(authors, list):
        author_list = authors
    elif isinstance(authors, str):
        author_list = authors.split(' and ')
    else:
        raise ValueError

    name_list = [HumanName(author) for author in author_list]
    last_names = []
    first_names = []
    for name in name_list:
        if len(name.suffix) > 0:
            last_names.append('{l} {s}'.format(l=name.last, s=name.suffix))
        else:
            last_names.append('{l}'.format(l=name.last))
        if len(name.middle) > 0:
            first_names.append('{f} {m}'.format(f=name.first, m=name.middle))
        else:
            first_names.append('{f}'.format(f=name.first))
    if lastname_first:
        name_str = ' and '.join(['{}, {}'.format(*name) for name in zip(last_names, first_names)])
    else:
        name_str = ' and '.join(['{} {}'.format(*name) for name in zip(first_names, last_names)])
    return name_str


month_map = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}


def format_bibtex_entry(short_name,
                        authors,
                        title,
                        year,
                        month,
                        eprinttype,
                        eprint,
                        article_url):
    bibtex_header = '@online{'
    bibtex_base = "{header}{short_name},\n" \
                  "\tauthor = {{{authors}}},\n" \
                  "\ttitle = {{{title}}},\n" \
                  "\tyear = {{{year}}},\n" \
                  "\tmonth = {{{month}}},\n" \
                  "\teprinttype = {{{eprinttype}}},\n" \
                  "\teprint = {{{eprint}}},\n" \
                  "\thowpublished = {{{how_published}}},\n" \
                  "\turl = {{{url}}}\n}}\n"
    bibtex = bibtex_base.format(header=bibtex_header,
                                short_name=short_name,
                                authors=authors,
                                title=title,
                                year=year,
                                month=month,
                                eprinttype=eprinttype,
                                eprint=eprint,
                                how_published=':'.join((eprinttype, eprint)),
                                url=article_url)
    return bibtex


def parse_arxiv_bibtex(data, lastname_first=True):
    # todo: exceptions versioning
    ind = 0

    title = data['entries'][ind]['title']

    eprinttype = 'arXiv'
    id_parser = re.search('http://arxiv.org/abs/(?P<id_str>.*)', data['entries'][ind]['id'])
    eprint = id_parser.groupdict()['id_str']

    author_list = [author['name'] for author in data['entries'][ind]['authors']]
    authors = parse_authors(author_list, lastname_first=lastname_first)

    year = data['entries'][ind]['published_parsed'].tm_year
    month = month_map[data['entries'][ind]['published_parsed'].tm_mon]

    article_url = data['entries'][0]['link']

    first_author = HumanName(author_list[0])
    if len(first_author.suffix) > 0:
        default_short_name = '_'.join((first_author.last.replace(' ', "_"),
                                       first_author.middle.replace(' ', "_"),
                                       str(year)))
    else:
        default_short_name = '_'.join((first_author.last.replace(' ', "_"),
                                       str(year)))

    bibtex = format_bibtex_entry(default_short_name,
                                 authors,
                                 title,
                                 year,
                                 month,
                                 eprinttype,
                                 eprint,
                                 article_url)
    return bibtex
