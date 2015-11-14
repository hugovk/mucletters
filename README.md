# MUC letters

![heart](/output/favicon.ico?raw=true) My second [NaNoGenMo 2015 entry](https://github.com/dariusk/NaNoGenMo-2015) is an epistolary novel of love letters (and the second entry inspired by [D004x](https://www.edx.org/course/electronic-literature-davidsonx-d004x
)).

![405 Love Letters](/output/snippet1.png?raw=true "405 Love Letters")

 * [HTML](https://hugovk.github.io/mucletters/output/mucletters.html)
 * [PDF](https://hugovk.github.io/mucletters/output/mucletters.pdf)
 * [code](mucletters.py)

![heart](/output/favicon.ico?raw=true) Christopher Strachey has been named the first digital artist; the first to make literary or artistic use of a computer.

![heart](/output/favicon.ico?raw=true) A colleague of Alan Turing, in 1952 Strachey was a programmer of the world's first commercially available general-purpose electronic computer, the Ferranti Mark 1, also known as the Manchester University Computer.

![heart](/output/favicon.ico?raw=true) According to [by Noah Wardrip-Fruin](https://grandtextauto.soe.ucsc.edu/2005/08/01/christopher-strachey-first-digital-artist/):

> Christopher Strachey is rightly viewed as a pioneer of modern computing. He’s not usually, however, viewed as the creator of the first work of digital literature. Research toward my submission for DAC, however, has lead me to believe that he was — and that his initial digital literature project was also, quite probably, the first piece of digital art.

> ...

> That [1952] summer he developed — with some aesthetic advice from his sister Barbara, using Turing’s random number generator, and perhaps in collaboration with Turing — a Mark I program that created combinatory love letters. This was the first piece of digital literature, and of digital art, predating by a decade the earliest examples of digital computer art from recent surveys (e.g., quite useful books such as Christiane Paul’s *Digital Art* and Stephen Wilson’s *Information Arts*).

![heart](/output/favicon.ico?raw=true) Strachey described the love letters in a 1954 article entitled The "Thinking" Machine, published in the literary journal [*Encounter*](http://www.unz.org/Pub/Encounter-1954oct-00025):

> IN SPITE of a certain impression of rather
Victorian Babu, I think there is very little
doubt of the intention of these letters:

> *Darling Sweetheart
You are my avid fellow tiding. My affection
curiously clings to your passionate wish. My liking
yearns for ),our heart. You are my wistful sympathy:
my tender liking.
Yours beautifully
M.U.C.*

> *Honey Dear
My sympathetic affection beautifully attracts your
affectionate enthusiasm. You are my loving adoration:
my breathless adoration. My fellow feeling
breathlessly hopes for your dear eagerness. My
lovesick adoration cherishes your avid ardour.
Yours wistfully
M.U.C.*

> The Manchester University Computer (hence
the irreverent signature) can type out letters
like this at the rate of about one a minute for
hours without ever repeating itself. The scheme
on which it works, however, is almost
childishly simple. Apart from the beginning and
the ending of the letters, there are only two
basic types of sentence. The first is "*My* —
(adj.) ~ (noun) — (adv.) — (verb) *your* —
 (adj.) ~ (noun)." There are lists
appropriate adjectives, nouns, adverbs, and
verbs from which the blanks are filled in at
random. There is also a further random choice
as to whether or not the adjectives and adverb
are included at all. The second type is simply
"*You are my* — (adj.) — (noun)," and
this case the adjective is always present. There
is a random choice of which type of sentence is
to be used, but if there are two consecutive
sentences of the second type, the first ends with
a colon (unfortunately the teleprinter of the
computer had no comma) and the initial "*You
are*" of the second is omitted. The letter starts
with two words chosen from special lists ; there
are then five sentences of one of the two basic
types, and the letter ends "*Yours* — (adv.)
M. U. C."

> There are many obvious imperfections in
this scheme (indeed very little thought went
into its devising) and the fact that the vocabulary
was largely based on Roget’s Thesaurus
lends a very peculiar flavour to the results. The
chief point of interest, however, is not the
obvious crudity of the scheme, nor even in
ways in which it might be improved, but in the
remarkable simplicity of the plan when compared
with the diversity of the letters it produces.
It is clear that these letters are produced by a
rather simple trick and that the computer is not
really "thinking" at all. This is true of all
programs which make the computer appear
to think; on analysis they are nothing more
than rather complicated tricks. However,
sometimes these tricks can lead to quite unexpected
and interesting results.

![heart](/output/favicon.ico?raw=true) Using Strachey's description, I reimplemented his love-letter generator in Python (using the word lists from this [PHP version](http://www.gingerbeardman.com/loveletter/).

![DARLING MOPPET](/output/snippet2.png?raw=true "DARLING MOPPET")

![heart](/output/favicon.ico?raw=true) Running on a Macbook Pro, it can generate some half a million per minute, compared with Manchester University Computer's rate of one per minute. (Well, this isn't quite a fair comparison: the MUC outputted to paper whereas the MBP just saved to disk.)

![DARLING CHICKPEA](/output/snippet3.png?raw=true "DARLING CHICKPEA")

![heart](/output/favicon.ico?raw=true) My NaNoGenMo entry goes further: it starts out as simple five-line love letters following Strachey. But as the pages turn, the letters become more and more absurd as more and more words are instead taken at random from the [Wordnik dictionary](http://developer.wordnik.com/docs.html). And towards the middle of the book the letters become longer, up to 120 lines long, before settling back down to five lines at the end.

![All victorious night-line](/output/snippet4.png?raw=true "All victorious night-line")

![heart](/output/favicon.ico?raw=true) In the HTML version, clicking a word takes you to another letter containing that word.

![heart](/output/favicon.ico?raw=true)
