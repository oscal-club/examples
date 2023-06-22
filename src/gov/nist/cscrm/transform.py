#!/usr/bin/env python3

import argparse
from tabula import read_pdf
from tabulate import tabulate

class CyberSupplyChainPDFOSCALTransformer:
    def __init__(self, source=None):
        self.source = source
        self.load_args = {'pages': '169-176'}
        self.data = None

    def load(self, source):
        self.data = read_pdf(source, **self.load_args)
        type(self.data)

    def transform(self):
        """Transform the PDF into an OSCAL JSON catalog."""
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert the NIST SP 800-161 Revision 1 Appendix F controls to OSCAL JSON profiles and catalogs')
    parser.add_argument(
        '-i',
        '--input-file',
        help='Path to the SP 800-161 Revision 1 PDF files',
        default='NIST.SP.800-161r1.pdf',
        dest='input_file',
        required=False
    )
    parser.add_argument(
        '-o',
        '--output-file',
        help='Path intended to save OSCAL JSON catalog file. If not provided print to standard out.',
        type=argparse.FileType('w'),
        dest='output_file',
        required=False
    )
    args = parser.parse_args()
    transformer = CyberSupplyChainPDFOSCALTransformer()
    transformer.load(args.input_file)
    transformer.transform()

    if args.output_file:
        transformer.save(args.output_file)
    else:
        print(transformer.oscal_catalog)
