# inception-recommender

An external recommender for the INCEpTION annotation platform, with support for tagging Classics knowledge entities.

To launch the recommender service:

```
pip install -r requirements.txt


# or bind it to 127.0.0.1
gunicorn -w 4 -b 192.168.0.177:5000 inception_recommender:app
```

And the Docker command

```
docker run -e JAVA_OPTS="-Dlogging.level.httpclient.wire.header=debug" -p 8080:8080 -p 5001:5000 ghcr.io/inception-project/inception:29.7
```

## TODOs

- ✅ make it possible to select a different model for diff. languages supported
- ✅ support fine-grained in addition to coarse
- add the hmbert fine-grained model to git via lfs