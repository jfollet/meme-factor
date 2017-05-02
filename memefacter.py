import requests

"""
A Mashup that takes "facts" from http://www.unkno.com/ and adds them
to memes using https://memegenerator.net

This base code is a copy of our initial pseudo calculator code; we will
modify it to our purpose.

TODO PART 1:

Visit https://memegenerator.net/Woody-Buzz-Everywhere/caption . Open the
network inspector and begin filling in TOP TEXT and BOTTOM TEXT. Take a
look at the traffic that's generated as the image displays the text that
you have entered.

You should see that everytime you modify the text, a request is issued.

Questions PART 1:

1. What is the PROTOCOL of these requests? (http vs https) ____https_________
2. What is the METHOD of these requests? (GET, POST, other?) ____GET_________
3. What is the RESOURCE of these requests? (everything between the domain and the `?`)
   _______Instance/Preview___________
4. What are the PARAMETERS of the request? (look at the query string variable
   names following the `?` ________imageID, text0______________________________
   

Point of interest: When you inspect the query string variables, you'll see
that your spaces have been replaced by "%20".

Given this information, you should now be able to issue your own requests to
the meme generator server!

"""


def meme_it(fact):
    """
    Given a fact, mashes that fact into a Buzz Lightyear "x-x-everywhere"
    meme. Use https://memegenerator.net/Woody-Buzz-Everywhere/caption .
    Returns the byte-encoded image.
    
    TODO PART 1: COMPLETE THIS FUNCTION
    
    HINT: You'll be issuing a GET request using the requests library,
    capturing the response object that's returned from the request,
    and then returning response.content

    HINT: Remember that you can pass the query string variables as
    a dictionary using the `params` keyword argument of requests.get

    """
    meme_url = "https://cdn.meme.am/Instance/Preview"
    params = {"imageID": "7953644"}
    for i, sentence in enumerate(fact.splitlines()):
        key = "text" + str(i)
        params[key] = sentence
    response = requests.get(meme_url, params=params)
    print(response.url)
    return response.content


def get_fact():
    """
    Returns a string.
    
    TODO PART 2: Make this get a fact from unkno.com
    """

    return "Badgers are strong.\r\nYes they are..."


def process(path):
    fact = get_fact()
    meme = meme_it(fact)

    return meme


def application(environ, start_response):
    headers = [('Content-type', 'image/jpeg')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        body = process(path)
        status = "200 OK"
    except NameError as e:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>".encode()
        body += str(e)
        exit(1)
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>".encode()
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
