#!/usr/bin/env python
# encoding: utf-8
"""
Generate an epistolary novel of love letters for NaNoGenMo 2015,
inspired by and extending Christopher Strachey's 1952 program for the
world's first commercially available general-purpose electronic computer.

Simple usage, for a single love letter:
python mucletters.py

To create a NaNoGenMo novel:
python mucletters.py --link --html --nanogenmo -v mixed > mucletters.html

"""
from __future__ import print_function, unicode_literals
# from pprint import pprint
import argparse
import random
import re
import sys
import yaml  # pip install pyaml
from wordnik import swagger, WordsApi  # pip install wordnik


# "Apart from the beginning and the ending of the letters, there are only
# two basic types of sentence. The first is “My — (adj.) — (noun)
# — (adv.) — (verb) your — (adj.) — (noun).” There are lists of
# appropriate adjectives, nouns, adverbs, and verbs from which the blanks
# are filled in at random. There is also a further random choice as to
# whether or not the adjectives and adverb are included at all. The second
# type is simply “You are my — (adj.) — (noun),” and in this case
# the adjective is always present. There is a random choice of which type
# of sentence is to be used, but if there are two consecutive sentences of
# the second type, the first ends with a colon (unfortunately the
# teleprinter of the computer had no comma) and the initial “You are”
# of the second is omitted. The letter starts with two words chosen from
# the special lists; there are then five sentences of one of the two basic
# types, and the letter ends “Yours — (adv.) M. U. C.”"
#
# Christopher Strachey in Enounter (1954)
#
# http://www.unz.org/Pub/Encounter-1954oct-00025
# https://grandtextauto.soe.ucsc.edu/2005/08/01/
# http://www.gingerbeardman.com/loveletter/


SALUTATIONS1 = [
    "BELOVED",
    "DARLING",
    "DEAR",
    "DEAREST",
    "FANCIFUL",
    "HONEY"]

SALUTATIONS2 = [
    "CHICKPEA",
    "DEAR",
    "DUCK",
    "JEWEL",
    "LOVE",
    "MOPPET",
    "SWEETHEART"]

ADJECTIVES = [
    "AFFECTIONATE",
    "AMOROUS",
    "ANXIOUS",
    "AVID",
    "BEAUTIFUL",
    "BREATHLESS",
    "BURNING",
    "COVETOUS",
    "CRAVING",
    "CURIOUS",
    "EAGER",
    "FERVENT",
    "FONDEST",
    "LOVEABLE",
    "LOVESICK",
    "LOVING",
    "PASSIONATE",
    "PRECIOUS",
    "SEDUCTIVE",
    "SWEET",
    "SYMPATHETIC",
    "TENDER",
    "UNSATISFIED",
    "WINNING",
    "WISTFUL"]

NOUNS = [
    "ADORATION",
    "AFFECTION",
    "AMBITION",
    "APPETITE",
    "ARDOUR",
    "BEING",
    "BURNING",
    "CHARM",
    "CRAVING",
    "DESIRE",
    "DEVOTION",
    "EAGERNESS",
    "ENCHANTMENT",
    "ENTHUSIASM",
    "FANCY",
    "FELLOW FEELING",
    "FERVOUR",
    "FONDNESS",
    "HEART",
    "HUNGER",
    "INFATUATION",
    "LITTLE LIKING",
    "LONGING",
    "LOVE",
    "LUST",
    "PASSION",
    "RAPTURE",
    "SYMPATHY",
    "THIRST",
    "WISH",
    "YEARNING"]

ADVERBS = [
    "AFFECTIONATELY",
    "ARDENTLY",
    "ANXIOUSLY",
    "BEAUTIFULLY",
    "BURNINGLY",
    "COVETOUSLY",
    "CURIOUSLY",
    "EAGERLY",
    "FERVENTLY",
    "FONDLY",
    "IMPATIENTLY",
    "KEENLY",
    "LOVINGLY",
    "PASSIONATELY",
    "SEDUCTIVELY",
    "TENDERLY",
    "WISTFULLY"]

VERBS = [
    "ADORES",
    "ATTRACTS",
    "CLINGS TO",
    "HOLDS DEAR",
    "HOPES FOR",
    "HUNGERS FOR",
    "LIKES",
    "LONGS FOR",
    "LOVES",
    "LUSTS AFTER",
    "PANTS FOR",
    "PINES FOR",
    "SIGHS FOR",
    "TEMPTS",
    "THIRSTS FOR",
    "TREASURES",
    "YEARNS FOR",
    "WOOS"]


big_dict_of_all_the_random_words = {}


def logit(*log_args):
    if args.log:
        print(' '.join(map(str, log_args)))


def log_html(html):
    if args.html and args.log:
        print(html)


def print_html(html):
    if args.html:
        print(html)


def load_yaml(filename):
    """
    File should contain:
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'wordnik_api_key'}:
        sys.exit("Wordnik credentials missing from YAML: " + filename)
    return data


def get_random_words_from_wordnik(part_of_speech):
    """ Get a random word from Wordnik """
    words = words_api.getRandomWords(includePartOfSpeech=part_of_speech,
                                     limit=1000)

    random_words = []
    for word in words:
        random_words.append(word.word)
#     logit("Random " + part_of_speech + ": " + word)
    return random_words


def strip_tags(text):
    """Strip HTML tags"""
    return re.sub('<[^<]+?>', '', text)


def count_words(text):
    count = len(strip_tags(text).split())
    logit(count, "words")
    return count


def upperfirst(x):
    return x[0].upper() + x[1:]


def taggy(text, class_name):
    """Wrap in HTML tags?"""
    if args.html:
        return '<span class="{0}">{1}</span>'.format(class_name, text)
    else:
        return text


def commafy(value):
    """Add thousands commas"""
    return "{:,}".format(value)


def list_selector(original_list, wordnik_list, upper_first=False):

    if args.vocabulary != "original":
        # Do Wordnik lists need topping up?
        check_wordnik_lists()

    class_name = "w"
    if args.vocabulary == "original":
        output = random.choice(original_list)
        class_name = "o"
    elif args.vocabulary == "wordnik":
        output = random.choice(wordnik_list)
    else:  # mixed
        if percent_chance(chance_of_original):
            output = random.choice(original_list)
            class_name = "o"
        else:
            if percent_chance(20):
                # remove from list
                output = wordnik_list.pop()
            else:
                # leave in list
                output = random.choice(wordnik_list)

    try:
        big_dict_of_all_the_random_words[output] += 1
    except KeyError:
        big_dict_of_all_the_random_words[output] = 1

    if upper_first:
        output = upperfirst(output)
    return taggy(output, class_name)


def random_salutation1():
    return list_selector(SALUTATIONS1, wordnik_adjectives, upper_first=True)


def random_salutation2():
    return list_selector(SALUTATIONS2, wordnik_nouns)


def adj():
    return list_selector(ADJECTIVES, wordnik_adjectives)


def noun():
    return list_selector(NOUNS, wordnik_nouns)


def adv():
    return list_selector(ADVERBS, wordnik_adverbs)


def verb():
    return list_selector(VERBS, wordnik_verbs)


def percent_chance(percent):
    return random.random() < percent / 100.0


def muc_sentences(number_of_sentences):
    first_type_template_with = "My {0} {1} {2} {3} your {4} {5}. "
    first_type_template_without = "My {0} {1} your {2}. "
    second_type_template_with = "You are my {0} {1}. "
    second_type_template_without = "my {0} {1}. "
    sentences = []
    sentence_types = []
    number_of_consecutive_sentences_of_the_second_type = 0
    while len(sentences) < number_of_sentences:

        if percent_chance(50):
            sentence_type = 1
            if percent_chance(50):
                sentence = first_type_template_with.format(
                    adj(), noun(), adv(), verb(), adj(), noun())
            else:
                sentence = first_type_template_without.format(
                    noun(), verb(), noun())

        else:
            sentence_type = 2
            number_of_consecutive_sentences_of_the_second_type += 1
            if sentence_types and sentence_types[-1] == 2:
                # Replace previous sentence's full-stop with a comma
                sentences[-1] = sentences[-1][:-2] + ", "

                sentence = second_type_template_without.format(adj(), noun())
            else:
                sentence = second_type_template_with.format(adj(), noun())

        sentences.append(sentence)
        sentence_types.append(sentence_type)

    if len(sentences) > 20:
        for i, sentence in enumerate(sentences):
            if percent_chance(10):
                sentences[i] += "\n\n"

    # logit(sentence_types)
    # logit(sentences)
    return sentences


def muc(number_of_sentences=5):
    start = random_salutation1() + " " + random_salutation2() + ",\n\n"
    end = "\n\nYours {0},\n\nM. U. C.".format(adv())

    sentences = muc_sentences(number_of_sentences)

    letter = []
    letter.append(start)
    letter.extend(sentences)
    letter.append(end)

    return "".join(letter)


def check_wordnik_list(wordnik_list, part_of_speech):
    if len(wordnik_list) < 30:
        top_up = get_random_words_from_wordnik(part_of_speech)
        wordnik_list.extend(top_up)
    return wordnik_list


def check_wordnik_lists():
    global wordnik_adjectives
    global wordnik_nouns
    global wordnik_adverbs
    global wordnik_verbs
    wordnik_adjectives = check_wordnik_list(wordnik_adjectives, "adjective")
    wordnik_nouns = check_wordnik_list(wordnik_nouns, "noun")
    wordnik_adverbs = check_wordnik_list(wordnik_adverbs, "adverb")
    wordnik_verbs = check_wordnik_list(wordnik_verbs, "verb")


def this_file():
    return open(__file__).read()


def link_words_randomly(text):
    """Link words randomly to other occurences of the same word"""

    global big_dict_of_all_the_random_words

    # Remove all entries with only one occurence
    big_dict_of_all_the_random_words = {
        k: v for k, v in big_dict_of_all_the_random_words.items() if v > 1}

    for word, tally in big_dict_of_all_the_random_words.items():
        ids = range(tally)
        hrefs = list(ids)
        while ids == hrefs:  # make sure different
            random.shuffle(ids)
            random.shuffle(hrefs)

        old = '">{0}</span>'.format(word)

        for i in range(tally):
            id = ids.pop()
            href = hrefs.pop()

            # For example: ">BEAUTIFUL</span> -> "><a ...>BEAUTIFUL</a></span>
            new = '"><a id="{0}{1}" href="#{0}{2}">{0}</a></span>'.format(
                word, id, href)

            # Slow (~1m08s):
            text = text.replace(old, new, 1)

            # Even slower (~1m31s):
#             index = text.find(old, index)
#             old_len = len(old)
#             text = text[:index] + new + text[index+old_len:]

    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an epistolary novel of love letters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-n', '--number',
        type=int, default=5,
        help="Number of middle sentences")
    parser.add_argument(
        '--nanogenmo', action='store_true',
        help="Create a NaNoGenMo novel")
    parser.add_argument(
        '-m', '--minwords',
        type=int, default=50000,
        help="Minimum number of words of the full work")
    parser.add_argument(
        '-v', '--vocabulary',
        choices=('original', 'wordnik', 'mixed'),
        help="Vocabulary to use", default='original')
    parser.add_argument(
        '--link', action='store_true',
        help="Link words randomly to other occurences of the same word (slow)")
    parser.add_argument(
        '--html', action='store_true',
        help="HTML tags for formatting")
    parser.add_argument(
        '-l', '--log', action='store_true',
        help="Log some extra stuff")
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/mucletters.yaml',
        # default='M:/bin/data/mucletters.yaml',
        help="YAML file location containing Wordnik token")
    args = parser.parse_args()

    words_api = None
    wordnik_adjectives = []
    wordnik_nouns = []
    wordnik_adverbs = []
    wordnik_verbs = []

# "The Manchester University Computer (hence the irreverent signature) can type
# out letters like this at the rate of about one a minute for hours without
# ever repeating itself."
# The Macbook Pro can pump out 100,000 in 0m11.868s = 505,561/min

    # Example of the simplest use of original algorithm:
    if not args.nanogenmo:
        letter = muc(args.number)
        print(letter)
        print()
        print(len(letter), "chars")
        print(count_words(letter), "words")
        sys.exit()

    if args.vocabulary != "original":
        credentials = load_yaml(args.yaml)
        wordnik_client = swagger.ApiClient(credentials['wordnik_api_key'],
                                           'http://api.wordnik.com/v4')
        words_api = WordsApi.WordsApi(wordnik_client)

        wordnik_adjectives = get_random_words_from_wordnik("adjective")
        wordnik_nouns = get_random_words_from_wordnik("noun")
        wordnik_adverbs = get_random_words_from_wordnik("adverb")
        wordnik_verbs = get_random_words_from_wordnik("verb")

    print_html('''
<html>
<head>
  <meta charset="utf-8" />
  <title>MUC letters - NaNoGenMo2015</title>
  <link rel="stylesheet" type="text/css" href="mucletters.css">
  <link rel="shortcut icon" type="image/ico" href="favicon.ico"/>
</head>
<body>
''')

    number_of_words = 0
    full_piece = []

    while number_of_words < args.minwords:

        # Degenerates toward 0 as we progress towards minwords
        percent_complete = 100 * float(number_of_words) / args.minwords
        chance_of_original = 100 - percent_complete

        # first is 100% original, but let's try and get more mix from second
        if chance_of_original < 100:
            chance_of_original = min(chance_of_original, 95)

        # How many lines per letter?
        # Let's peak at 250 half-way through;
        # but we pick a random number between 5 and
        # the theoretical maximum at any point:
        # 0 to 25k to 50k
        # 5 to 100 to 5

        # how far from half way?
        centre = args.minwords/2
        dist_from_centre = abs(centre - number_of_words)
        amplitude = float(dist_from_centre) / centre  # 1->0->1

        if args.html:
            total_so_far = len(full_piece)
            if total_so_far % 2:
                odd_even = "even"
            else:
                odd_even = "odd"
            p = '<P class={0}>'.format(odd_even)

        log_html('<span class="meta">')
        logit("chance_of_original", chance_of_original)
        logit("centre", centre)
        logit("dist_from_centre", dist_from_centre)
        logit("amplitude", amplitude)

        max_lines = 120
        number_of_lines = int((1 - amplitude) * max_lines)
        logit("number_of_lines", number_of_lines)
        number_of_lines = random.randint(5, max(5, number_of_lines))
        logit("number_of_lines", number_of_lines)
        log_html('</span>')

        letter = muc(number_of_lines)
        if args.html:
            letter = letter.replace("\n", "<br>\n")
#         print(letter.encode('utf-8'))
#         print()
        log_html('<span class="meta">')
        logit(len(letter), "chars")
        log_html('</span>')

        number_of_words += count_words(letter)
        if args.html:
            letter = p + letter
        full_piece.append(letter)

    print_html('<div class="border even">')
    print('<H1 id="0"><img src="favicon.ico"> ' + str(len(full_piece)) +
          ' Love Letters <img src="favicon.ico"></H1>')
    print("<H2>An epistolary novel for NaNoGenMo</H2>")
    print("<H2>by hugovk and mucletters.py (2015)</H2>")
    print("<H2>after Christopher Strachey and<br>"
          "Manchester University Computer (1952)</H2>")
    print('<H3>' + commafy(number_of_words) + ' words</H3>')
    print_html('</div>')

    big_output = []

    for id, letter in enumerate(full_piece):
        big_output.append('<span id="{0}"></span>'.format(id+1))
        big_output.append(letter)

    big_output = "\n".join(big_output)

    if args.link:
        big_output = link_words_randomly(big_output)

    print(big_output.encode('utf-8'))

    print_html("</body></html>")

# End of file
