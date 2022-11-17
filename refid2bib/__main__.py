from refid2bib import refid2bib


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('document_id', help='DOI, ArXiv ID, etc. of the document you wish to look up')
    args = parser.parse_args()

    print(refid2bib(args.document_id))
