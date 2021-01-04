# Facebook Scraper

Scrape Facebook public pages without an API key. Inspired by [twitter-scraper](https://github.com/kennethreitz/twitter-scraper).

## Install

```sh
pip install facebook-scraper
```

## Running

```python the_crawler.py

After run the command, the process will automatically crawl the all the posts(to set the number of posts, modify the "SCROLL" in setting.py file) and the all user profiles.
```

## Post example

```python
{
    _id: "108517"
id: ""
post_id: ""
post_url: "https://www.facebook.com/nam.lethanh.948/posts/1411555592343129"
post_date: "11 tháng 12, 2019 lúc 14:45"
message: "Chính Chủ Bán 2 lô Đất .. lô Trước Và Lô Phía Sau liền Kề Nhau Mặt Tiề..."
n_likes: ""
n_react: "14"
n_comments: 9
n_shares: "150 lượt chia sẻ"
attributes:[]
post_owner_id: "100004661048146"
phone: "0365280951"
list_user_like:
0: "100011569806344"
1: "100014006445510"
2: "100007108396509"
3: "100008487732446"
4: "100043672152139"
5: "100030086821369"
6: "100006068760838"
7: "100023760641757"
8: "100029057504405"
9: "100007033536394"
10: "100014647092059"
11: "100021934846816"
12: "100004661048146"
13: "100041289641847"
}
```

### Notes

- There is no guarantee that every field will be extracted (they might be `None`).
- Shares doesn't seem to work at the moment.
