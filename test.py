from urllib import response


CLIENT_ID = "hMsbLHYw68EctNQC_Bml"
CLIENT_SECRET = "zbMb6cu4PE"


def search_book(query):
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode, quote
    import json

    request = Request(
        "https://openapi.naver.com/v1/search/book?query=" + quote(query)
    )
    request.add_header("X-Naver-Client-id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)

    response = urlopen(request).read().decode("utf-8")
    search_result = json.loads(response)
    return search_result


if __name__ == "__main__":
    books = search_book("종의 기원")["items"]
    for book in books:
        print("title: {}".format(book["title"]))
        print("author: {}".format(book["author"]))
        print("pubdate: {}".format(book["pubdate"]))
        print("image: {}".format(book["image"]))
        print("description: {}".format(book["description"]))
        print("-------")
# item's key
# title, link, image, author, price, discount, publisher, pubdate, isbn, description
