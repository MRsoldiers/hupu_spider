from cardsStore import CardStore
from cardCrawler import PostStore
import json


def crawl():
    u = 'https://bbs.hupu.com/vote-postdate'
    cardStore = CardStore()
    i = 0
    dateFlag = 1
    while(dateFlag):
        url = u if i == 0 else u + '-' + str(i)
        print('parsing page', i, dateFlag, url)
        dateFlag = cardStore.parsePage(url)
        i += 1
    cards = cardStore.getCards()
    
    data = []
    i = 0
    for card in cards:
        print('parsing card %d', i)
        postStore = PostStore(card)
        postStore.crawlDialog()
        cardWithPost = postStore.getCardInfoWithPost()
        data.append(cardWithPost)
        i += 1

    fw = open('hupu.json', 'w')
    fw.write(json.dumps(data, indent=4))
    fw.close()
    

if __name__ == "__main__":
    crawl()


