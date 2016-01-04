tweetcatcher.py
---
Interactive Twitter client for the REST API that makes use of the [Twython library](https://github.com/ryanmcgrath/twython). It knows about the [entire REST API surface](https://gist.github.com/withtwoemms/54ea3e7e389703640f9d) by scraping the docs and caching the info in a convenient format. Does the same with [rate limits](https://gist.github.com/withtwoemms/e5c80f9eed0d3f8b9e4a). It's meant to be used in your favorite Python interactive shell (bpython, ipython, python, etc.). Below are
some notes on usage:

```python
>>> from tweetcatcher import TweetCatcher
>>> tc = TweetCatcher()
>>> tc.catch('statuses/home_timeline')
--------------------
Please enter values for the following params: 
--------------------
count = 50
contributor_details = 
exclude_replies = 
since_id = 
include_entities = 
trim_user = 
max_id =
```

All you need to do is pass the endpoint name to the TweetCatcher#catch method and this implementation handles the rest. If there are params to be specified, they will pop up sequentially. Enter values if you'd like, otherwise they will be logged as having a value of `None`. Currently, I am the only one with app keys, but I will make an interface for serving access tokens so that others can use it. Going to deal with pagination and exporting data in the future.
