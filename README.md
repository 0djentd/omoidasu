![PyPI](https://img.shields.io/pypi/v/omoidasu)
![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/0djentd/omoidasu?include_prereleases)
![GitHub all releases](https://img.shields.io/github/downloads/0djentd/omoidasu/total)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/omoidasu)

![GitHub issues](https://img.shields.io/github/issues/0djentd/omoidasu)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/0djentd/omoidasu)
![GitHub Repo stars](https://img.shields.io/github/stars/0djentd/omoidasu?style=social)

[![Python package](https://github.com/0djentd/omoidasu/actions/workflows/python-package.yml/badge.svg)](https://github.com/0djentd/omoidasu/actions/workflows/python-package.yml)
[![Pylint](https://github.com/0djentd/omoidasu/actions/workflows/pylint.yml/badge.svg)](https://github.com/0djentd/omoidasu/actions/workflows/pylint.yml)

# omoidasu

### Description

CLI flashcards tool.

### Installation

```
pip install omoidasu
```

### How to use
```
Usage: omoidasu [OPTIONS] COMMAND [ARGS]...

  CLI for Omoidasu.

Options:
  --data-dir TEXT                 Data directory.
  --config-dir TEXT               Config directory.
  --cache-dir TEXT                Cache directory.
  --state-dir TEXT                State directory.
  --log-dir TEXT                  Log directory.
  --flashcards-dir TEXT           Flashcards directory.
  --verbose / --no-verbose        Show additional information.
  --interactive / --no-interactive
                                  Use interactive features.
  --debug / --no-debug            Show debug information.
  --help                          Show this message and exit.

Commands:
  add     Add cards interactively using text editor.
  list    Writes all cards to stdout.
  new     Add card.
  review  Review all cards.
```

```
Usage: omoidasu list [OPTIONS] REGULAR_EXPRESSION

  Writes all cards to stdout.

Options:
  --max-cards INTEGER  Max number of cards to list.
  --help               Show this message and exit.
```

```
Usage: omoidasu review [OPTIONS] REGULAR_EXPRESSION

  Review all cards.

Options:
  --max-cards INTEGER  Max number of cards to review.
  --help               Show this message and exit.
```

```
Usage: omoidasu add [OPTIONS]

  Add cards interactively using text editor. Save empty file to finish adding
  cards.

Options:
  --editor TEXT
  --help         Show this message and exit.
```

```
Usage: omoidasu new [OPTIONS] [SIDES]...

  Add card.

Options:
  --help  Show this message and exit.
```

