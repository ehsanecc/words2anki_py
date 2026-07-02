# words2anki_py

A Python tool for converting vocabulary lists into Anki flashcard decks (`.apkg`) automatically.

The project simplifies the process of creating Anki decks by generating cards from plain text word lists and enriching them with additional information such as translations, definitions, examples, images, or pronunciation files depending on the configured sources.

## Features

* Generate Anki `.apkg` packages automatically
* Create cards from simple text files
* Batch process large vocabulary lists
* Support for custom deck names
* Easy integration into scripts and automation workflows
* Fully written in Python

## Installation

Clone the repository:

```bash
git clone https://github.com/ehsanecc/words2anki_py.git
cd words2anki_py
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Place your vocabulary words into a text file:

```text
apple
computer
network
algorithm
```

Run the program:

```bash
python main.py words.txt
```

Example:

```bash
python main.py english_words.txt
```

The generated Anki package (`.apkg`) will be created in the current directory.

## Project Structure

```text
words2anki_py/
├── main.py
├── requirements.txt
├── README.md
└── ...
```

## Example Workflow

1. Create a text file containing one word per line.
2. Run the script.
3. Import the generated `.apkg` file into Anki.
4. Start studying.

## Requirements

* Python 3.9+
* Anki (for importing generated decks)

## Contributing

Pull requests and feature suggestions are welcome.

## License

This project is released under the MIT License.
