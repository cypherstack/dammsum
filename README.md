# DammSum: efficient mnemonic seeds from quasigroup checksums

This respository contains a technical note and proof-of-concept code for a mnemonic seed generation technique related to research performed by [Cypher Stack](https://cypherstack.com) for Slaz Labs.


## Requirements

The technical note requires a suitable [LaTeX](https://www.latex-project.org/) distribution, along with an assortment of packages.

The code requires an active [Python 3 release](https://devguide.python.org/#status-of-python-branches).


## Testing

### Technical note

Testing for the technical note is done by a workflow in this repository that builds the note and checks for errors and certain warnings.
You can view the resulting PDF as a build artifact.

[![Build status](../../actions/workflows/build.yml/badge.svg)](../../actions/workflows/build.yml)

### Code

Testing for the code is done by a workflow in this repository that runs the test suite against all active Python 3 release minor versions.

[![Test status](../../actions/workflows/test.yml/badge.svg)](../../actions/workflows/test.yml)
