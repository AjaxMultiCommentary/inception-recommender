# inception-recommender

An external recommender for the INCEpTION annotation platform, with support for tagging Classics knowledge entities.

To launch the recommender service:

```
pip install -r requirements.txt


# or bind it to 127.0.0.1
gunicorn -w 4 -b 192.168.0.177:5000 inception_recommender:app
```