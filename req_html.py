from requests_html import HTMLSession


from prototype_add_products import add_to_wp



def parse_img(product):
    img_tag = r.html.xpath(f'//*[@id="{product.attrs["id"]}"]/div/a/div[1]/div[2]/img')
    img_tag_without_probels = str(img_tag).split("=")

    not_valid_link = img_tag_without_probels[6]
    valid_img = "https:" + not_valid_link.split(">", 1)[0][1:-1]

    not_valid_name_product = img_tag_without_probels[5]

    valid_name_product = not_valid_name_product.split(" src", 1)[0][1:-1]
    return valid_img, valid_name_product


def add_to_model(product, valid_name_product, valid_img, price):
    # print(valid_img)
    model = {
        "name": valid_name_product,
        "regular_price": price,
        "images": [
            {
                "src": valid_img,
                "alt": valid_name_product,
            }
        ],
    }
    return model


def get_price(product):
    # print(product.text)
    i = product.text.replace("\n", " ")
    # print(i)
    j = i.split("Реклама Быстрый просмотр ", 1)[1]
    h = j.split()
    # print(h)

    # print(i.attrs)
    price = h[4]
    if price.isnumeric():
        if int(price) < 100:
            price = h[4] + h[5]
            # print(price)
    return price

    # print(price)


if __name__ == "__main__":
    print("Введите ссылку для парсинга")
    url = str(input())

    s = HTMLSession()

    r = s.get(url)
    r.html.render(sleep=1)
    prod = r.html.find("div.product-card.j-card-item.j-good-for-listing-event")

    for product in prod:
        price = get_price(product)
        valid_img, valid_name_product = parse_img(product)
        model = add_to_model(product, valid_name_product, valid_img, price)
        add_to_wp(model)
