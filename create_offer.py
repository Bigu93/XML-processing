import os.path
import codecs

base_texts = ["ID towaru:", "Nazwa towaru:", "Kategoria:", "Długi opis:",
              "Cena:", "Zdjecia:", "Rozmiary:", "Parametry:"]


def make_file(complete_data, filename):
    if os.path.isfile(filename):
        with codecs.open(filename, 'a', 'utf-8') as f:
            save_data(complete_data, f)
    else:
        with codecs.open(filename, 'w', 'utf-8') as f:
            save_data(complete_data, f)


def save_data(list_data, file):
    proper_list = convert_to_list(list_data)

    for elem in proper_list:
        file.write('\n')
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
                    file.write("%s %s\n" % (k, v))
                continue
            file.write("%s %s\n" % (elem[0], elem[1]))
    file.write('\n')


def convert_to_list(data):
    temp_list = [shoes_id,
                 name, cat,
                 desc, price,
                 images, sizes,
                 params] = data
    new_list = zip(base_texts, temp_list)
    return list(new_list)
