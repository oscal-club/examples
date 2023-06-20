# SSDF Excel to OSCAL JSON Catalog Transformer

This utility takes the current NIST SP 800-218 Secure Software Development Framework's practices [provided in a Microsoft Excel file by its authors](https://csrc.nist.gov/publications/detail/sp/800-218/final) into a valid [OSCAL JSON catalog](https://pages.nist.gov/OSCAL/reference/latest/catalog/json-outline/) instance.

## Installation

This utility uses Python 3.x and the poetry dependency management tool to install jinja2, openpyxl, and their transitive dependencies.

```sh
$ python3 -m poetry install
```

## Operation

To convert NIST's official Microsoft Excel spreadsheet into an OSCAL JSON catalog, perform the installation steps above and execute the following commands.

```sh
$ python3 -m poetry shell
$ transform.py -i NIST.SP.800-218.SSDF-table.xlsx -o ssdf.oscal.json
```

To convert the JSON into additional OSCAL catalog formats (i.e. XML, YAML), you can subsequently use NIST's reference implementation, the [`oscal-cli`](https://github.com/usnistgov/oscal-cli).

```sh
$ oscal-cli catalog validate ssdf.oscal.json
The file '/home/al/Code/oc_examples/src/gov/nist/ssdf/ssdf.oscal.json' is valid.
$ oscal-cli catalog convert ssdf.oscal.json --to=yaml | tee ssdf.oscal.yaml
$ oscal-cli catalog convert ssdf.oscal.json --to=xml | tee ssdf.oscal.xml
```

A copy of the JSON, YAML, and XML catalogs will be provided as a convenience to community members.
