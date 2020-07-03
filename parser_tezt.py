import requests
import lxml.html
import json

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

def input_url():
	text = input(" Введите требуемую профессию: ")
	url = f'https://spb.hh.ru/search/vacancy?clusters=true&area=2&order_by=salary_desc&enable_snippets=true&salary=&st=searchVacancy&text={text}&fromSearch=true'
	return url

def hh_parse(headers):
	base_url = input_url()
	html = requests.get(base_url, headers = headers)
	doc = lxml.html.fromstring(html.content)
	print (html)
	vacancies_count = doc.xpath('.//div[@class="bloko-columns-wrapper"]/div/div/div/h1')[0].text_content()
	pages_count = int(''.join(doc.xpath('.//div[@data-qa="pager-block"]/span[@class="pager-item-not-in-short-range"]/a/text()')))
	print (vacancies_count)
	print (str(pages_count) + " pages of pagination")
	url_list = []
	job = []
	money = []
	for i in range (pages_count):
		url_list.append(base_url + f'&page={i}')
	for url in url_list:
		html = requests.get(url, headers=headers)
		vacancies = lxml.html.fromstring(html.content).xpath('//div[@data-qa="vacancy-serp__vacancy"]')
		for divs in vacancies:
			job.append (''.join(divs.xpath('.//span[@class="g-user-content"]/a/text()')))
			if (len(divs.xpath('.//div[@class="vacancy-serp-item__sidebar"]/span/text()'))) == 1:
				money.append (divs.xpath('.//div[@class="vacancy-serp-item__sidebar"]/span')[0].text_content())
			else: money.append("none")
	# Creating a database in json where keys = jobs
	database = dict(zip(job, money))
	with open('jobs.json', 'w', encoding="utf-8") as file:
		 json.dump(database, file, ensure_ascii=False, indent=4 )



if __name__ == '__main__':
	hh_parse (headers)




# Parsing w/ BeautifulSoup
#     url_list = [base_url]
#     session = requests.Session()
#     request = session.get(base_url, headers=headers)
#
#         soup = bs(request.content, 'html.parser')
#         try:
#             pages = soup.find_all('a', attrs={'data-qa': 'pager-page'})
#             for i in range(1, int(pages[-1].text)):
#                 url = f'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&text=python&page={i}'
#                 if url not in url_list:
#                     url_list.append(url)
#         except:
#             pass
#         check = 0
#         for url in url_list:
#             request = session.get(url, headers=headers)
#             soup = bs(request.content, 'html.parser')
#             divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
#             for div in divs:
#                 title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
#                 link = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
#                 try:
#                     cost = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
#                 except:
#                     pass
#                 print(title)
#                 check += 1
#         print(check)
#
#
#
#
# hh_parse(base_url, headers)

# Creating a json database
# output = {'Title': titles, 'Price': prices}
# with open('sw_templates.json', 'w', encoding="utf-8") as file:
# 	json.dump(output, file, ensure_ascii=False, indent=4 )



# Parsing with lxml https://yasoob.me/2018/06/20/an-intro-to-web-scraping-with-lxml-and-python/
# headers = {
#      'accept': '*/*',
#      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
#                    '537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',}
# session = requests.Session()
# url = 'https://store.steampowered.com/search/?filter=topsellers&specials=1'
# base_html = session.get(url, headers = headers)
#
# url_list = []
# for i in range (5):
# 	url_list.append(f'https://store.steampowered.com/specials/#p={i}&tab=TopSellers')
#
# document = lxml.html.fromstring(base_html.content).xpath('//div[@id="search_resultsRows"]')[0]
# names = (document.xpath('.//div[@class="col search_name ellipsis"]/span/text()'))
# print (names)
