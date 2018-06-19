#! /usr/bin/python

import os, scrapy, urllib.request, hashlib

class haodooSpyder(scrapy.Spider):
    name = "haodoo"
    custom_settings = {
        'DOWNLOAD_DELAY' : '0.35',
    }
    start_urls = ['http://haodoo.net']

    def parse(self, response):
        if not os.path.exists('epub'):
            os.makedirs('epub')
        if not os.path.exists('covers'):
            os.makedirs('covers')
        headpages = response.css('table')[2].css('td.a03 a::attr(href)').extract()
        for pg in headpages:
            if pg.find('audio') < 0 and pg.find('letter') < 0:
                url = response.urljoin(pg)
                yield response.follow(url, self.parse_heading)

    def parse_heading(self, response):
        links = response.css('script')[6].re(r'<a href="(.*)">')
        for ln in links:
            url = response.urljoin(ln)
            yield response.follow(url, self.parse_listing)
            
    def parse_listing(self, response):
        books = response.css('div.a03 a::attr(href)').extract()
        for bk in books:
            if bk.find('.pdb') >= 0 or bk.find(':') >= 0:
                # print(bk)
                continue
            url = response.urljoin(bk)
            yield response.follow(url, self.parse_book)

    def download(self, url, filename):
        if url != '':
            urllib.request.urlretrieve(url, filename)
            m = hashlib.md5()
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    m.update(data)
            return m.hexdigest()
        else:
            return ''

    def parse_book(self, response):
        names = response.css('script').re(r'SetTitle\("(.*)[《|【](.*)[》|】]"\);')
        if len(names) == 0:
            names = response.css('table')[6].re(r'<font .*>(.*)</font>[《|【](.*)[》|】]<input')
        if len(names) >= 2:
            author = names[0]
            title = names[1]
        else:
            author = 'Unknown'
            title = 'Unknown'
        book_ids = response.css('input::attr(onclick)').re(r'DownloadEpub\(\'(.*)\'\)')
        images = response.css('img::attr(src)').re(r'(covers/.*)')
        count = len(book_ids)
        imgl = len(images)
        if count > 1:
            i = 1
            for book in book_ids:
                ref = '?M=d&P=' + book + '.epub'
                url = response.urljoin(ref)
                if author == 'Unknown':
                    title = book
                if imgl == 0:
                    img = ''
                    imgurl = ''
                elif imgl < i:
                    img = images[-1]
                    imgurl = response.urljoin(img)
                else:
                    img = images[i - 1]
                    imgurl = response.urljoin(img)
                epub_md5 = self.download(url, 'epub/' + book + '.epub')
                img_md5 = self.download(imgurl, img)
                yield {
                    'author' : author,
                    'title'  : title + '%02d' % i,
                    'epub'   : url,
                    'epub_md5' : epub_md5,
                    'image'  : imgurl,
                    'img_md5': img_md5,
                }
                i = i + 1
        elif count == 1:
            ref = '?M=d&P=' + book_ids[0] + '.epub'
            url = response.urljoin(ref)
            if author == 'Unknown':
                title = book_ids[0]
            if imgl > 0:
                img = images[0]
                imgurl = response.urljoin(img)
            else:
                img = ''
                imgurl = ''    
            epub_md5 = self.download(url, 'epub/' + book_ids[0] + '.epub')
            img_md5 = self.download(imgurl, img)
            yield {
                'author' : author,
                'title'  : title,
                'epub'   : url,
                'epub_md5' : epub_md5,
                'image'  : imgurl,
                'img_md5': img_md5,
            }
