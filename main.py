import argparse
import json
import csv
import random
import re

from faker import Faker

import conf


def main():
    parser = create_parser()
    args = parser.parse_args()
    my_gen_book = generate_book(args)
    book_list = []
    for i in range(args.count):
        book_list.append(next(my_gen_book))
    if args.output == 'json':
        to_json(book_list, args.filename, args.indent)
        print(f"Output saved to {args.filename}...")
    elif args.output == 'csv':
        to_csv(book_list, args.filename, args.v_separator, args.l_separator)
        print(f"Output saved to {args.filename}...")
    else:
        for book in book_list:
            print(book)


def to_csv(obj: list, filename: str, v_sep: str, l_sep: str):
    """
    Function outputs given iterable object to csv file
    :param obj: Iterable object to dump to csv file
    :param filename: Iterable object to dump to csv file
    :param v_sep: Symbol to use as value separator
    :param l_sep: Symbol to use as line separator
    :return:
    """
    with open(filename, 'w', encoding="utf-8") as csv_file:
        book_writer = csv.writer(csv_file, delimiter=v_sep, lineterminator=l_sep, quoting=csv.QUOTE_MINIMAL)
        for book in obj:
            for key, value in book.items():
                book_writer.writerow([key, value])


def to_json(obj: list, filename: str, dent: int):
    """
    Function outputs given iterable object to json file
    :param obj: Iterable object to dump to json file
    :param filename: Name of the json file
    :param dent: Indent to json formatting, default 0 symbols
    :return: None
    """
    with open(filename, 'w', encoding="utf-8") as json_file:
        json.dump(obj, json_file, indent=dent, ensure_ascii=False)


def create_parser():
    """
    Command line parser initialization
    :return: Parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("count", help="Number of books to generate", type=int)
    parser.add_argument("-a", "--authors", help="Authors per book", type=int, default=-1)
    parser.add_argument("-s", "--sale", help="Sale percentage(0-100)", type=int, default=-1)

    subparsers = parser.add_subparsers(dest="output", required=False)

    json_parser = subparsers.add_parser("json", help="Output books to json file")
    json_parser.add_argument("-f", "--filename", help="JSON file name", default="cancer.json")
    json_parser.add_argument("-i", "--indent", help="JSON formatting indent", type=int, default=0)

    csv_parser = subparsers.add_parser("csv", help="Output books to csv file")
    csv_parser.add_argument("-f", "--filename", help="CSV file name", default="cancer.csv")
    csv_parser.add_argument("-v", "--v_separator", help="CSV value separator", default=",")
    csv_parser.add_argument("-l", "--l_separator", help="CSV line separator", default="\n")

    return parser


def fetch_title() -> str:
    """
    Fetching the title for a book
    :return: random title from file, filename set by BOOK_TITLES
    """
    with open(conf.BOOK_TITLES, encoding="utf-8") as titles:
        title_list = titles.readlines()
    title_list = [line.strip("\n") for line in title_list]
    size = len(title_list)
    title = title_list[random.randrange(size)]
    return title


def check_name_file(name_list: list):
    """
    Checking the name file for correct layout
    :param name_list: Contents of the file
    :return: None or raises the Exception(ValueError)
    """
    for line in name_list:
        a = re.fullmatch("[A-ZА-Я][a-zа-я]+? [A-ZА-Я][a-zа-я]+", line)
        if a is None:
            raise Exception(ValueError)


def fetch_authors(num: int) -> list:
    """
    Fetching authors for the book
    :param num: Amount of authors the book would have
    :return: List of names from the file, filename set by AUTHORS
    """
    with open(conf.AUTHORS, encoding="utf-8") as names:
        name_list = names.readlines()
    name_list = [line.strip() for line in name_list]

    size = len(name_list)
    author_names = []
    for i in range(num):
        author_names.append(name_list[random.randrange(size)])
    return author_names


def generate_book(args) -> dict:
    """
    Generator for a fake book
    :param args: command line arguments
    :return: Dict Object, containing a new fake book
    """
    pk = 0
    fake = Faker()
    Faker.seed(0)
    while True:
        amt_authors = args.authors if args.authors != -1 else random.randint(1, 3)
        sale = args.sale if args.sale != -1 else random.randint(0, 100)
        pk += 1
        fields = {
            "title": fetch_title(),
            "year": random.randint(1800, 2020),
            "pages": random.randint(100, 500),
            "isbn13": fake.isbn13(),
            "rating": random.randint(0, 5),
            "price": round(random.random()*500, 2),
            "discount": sale,
            "author": fetch_authors(amt_authors)
        }
        new_book = {
            "model": conf.MODEL,
            "pk": pk,
            "fields": fields,
        }

        yield new_book


if __name__ == '__main__':
    main()
