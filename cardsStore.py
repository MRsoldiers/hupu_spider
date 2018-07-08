import requests
import datetime
import re
import json
from bs4 import BeautifulSoup

class CardStore():
    cards = []
    _requestHeaders = {
        "cookie": "",
        "origin": "https://passport.hupu.com",
        "referer": "https://passport.hupu.com/pc/login?project=bbs&from=pc",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "x-requested-with": "XMLHttpRequest" 
    }
    _startDate = datetime.datetime.strptime('2018-07-01', '%Y-%m-%d')
    reDatePattern = re.compile(';cursor: initial; \">(\d*)-(\d*)-(\d*)</a>')

    def pushCards(self, cards):
        self.cards = self.cards + cards

    def getCards(self):
        return self.cards

    def getHtmlString(self, tag):
        return tag.string

    def getHtmlHref(self, tag):
        return tag.get('href')

    def generateCards(self, titles, dates, authors, links, replys):
        cards = []
        dateFlag = 1
        print(len(dates))
        for (index, dateStr) in enumerate(dates):
            date = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
            if (index == 0):
                print(date)
                continue
            replyNum = int(replys[index].split('/')[0])
            if (date <= self._startDate):
                dateFlag = 0
                break
            if (date > self._startDate and replyNum > 50):
                card = {}
                card['title'] = titles[index]
                card['author'] = authors[index]
                card['link'] = links[index]
                card['replyNum'] = replyNum
                card['date'] = dateStr
                cards.append(card)
        self.pushCards(cards)
        return dateFlag

    def parsePage(self, url):
        
        r = requests.get(url, headers=self._requestHeaders)
        htmlText = r.text
        # print(htmlText)
        soup = BeautifulSoup(htmlText, 'lxml')

        titleTags = soup.find_all('a', class_='truetit')
        titlesMap = map(self.getHtmlString, titleTags)
        titles = [t for t in titlesMap]

        datesArr = re.findall(self.reDatePattern, htmlText)
        dates = []
        for dateArr in datesArr:
            divider = '-'
            date = divider.join(dateArr)
            dates.append(date)

        authorTags = soup.find_all('a', class_='aulink')
        authorsMap = map(self.getHtmlString, authorTags)
        authors = [a for a in authorsMap]

        linkTags = soup.find_all('a', class_='truetit')
        linksMap = map(self.getHtmlHref, linkTags)
        links = [l for l in linksMap]

        replyTags = soup.find_all('span', class_='ansour')
        replysMap = map(self.getHtmlString, replyTags)
        replys = [l for l in replysMap]
        
        return self.generateCards(titles, dates, authors, links, replys)