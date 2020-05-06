# spider_bili
哔哩哔哩的爬虫

```python
with Bili() as bili:
    aid, cid = bili.get_aid(bv='BV1bz411q7XU')      # 使用 bv 号获取视频信息
    tv_data = bili.get_tv_data(aid=aid)             # 使用 aid 获取视频的播放、投币、收藏等
    tv_commit = bili.get_commit(aid=aid)            # 获取评论
    tv_dm = bili.get_dm(oid=cid)                    # 获取弹幕
    bili.get_video(aid, cid, 32)                    # 下载视频

```