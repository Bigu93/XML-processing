import xml.etree.ElementTree as ET
import sys
import re
from create_offer import make_file

nsmap = '{http://www.iai-shop.com/developers/iof/extensions.phtml}'


def processProducts():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    for child in root.iter('product'):
        data = process_data(child)
        print_results(data)
        make_file(data, sys.argv[2])


def process_data(product):
    """Parse XML file, iterate through it to get and retrieve data.
    Return all interesting values as a tuple."""
    for value in product.iter('product'):
        shoes_id = value.get('id')
        name_of_shoes = value.find('description')[2].text
        category = value.find('category').get('name')
        temp_desc = value.find('description')[6].text
        long_desc = clean_description(temp_desc)
        price = (value.find('price').get('gross'), value.get('currency'))

        parameters = dict()
        for param in value.iter('parameter'):
            if param.get(nsmap + 'hide') != 'y':
                parameter_name = param.get('name').lstrip()
                parameter_value = param.find('value').get('name')
                parameters[parameter_name] = parameter_value

        images = list()
        for img in value.iter('image'):
            image = img.get('url')
            images.append(image)

        sizes = dict()
        for s in value.iter('size'):
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
    """Remove everything inside <[tag]> with tag itself."""
    clean_re = re.compile('<.*?>')
    clean_s = re.sub(clean_re, '', s).lstrip()
    return clean_s


def print_results(data):
    """Printing all results in human read style."""
    shoes_id, name, cat, long_desc, price, images, sizes, params = data

    print("ID towaru:", shoes_id, '\n')
    print("Nazwa butów:", name, "\n")
    print("Kategoria:", cat, "\n")
    print("Długi opis:", long_desc, "\n")
    print("Cena brutto:", price[0], price[1], "\n")
    [print(images.index(img) + 1, img) for img in images]
    dict_print(sizes, "Rozmiar:", "Ilość:")
    dict_print(params)


def dict_print(dict, size='', quantity=''):
    """Print dictionary result in key, value style with optional
    size and quanitity args."""
    for key, value in dict.items():
        if size == '' and quantity == '':
            print(key + ": " + value)
        else:
            print(size, key + ": " + quantity, value)


if __name__ == "__main__":
    processProducts()
