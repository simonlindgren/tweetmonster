# TWEETMONSTER

Tweetmonster is a method for collecting tweets both a bit back in time (as long as the SearchAPI allows, ~7 days), and in realtime, for a set of keywords. It uses the Search API to search back, and the Streaming API to stream in realtime. Tweet objects are written to two databases, that can eventually be merged into one.

## Usage 

To set up the query, edit `q.txt` with one keyword per line.

A set of valid Twitter API keys must be provided in `credentials.py`.

Create the databases:

```
>>> import tweetmonster as tm
>>> tm.make_databases("<your-project-name>")
```

Long-term tweet collections jobs will inevitably break or run into errors that you have not been able to catch or predict with your code. A (nearly) fool-proof way of avoiding this, is to launch your collection jobs through persistent bash-scripts that will re-start relentlessly on any crash.

To be able to keep track of your jobs, it is recommendable to run them as two separate [screen](https://linuxize.com/post/how-to-use-linux-screen/) sessions.

#### Launch the backward search (in one session)

```
$ sh search.sh
```

#### Launch the forward search (in another session)

```
$ sh stream.sh
```

#### Extract the data currently in the databases

At any point during ongoing data collection.

```
>>> import tweetmonster as tm
>>> tm.extract_data("<your-project-name>")

```

#### Drastic cleanup

`tm.dbkill()` - delete all databases in the directory.


