mongodb-balance-check
=====================

This script provides an easy way to find out if your MongoDB shard cluster is properly balanced or not. 

You can achieve the same effect by calling `db.printShardingStatus()` but it requires manually parsing the output to see if the counts are balanced for all your collections, which could be difficult if you have a lot...or are lazy. This script does it for you and makes it clear.

Requirements
------------

* Python
* [pymongo](http://pypi.python.org/pypi/pymongo/)
* [clint](http://pypi.python.org/pypi/clint/)

Installation
------------
```
git clone git://github.com/serverdensity/mongodb-balance-check.git
sudo pip install pymongo
sudo pip install clint
```

Running
-------
This assumes you have a mongos running on `localhost:27017`

`python check.py`

Console Output
------
It will list all your collections from all databases, indicating whether they are balanced or not and the total chunk count for each one.

```
david@sdapp-web1 ~/mongodb-balance-check: python check.py 
sd.servers
    sdapp1 balanced (9)
    sdapp2 balanced (9)
sd.users
    sdapp1 unbalanced (62)
    sdapp2 unbalanced (89)
sd.alerts
    sdapp1 balanced (12)
    sdapp2 balanced (12)
...
```

Programmatic output
-------------------
You can import balanced into your own code as it has the option to return the value as part of a method call instead of outputting to the console:

```python
import balanced
result = balanced.is_balanced()
print result
{
    'chunks': {
        u'sd.servers': {
            u'sdapp1': 9,
            u'sdapp2': 9
        },
        u'sd.users': {
            u'sdapp1': 62,
            u'sdapp2': 89
        },
        u'sd.alerts': {
            u'sdapp1': 12,
            u'sdapp2': 12
        }
    },
    'isBalanced': False
}
```