from lxml import html
import os, json, re

results = []
sources = [s for s in os.listdir() if '.' not in s]

# s0 = sources[0]
for s0 in sources:

    pages = [p for p in os.listdir(s0) if 'html' in p]

# page = pages[0]
    for page in pages:
        with open(os.path.join(s0,page), encoding='utf-8') as f:
            text = f.read()
        res = html.fromstring(text)
        articles = res.xpath('//div[@class="article enArticle"]')
        for article in articles:
        # article = articles[3]
            line = {}
            line['title'] = (article.xpath('./div/span/text()')+[''])[0].strip()
            line['date'] = (re.findall(r'\d{1,2} \w{3,11} 20\d{2}', '\n'.join(article.xpath('.//text()')))+[''])[0].strip()
            line['author'] = (article.xpath('./div[@class="author"]/text()')+[''])[0].strip()
            line['wordscount'] = (re.findall(r'(\d+) words', '\n'.join(article.xpath('.//text()')))+[''])[0].strip()
            line['content'] = '\n'.join(article.xpath('.//p[@class="articleParagraph enarticleParagraph"]//text()'))
            line['Journal'] = s0
            results.append(line)

with open('news.json', 'w') as t:
    t.write(json.dumps(results))
    
import pandas as pd
df = pd.read_json('news.json')
df.to_excel('news.xlsx',index=0)
