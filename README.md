# TWEETMONSTER

Tweetmonster will get tweets from the public Twitter APIs, and save them in sqlite3 format. It launches two simultaneous processes for one and the same search query, where one process goes as far back in time as possible (SearchAPI), and the other keeps streaming tweets live as they happen (StreamingAPI).


### Usage

A valid set of Twitter api credentials must be provided in `credentials.py`.

Enter queries as lines in `q.txt`.

```
python tm.py <parameters>
```

### Parameters

`-p`, `--project`, name of the tweet collection project, default = "tm"

`-d`, `--days`, the number of days _back_ in time collected, the SearchAPI offers up to around a week back, default = 10 (to get as much as possible) 


As you will likely collect data for some time, it may be a good idea to run tm.py as a [background process](https://kb.iu.edu/d/afnz).


---
### Additional functions
#### Progress inspector
```
python tm_i.py <parameters>
```

`-p`, `--project`, name of the project, default = "tm"

#### Data extractor

```
python tm_d.py <parameters>
```

`-p`, `--project`, name of the project, default = "tm"

`--csv`, set this flag to export not only to sqlite3 db, but also to a csv file

---

### Prerequisites

Run the following command to install package dependencies:

```
pip install -r requirements.txt
```

