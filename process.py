import xml.etree.ElementTree as ET
import sys
import re
from create_offer import make_file


def process_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    nsmap = '{http://www.iai-shop.com/developers/iof/extensions.phtml}'

    for product in root.iter('product'):
        shoes_id = product.get('id')
        name_of_shoes = product.find('description')[2].text
        category = product.find('category').get('name')
        temp_desc = product.find('description')[6].text
        long_desc = clean_description(temp_desc)
        price = (product.find('price').get('gross'), product.get('currency'))

        parameters = dict()
        for param in root.iter('parameter'):
            if param.get(nsmap + 'hide') != 'y':
                parameter_name = param.get('name').lstrip()
                parameter_value = param.find('value').get('name')
                parameters[parameter_name] = parameter_value

        images = list()
        for img in root.iter('image'):
            image = img.get('url')
            images.append(image)

        sizes = dict()
        for s in root.iter('size'):
            size = s.get(nsmap + 'name')
            quantity = s.find('stock').get('quantity')
            sizes[size] = quantity

        return (shoes_id,
                name_of_shoes,
                category,
                long_desc,
                price,
                images,
                sizes,
                parameters)


def clean_description(s):
    clean_re = re.compile('<.*?>')
    clean_s = re.sub(clean_re, '', s).lstrip()
    return clean_s


def print_results(data):
    shoes_id, name, cat, long_desc, price, images, sizes, params = data

    print("ID towaru:", shoes_id, '\n')
    print("Nazwa butów:", name, "\n")
    print("Kategoria:", cat, "\n")
    print("Długi opis:", long_desc, "\n")
    print("Cena brutto:", price[0], price[1], "\n")
    [print(images.index(img) + 1, img) for img in images]
    dict_print(sizes, "Rozmiar:", "Ilość:")
    dict_print(params, optional_colon=':')


def dict_print(dict, size='', quantity='', optional_colon=''):
    for key, value in dict.items():
        if size == '' and quantity == '':
            print(key, optional_colon, value)
        else:
            print(size, key, optional_colon, quantity, value)


if __name__ == "__main__":
    data = process_data(sys.argv[1])
    # print_results(data)
    make_file(data, "Oferta.txt")
