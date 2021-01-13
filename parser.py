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
	for item in zip(job, money):
		print (", ".join(item))
	with open('jobs.json', 'w', encoding="utf-8") as file:
		 json.dump(database, file, ensure_ascii=False, indent=4 )


if __name__ == '__main__':
	hh_parse (headers)

