import urllib2
import bs4
from workflow import Workflow

baseurl = 'https://www.v2ex.com'
r = urllib2.urlopen('https://www.v2ex.com/go/macos?p=1').read()

soup = bs4.BeautifulSoup(r, "html.parser")

wf = Workflow()
for a in soup.select('span.item_title a'):
    wf.add_item(title=a.text,
                subtitle=baseurl + a.attrs.get('href'),
                arg=baseurl + a.attrs.get('href'),
                valid=True,
                icon=u'./icon.png')

wf.send_feedback()


# import urllib2
# import bs4
# from workflow import Workflow

# baseurl = 'https://www.v2ex.com'
# r = urllib2.urlopen('https://www.v2ex.com/go/macos?p=1').read()

# soup = bs4.BeautifulSoup(r, "html.parser")

# topicsnode = soup.find('div', attrs={'id': 'TopicsNode'})

# wf = Workflow()
# for a in topicsnode.select('div.cell'):
#     wf.add_item(title=a.span.a.text,
#                 subtitle=baseurl + a.span.a['href'],
#                 valid=True,
#                 icon='https:' + a.img['src'])

# wf.send_feedback()

