from build_data import build_signs_and_transcriptions, break_into_sentences
from pathlib import Path
import os
from parse_xml import parse_xml, from_key_to_text_and_line_numbers
from statistics import mean
import matplotlib.pyplot as plt
from data import increment_count


def write_sentences_to_file(chars_sentences, translation_sentences):
    signs_file = open(Path(r"../NMT_input/signs_per_line.txt"), "w", encoding="utf8")
    transcription_file = open(Path(r"../NMT_input/transcriptions_per_line.txt"), "w", encoding="utf8")
    translation_file = open(Path(r"../NMT_input/translation_per_line.txt"), "w", encoding="utf8")

    translation_lengths = []
    for key in translation_sentences:
        signs_file.write(key + ": ")
        transcription_file.write(key + ": ")
        translation_file.write(key + ": ")

        for c in chars_sentences[key]:
            signs_file.write(c[3])
            delim = c[2] if not c[2] is None else " "
            transcription_file.write(c[1] + delim)

        translation_lengths.append(len(translation_sentences[key]))
        for t in translation_sentences[key]:
            translation_file.write(t[1] + " ")

        signs_file.write("\n")
        transcription_file.write("\n")
        translation_file.write("\n")

    print("Number of word translations in a line is: " + str(len(translation_lengths)))
    print("Mean word translations in a line length is: " + str(mean(translation_lengths)))
    build_graph(translation_lengths, "word translations in a line")

    signs_file.close()
    transcription_file.close()
    translation_file.close()


def build_translations(corpora, mapping):
    base_directory = Path(r"../raw_data/tei/")
    all_translations = {}

    for corpus in corpora:
        directory = base_directory / corpus
        for r, d, f in os.walk(directory):
            for file in f:
                translation = parse_xml(os.path.join(r, file), mapping, corpus)
                all_translations.update(translation)

    return all_translations


def build_full_line_translation_process(corpora):
    chars, translation, mapping = build_signs_and_transcriptions(corpora)
    chars_sentences = break_into_sentences(chars)
    translation_sentences = break_into_sentences(translation)
    write_sentences_to_file(chars_sentences, translation_sentences)
    return chars_sentences, mapping


def build_graph(translation_lengths, name):
    # matplotlib histogram
    plt.hist(translation_lengths, color='blue', edgecolor='black', bins=100)

    # Add labels
    plt.title('Histogram of Translation Lengths - ' + name)
    plt.xlabel('Number of Words in a Sentence')
    plt.ylabel('Number of Sentences')

    plt.savefig(Path(r"../output/" + name))


def get_dict_sorted(d):
    return str({k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)})


def get_rare_elements_number(d, n):
    i = 0
    for k, v in d.items():
        if v < n:
            i += 1

    return str(i)


def write_translations_to_file(chars_sentences, translations):
    signs_file = open(Path(r"../NMT_input/signs.txt"), "w", encoding="utf8")
    transcription_file = open(Path(r"../NMT_input/transcriptions.txt"), "w", encoding="utf8")
    translation_file = open(Path(r"../NMT_input/translation.txt"), "w", encoding="utf8")

    translation_lengths = []
    long_trs = 0
    very_long_trs = 0
    signs_vocab = {}
    transcription_vocab = {}
    translation_vocab = {}

    for key in translations.keys():
        text, start_line, end_line = from_key_to_text_and_line_numbers(key)

        if start_line == -1:
            continue

        signs = ""
        transcription = ""
        for n in range(start_line, end_line + 1):
            k = text + "." + str(n)
            if k not in chars_sentences.keys():
                continue

            for c in chars_sentences[k]:
                signs += c[3]
                increment_count(signs_vocab, c[3])
                delim = c[2] if not c[2] is None else " "
                transcription += c[1] + delim
                increment_count(transcription_vocab, c[1])

        if signs == "" and transcription == "":
            continue

        # Write to files
        signs_file.write(str(key) + ": ")
        transcription_file.write(str(key) + ": ")
        translation_file.write(str(key) + ": ")

        signs_file.write(signs + "\n")
        transcription_file.write(transcription + "\n")

        tr = translations[key]

        # Statistics of translation lengths
        translation_lengths.append(len(tr.split()))
        if len(tr.split()) > 50:
            long_trs += 1

        if len(tr.split()) > 200:
            very_long_trs += 1

        for word in tr.split():
            word = word.replace(",", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "")
            if word.replace(".", "") == "":
                word = "..."
            else:
                word = word.replace(".", "")
            increment_count(translation_vocab, word)

        translation_file.write(tr + "\n")

    print("Number of real translations is: " + str(len(translation_lengths)))
    print("Mean real translations length is: " + str(mean(translation_lengths)))
    print("Number of real translations longer than 50 is: " + str(long_trs))
    print("Number of real translations longer than 200 is: " + str(very_long_trs))

    print("Size of signs vocabulary is: " + str(len(signs_vocab)))
    print("Number of signs with less than 5 occurrences is: " + get_rare_elements_number(signs_vocab, 5))
    print("The signs vocabulary is: " + get_dict_sorted(signs_vocab))

    print("Size of transliteration vocabulary is: " + str(len(transcription_vocab)))
    print("Number of transliterations with less than 5 occurrences is: " +
          get_rare_elements_number(transcription_vocab, 5))
    print("The transliteration vocabulary is: " + get_dict_sorted(transcription_vocab))

    print("Size of translation (English) vocabulary is: " + str(len(translation_vocab)))
    print("Number of translations (English) with less than 5 occurrences is: " +
          get_rare_elements_number(translation_vocab, 5))
    print("The translation (English) vocabulary is: " + get_dict_sorted(translation_vocab))

    build_graph(translation_lengths, "real translations")

    signs_file.close()
    transcription_file.close()
    translation_file.close()


def preprocess(corpora):
    chars_sentences, mapping = build_full_line_translation_process(corpora)
    translations = build_translations(corpora, mapping)
    write_translations_to_file(chars_sentences, translations)


def main():
    corpora = ["rinap", "riao", "ribo", "saao", "suhu"]
    preprocess(corpora)

if __name__ == '__main__':
    main()
