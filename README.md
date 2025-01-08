# Project Title

![Project Screenshot](https://github.com/kapellos/lnksmuggler/LNKSmuggler.png)

A Python script for creating `.lnk` (shortcut) files with embedded encoded data and packaging them into ZIP archives. The resulting LNK file extracts the embedded files and executes the first file provided (so it can be used with AppDomainManager technique) effectivelly bypassing MOTW and the download of files over the Internet. Before the embedded file is executed the LNK opens up a Decoy URL for the user. Idea originated from Balliskit author @EmericNasi(https://github.com/sevagas/Advanced_Initial_access_in_2024_OffensiveX/blob/main/breach_the_gates_extended.pdf)

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## About the Project

This project automates the creation of Windows shortcut (`.lnk`) files containing embedded data and custom commands. It is designed to be used as a ZIP archive to downloaded in a Phishing Campaign.

### Built With

- Python
- Standard libraries: `tarfile`, `base64`, `os`, `sys`, `zipfile`
- External libraries: `pywin32`, `pyfiglet`

---

## Features

- Create `.lnk` shortcut files with:
  - Obfuscated commands.
  - Embedded Base64-encoded tarball data.
- Extract and append data to shortcuts at runtime.
- Package the generated shortcuts into ZIP archives.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kapellos/lnksmuggler.git
    cd lnksmuggler
    ```

2. Install dependencies:

    ```bash
    pip install pywin32 pyfiglet
    ```

---

## Usage

Run the script with the following command:

```bash
python3 script.py <lnk_name> <decoy_url> <file1> <file2> ...
```

### Arguments

- `lnk_name`: The name of the `.lnk` file to create.
- `decoy_url`: The URL to open when the shortcut is executed.
- `file1`, `file2`, ...: List of files to encode and embed in the shortcut.

### Example

```bash
python script.py example.lnk "https://example.com" file1.txt file2.exe
```


## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Credits
- EmericNasi [https://www.linkedin.com/in/emeric-nasi-84950528/]
