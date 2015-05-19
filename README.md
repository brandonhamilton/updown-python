# Updown

A Python wrapper and CLI for the [updown.io](https://updown.io) API

## Installation

Install from PyPI:

    pip install updown

Or install using the provided  `setup.py`:

    python setup.py install

## Usage

#### Import library

    import updown
    updown.API_KEY = 'YOUR API KEY'

Or set the `UPDOWN_API_KEY` environment variable

Find your API key in your [settings page](https://updown.io/settings/edit).

#### List all your checks
    checks = updown.checks()

#### List downtimes for a specific check (paginated, 100 per call)
    updown.checks()['http://myurl'].downtimes()
    updown.checks()['http://myurl'].downtimes(page=2)

#### Update a check
    c = updown.checks()['http://myurl']
    c.enabled = False
    c.sync()

#### Create a new check
    c = updown.add('http://myurl')

#### Delete a check
    c = updown.checks()['http://myurl'].delete()