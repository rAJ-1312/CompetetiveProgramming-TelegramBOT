import requests

def random_quote():
    try:       
        url = "https://programming-quotes-api.herokuapp.com/quotes/random"
        r = requests.get(url)
        obj = r.json()
        quote = obj["en"].strip(".") + " ->> <b>" + obj['author'] + "</b>"
        return quote
    except BaseException:
        s = "First, solve the problem. Then, write the code. ->> <b>John Johnson</b>"
        return s