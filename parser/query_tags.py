from chitaigorod import CGSpider
from livelib import getLivelib

a = getLivelib("Круть")
if a is None:
    print("Не спарсилось")
else:
    print(a.tags)