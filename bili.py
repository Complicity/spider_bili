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
			'Referer': 'https://www.bilibili.com',
			'TE': 'Trailers',
			'Connection': 'keep-alive',
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

	def get_video(self, bvid: str, cid: str, qn: int = 32):
		'cid=177627094&bvid=BV1Bt4y1U7gm&qn=80&type=&otype=json&fourk=1&fnver=0&fnval=16&session=a663cbd758c8a772e6f1b1f864b1bd1a'
		self.headers.update({'Referer': f'https://www.bilibili.com/{bvid}'})
		url = f'https://api.bilibili.com/x/player/playurl?cid={cid}&bvid={bvid}&qn={qn}&otype=json&fourk=1&fnver=0&fnval=16'
		data = self.session.get(url, headers=self.headers).content.decode()
		try:
			url = json.loads(data).get('data').get('dash').get('video')
			url = url[(len(url) + 1) // 2]
			video = self.session.get(url.get('base_url'), headers=self.headers)
			if video.status_code != 200:
				video = self.session.get(url.get('backup_url')[0], headers=self.headers)
				if video.status_code != 200:
					return -1
			if '.flv' in url:
				ext = '.flv'
			else:
				ext = '.m4s'
		except Exception:
			return -1
		abspath = os.path.join(os.path.dirname(__file__), str(hash(video))) + ext
		with open(abspath, 'wb') as f:
			f.write(video.content)
		return 1


if __name__ == '__main__':
	with Bili() as bili:
		bv = 'BV1b54y1d7fZ'
		aid, cid = bili.get_aid(bv=bv)
		# tv_data = bili.get_tv_data(aid=aid)
		# tv_commit = bili.get_commit(aid=aid,)
		# tv_dm = bili.get_dm(oid=cid)
		print({'aid': aid, 'cid': cid})
		# print(tv_data)
		# print(tv_commit[1])
		# print(tv_dm)
		print(bili.get_video(bv, cid, 80))


