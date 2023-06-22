#!/usr/bin/env python3

import argparse
from tabula import read_pdf
from tabulate import tabulate

class CPRTOSCALTransformer:
    def __init__(self, source=None):
        self.source = source

    def load(self, source):
        with open(source) as fd:
            self.data = read(fd)

    def transform(self):
        """Transform the CPRT into an OSCAL JSON catalog."""
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert the NIST SP 800-161 Revision 1 Appendix F controls to OSCAL JSON profiles and catalogs')
    parser.add_argument(
        '-i',
        '--input-file',
        help='Path to the CSF CPRT file.',
        default='cprt_CSF_1_1_0_06-21-2023.json',
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
    transformer = CPRTOSCALTransformer()
    transformer.load(args.input_file)
    transformer.transform()

    if args.output_file:
        transformer.save(args.output_file)
    else:
        print(transformer.oscal_catalog)
