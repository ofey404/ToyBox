N-crawler
=========

> Abandon all hope, all ye who enter here.

Simple crawler for nhentai.net.

## Usage

Take your gallery ID, then let's rock.

```bash
python ncurl.py 383251 # gallery ID
```

Output would save in `./383251/`

## Faster?

Change concurrency with `WORKER_COUNT` global variable.

```python
WORKER_COUNT = 10
```

Experiment: Allow about 24 connections at same time, more would be dropped.