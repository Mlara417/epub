# Epub CLI

A command-line tool to manage epub files. Epub CLI simplifies ebook management.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Commands](#commands)
  - [Examples](#examples)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Add covers to epubs.
- Easily extendable to add more ebook management features.

## Installation

To install the Epub CLI tool, use the following commands:

```bash
# Clone the repository
git clone https://github.com/yourusername/epub-cli.git
cd epub-cli
```

### Install in editable mode

```bash
pip install -e .
```

## Usage

After installing, you can use the CLI by typing `epub` in your terminal. Below are the main commands and options available.

### Commands

### edit

Argument with subcommands used to edit the epub.

#### `cover`

Update cover to an epub directory.

```bash
epub edit cover EPUB_PATH COVER_PATH [OPTIONS]
```

#### Args

- EPUB_PATH: path to book.epub.
- COVER_PATH: path to cover.jpg.

## Examples

```bash
epub edit cover "../book.epub" "../code.jpg"
```

## Configuration

### `setup`

Unzips epub file into a folder called epub-unzipped in repo root.

```bash
epub setup workspace
```

## Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b branch-name`)
3. Make Changes
4. Commit changes (`git commit -m "Add a change"`).
5. Push to branch (`git push origin branch-name`).
6. Open Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
