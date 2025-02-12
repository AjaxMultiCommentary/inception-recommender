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

# Acknowledgements

Code in this repository was produced in the context of the Ajax Multi-Commentary project, funded by the Swiss National Science Foundation under an Ambizione grant [PZ00P1\_186033](http://p3.snf.ch/project-186033).
