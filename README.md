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
    'balanceStatus': {
        u'sd.servers': True, 
        u'sd.users': False, 
        u'sd.alerts': True
    }
    'isBalanced': False
}
```

Server Density plugin
---------------------
This can be used as a plugin to Server Density to give you shard distribution graphs and trigger alerts when certain shards become unbalanced. It runs once per hour as it takes several seconds to run and doesn't need to be "real time".

1. Create the plugin directory for your agent if you haven't already. This involves editing the `/etc/sd-agent/config.cfg` file to point the `plugin_directory` config value to a directory e.g. `/usr/bin/sd-agent/plugins` (which you need to create).

2. In your Server Density account, click the Plugins tab then create a new plugin called MongoBalanced

3. Download the `balanced.py` and `MongoBalanced.py` files from this repo and place them in the plugin directory you created above.

4. Restart the agent

Values will be reported back right away and will appear on the graphs. There will be a lot of them; there are 3 different types.

* `database-collection-shard` e.g. `sd-users-sdapp1` - this shows the number of chunks for each database, collection and shard and is useful for graphing.
* `database-collection` e.g. sd-users - this will be either `0` (unbalanced) or `1` (balanced) and is used for alerting on specific collections.
* `isBalanced` this will be either `0` (unbalanced) or `1` (balanced) and shows the status for the whole cluster.

**Graphs**

From the Plugins tab you can edit the plugin to create the graphs based on the first type. For example, with these keys:

```
sd-users-sdapp1
sd-users-sdapp2
sd-alerts-sdapp1
sd-alerts-sdapp2
```

you can create a graph with the title `Users` and keys to display `sd-users-sdapp1`, `sd-users-sdapp2` which would show the chunk distribution for both shards.

**Alerts**

To get an alert when the `sd-users` collection is unbalanced, select the `MongoBalanced` plugin from the add alerts drop menu then use `sd-alerts` as the plugin key. Set the trigger value to equal to `0`.

To get an alert when any collection in the cluster is unbalanced, do the same as above but use `isBalanced` equal to `0` as the plugin key.