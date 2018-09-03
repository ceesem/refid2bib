import sys
from refid2bib import refid2bib

oid = sys.argv[1]
print( '\n')
print( refid2bib(oid) )
