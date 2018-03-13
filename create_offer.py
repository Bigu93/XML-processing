import os.path
import codecs

base_texts = ["ID towaru:", "Nazwa towaru:", "Kategoria:", "Długi opis:",
              "Cena:", "Zdjecia:", "Rozmiary:", "Parametry:"]


def make_file(complete_data, filename):
    """Depending on file, if it exists or not, create or append it."""
    if os.path.isfile(filename):
        with codecs.open(filename, 'a', 'utf-8') as f:
            save_data(complete_data, f)
    else:
        with codecs.open(filename, 'w', 'utf-8') as f:
            save_data(complete_data, f)


def save_data(zipped_lists, file):
    """Save values from list to txt file with special formatting."""
    final_list = convert_to_list(zipped_lists)

    for elem in final_list:
        if isinstance(elem, tuple):
            if isinstance(elem[1], tuple):
                file.write("%s %s %s\n" % (elem[0], elem[1][0], elem[1][1]))
                continue
            elif isinstance(elem[1], list):
                file.write("%s\n" % (elem[0]))
                for item in elem[1]:
                    file.write("%s,\n" % item)
                continue
            elif isinstance(elem[1], dict):
                file.write("%s\n" % (elem[0]))
                for k, v in elem[1].items():
                    file.write("%s\n" % (k + ": " + v))
                continue
            file.write("%s %s\n" % (elem[0], elem[1]))
    file.write('\n')


def convert_to_list(list_with_data):
    """Zip neccessary data with base_texts lists."""
    temp_list = [shoes_id,
                 name, cat,
                 desc, price,
                 images, sizes,
                 params] = list_with_data
    zipped_lists = zip(base_texts, temp_list)
    return list(zipped_lists)
