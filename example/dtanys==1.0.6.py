from pprint import pprint
from dtanys import jsonpath
data = { 
    "store": {
    "book": [
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 2.99
      },
      { "category": "reference",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 18.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    },
    "test" : {
        'dir': dir
    }
    },
    "test" : 'dsajk'
}



# /a /*a //*a /*['a', 'b'] //*['a', 'b'] /a[1] /a[1:5:2] /a[1,2,3] //a[@b="s"] //[1] //['a', 'b']

# pprint(jsonpath.xpath(data, '/test'))
# pprint(jsonpath.xpath(data, '/store/book[@price>10 | @category="fiction"]'))
# pprint(jsonpath.xpath(data, '/store["test", "bicycle",]/*color'))
# pprint(jsonpath.xpath(data, '/*[@price>10 and @category="fiction"]//price'))
# pprint(jsonpath.xpath(data, '/store/book[@price>10 | @category="fiction"]//price'))
# pprint(jsonpath.xpath(data, '//*["price","title"]'))
# pprint(jsonpath.xpath(data, '/store/book[1,2]/*price'))
