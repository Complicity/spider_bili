import requests
import typing
import json
import os
import random


class Bili:
	def __init__(self):
		self.session = requests.sessions.Session()
		self.headers = {
			'Host': 'api.bilibili.com',
			'Origin': 'https://www.bilibili.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
			'Referer': 'https://www.bilibili.com'
		}
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.session.close()

	def get_tv_data(self, aid: str) -> typing.Dict:
		url = f'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}'
		data = self.session.get(url=url, headers=self.headers).content.decode()
		return json.loads(data).get('data')

	def get_commit(self, aid: str):
		commit_list = []
		page = 1
		while True:
			url = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={aid}&sort=2'
			page += 1
			data = self.session.get(url=url, headers=self.headers)
			try:
				data_list: list = json.loads(data.content.decode()).get('data').get('replies')
				for data in data_list:
					commit_list.append(
						[data.get('member').get('mid'), data.get('member').get('uname'), data.get('content').get('message')])
			except TypeError:
				break
		return commit_list

	def get_aid(self, bv: str) -> list:
		url = f'https://api.bilibili.com/x/web-interface/view/detail?bvid={bv}&aid=&jsonp=jsonp'
		data = self.session.get(url=url, headers=self.headers).content.decode()
		view: dict = json.loads(data).get('data').get('View')
		return [view['aid'], view['cid']]

	def get_dm(self, oid: str) -> str:
		url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={oid}'
		data = self.session.get(url=url, headers=self.headers).content.decode()
		return data

	def get_video(self, aid: str, cid: str, qn: int = 32):
		url = f'https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn={qn}'
		data = self.session.get(url, headers=self.headers).content
		url = json.loads(data).get('data').get('durl')[0]
		video = self.session.get(url.get('url'), headers=self.headers)
		if video.status_code != 200:
			video = self.session.get(url.get('backup_url')[0], headers=self.headers)
			if video.status_code != 200:
				return -1
		ext = '.flv'
		abspath = os.path.join(os.path.dirname(__file__), str(hash(video))) + ext
		with open(abspath, 'wb') as f:
			f.write(video.content)


if __name__ == '__main__':
	with Bili() as bili:
		aid, cid = bili.get_aid(bv='BV1bz411q7XU')
		tv_data = bili.get_tv_data(aid=aid)
		tv_commit = bili.get_commit(aid=aid,)
		tv_dm = bili.get_dm(oid=cid)
		print(aid, cid)
		print(tv_data)
		print(tv_commit[1])
		print(tv_dm)
		bili.get_video(aid, cid, 32)


