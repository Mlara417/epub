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

- Add cover to epub.
- Easily extendable to add more ebook management features.

## Installation

To install the Epub CLI tool, use the following commands:

```bash
# Clone the repository
git clone https://github.com/Mlara417/epub.git
cd epub
```

### Install in editable mode

```bash
pip install -e .
```

### Setup epub workspace

```bash
# Setup epub workspace
epub setup /path/to/epub/file
```

## Usage

After installing, you can use the CLI by typing `epub` in your terminal. Below are the main commands and options available.

### Commands

### edit

Argument with subcommands used to edit the epub.

#### `cover`

Update cover to an epub directory.

```bash
epub edit cover COVER_PATH WORKSPACE(default="epub-unzipped")
```

#### Args

- COVER_PATH: path to cover.jpg.
- WORKSPACE: path to unzipped epub file.

## Examples

```bash
epub edit cover "../code.jpg"
```

## Configuration

### `setup`

Unzips epub file into a folder called epub-unzipped in repo root which will be used as workspace.

```bash
epub setup EPUB_PATH
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
