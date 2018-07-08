import requests
import re
from bs4 import BeautifulSoup

class PostStore():
    cardInfo = {}
    _host = 'https://bbs.hupu.com'
    _requestHeaders = {
        "cookie": "",
        "origin": "https://passport.hupu.com",
        "referer": "https://passport.hupu.com/pc/login?project=bbs&from=pc",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "x-requested-with": "XMLHttpRequest" 
    }
    replyPattern = re.compile(r'<td>(.*)</td>',re.DOTALL)
    blockquotePattern = re.compile(r'<blockquote>(.*)</blockquote>')
    smallPattern = re.compile(r'<small(.*)</small>')

    def __init__(self, cardInfo):
        self.cardInfo = cardInfo
    
    def getCardInfoWithPost(self):
        return self.cardInfo
    
    def cutblockquote(self, post):
        flag = self.blockquotePattern.search(post)
        if flag:
            e = flag.span()[1]
            lenA = len(post)
            return post[e-lenA:]
        else:
            return post

    def cutbSmall(self, post):
        flag = self.smallPattern.search(post)
        if flag:
            s = flag.span()[0]
            lenA = len(post)
            return post[0:s]
        else:
            return post

    def replaceTag(self, post):
        p = post.replace('<br/>', ';')
        p1 = p.replace('\n', '')
        p2 = p1.replace('<div>', '')
        p3 = p2.replace('</div>', '')
        return p3

    def cleanPost(self, post):
        post1 = self.cutblockquote(post)
        post2 = self.cutbSmall(post1)
        post3 = self.replaceTag(post2)
        return post3

    def crawlDialog(self):
        
        url = self._host + self.cardInfo['link']
        # url = 'https://bbs.hupu.com/22799363.html'
        r = requests.get(url, headers=self._requestHeaders)
        htmlText = r.text
        soup = BeautifulSoup(htmlText, 'lxml')
        if (len(soup.find_all('div', id="readfloor")) == 0):
            self.cardInfo['hotposts'] = []
            return
        hotposts = soup.find_all('div', id="readfloor")[0].contents

        hotpostsCleaned = []
        for post in hotposts:
            if len(str(post)) == 1:
                continue
            hotpostsCleaned.append(post.get_text("|", strip=True))
            # raw = re.findall(self.replyPattern, str(post))[0]
            # cleanedpost = self.cleanPost(raw)
            # print(cleanedpost.replace("\n", ""))
        
        self.cardInfo['hotposts'] = hotpostsCleaned
        


if __name__ == "__main__":
    postStore = PostStore({})
    postStore.crawlDialog()
