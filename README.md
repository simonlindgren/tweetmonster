# TWEETMONSTER

Twitter provides access to its data through a set of different APIs. Two of these are the Search API and the Streaming API. The public version of the Search API goes back 7 days in time. According to Twitter it "behaves similarly to, but not exactly like the Search feature available in Twitter mobile or web clients". It does not aspire to be a source of complete data. The public Streaming API returns tweets in realtime that match one or more filter predicates.

While none of these methods promises to give access to *all* tweets on a given topic, they still return large amounts of relevant data for a number of applications. 

Tweetmonster is a method for collecting tweets both a bit back in time, and in realtime, for a set of keywords. It uses the Search API to search back, and the Streaming API to stream in realtime. Tweet objects are parsed and written to two databases, that can eventually be merged into one database.

## Usage 

To set up the query, edit `q.txt` with one keyword per line.

A set of valid Twitter API keys must be provided in `credentials.py`.

```
python
import tweetmonster as tm
tm.make_databases("<your-project-name>")
```

Long-term tweet collections jobs will inevitably break or run into errors that you have not been able to catch or predict with your code. A fool-proof way of avoiding this, is to launch your collection jobs through persistent bash-scripts that will re-start relentlessly on any crash.

To be able to keep track of your jobs, it is recommendable to run them as two separate [screen](https://linuxize.com/post/how-to-use-linux-screen/) sessions.

#### Launch the backward search

```
$ sh search.sh
```

#### Launch the forward search

```
$ sh stream.sh

```

#### Extract the data currently in the databases

```
python
import tweetmonster as tm
tm.extract_data("<your-project-name>")

```

-

`tm.dbkill()` - delete all databases in the directory.


