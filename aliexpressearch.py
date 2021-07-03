import csv
import requests
import random
import json
import re
import pandas as pd
from bs4 import BeautifulSoup


class AliexpressCrawler:
    # Set default request parameters
    headers = {

        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    cookies = {
        "intl_locale": "",
        "aep_usuc_f": "",
    }
    item_uri = 'https://www.aliexpress.com/item/'
    feedback_uri = "https://feedback.aliexpress.com/display/productEvaluation.html"
    search_name = input("please input the search:")

    def __init__(self, owner_member_id="", company_id="", member_type="seller", region="US", locale="en_US",
                 currency="USD", country="usa"):
        self.owner_member_id = owner_member_id or self.generate_id()
        self.company_id = company_id or self.generate_id()
        self.cookies['intl_locale'] = f'{locale}'
        self.cookies['aep_usuc_f'] = f'isfm=y&site={country}&c_tp={currency}&region={region}&b_locale={locale}'
        self.member_type = member_type
        self.count = 1

        print(
            f'Crawliexpress - Region: {region} | Country: {country} | Locale: {locale} | Currency: {currency} | Member ID: {self.owner_member_id} | Company ID: {self.company_id}')

    # Generate random ID
    @staticmethod
    def generate_id(length=9, suffix=2):
        numbers = range(0, 10)
        id = f'{suffix}'
        for i in range(0, length - 1):
            id = f'{id}{random.choice(numbers)}'
        return id

    # Reduce text size to fit in prints
    @staticmethod
    def truncate(text, max=20):
        return f'{text[0:max]}...' if len(text) > max else text

    @property
    def search(self):

        # Results container

        res = []
        #  timeout = False

        url = f'https://www.aliexpress.com/wholesale?SearchText={self.search_name}&SortType=total_tranpro_desc'
        print(f'Crawliexpress - Categories | Url {url} ')

        request = requests.get(url, headers=self.headers, cookies=self.cookies)
        #   print(request.text)
        if request.status_code != 200:
            print('- Error: Invalid category page')

        # try:
        match = re.search(r'.*"content":(.*)}},"resultCount".*', request.text).group(1)

        items = json.loads(match)
        #  print(items)
        #  timeout = False
        '''
        except:
            print(f'- Error: No search results')
            if timeout:
                pass
            timeout = True
        '''

        for item in items:
            aux = {'product_id': item['productId'],  # .split('item/')[1].split('.html')[0],
                   'image_url': 'https:' + item['image']['imgUrl'],
                   'price': item['prices']['salePrice']['formattedPrice'],
                   'title': item['title']['displayTitle'],
                   'rating-avg': item['evaluation']['starRating'],
                   'tradeDesc': int((item['trade']['tradeDesc']).split(' ')[0])
                   }
            pic_name = aux['product_id']
            pic = requests.get(aux['image_url'])
            with open(f'./jpg/{pic_name}.jpg', "wb") as f:
                f.write(pic.content)
                print(f'{pic_name}.jpg has been saved')
            '''
            if 'starRating' in item:
                aux['rating_avg'] = item['starRating']
            else:
                aux['rating_avg'] = 0
            if 'tradeDesc' in item:
                aux['order_count'] = int((item['tradeDesc']).split(' ')[0])
            else:
                aux['order_count'] = 0
            '''
            res.append(aux)

        # res.sort(key=lambda x: x.get('order_count'))

        return res


def save_file(results, filename):
    df = pd.DataFrame(results)
    df.to_excel(f'{filename}.xlsx', index=False)
    '''
    if file_format == 'csv':
        if len(results) > 0:
            with open(f'{filename}.csv', 'w', encoding='utf8', newline='') as output_file:
                output_file.write('sep=,\n')
                fc = csv.DictWriter(output_file, fieldnames=results[0].keys())

                fc.writeheader()
                fc.writerows(results)
    elif file_format == 'json':
        with open(f'{filename}.json', 'w') as f:
            json.dump(results, f)
    print(f'file saved to {filename}.{file_format}')
    '''
    print(f'file saved to {filename}.xlsx')


def pic_to_excel(file_name):
    from openpyxl.drawing.image import Image
    import openpyxl
    pics_name = pd.read_excel(f'./{file_name}.xlsx')
    for i in range(60):
        pic_name = pics_name.iloc[i, 0]
        pic_path = f'./jpg/{pic_name}.jpg'
        pic = Image(pic_path)
        pic.width = 220
        pic.height = 220
        wb = openpyxl.load_workbook(f'./{file_name}.xlsx')
        ws = wb['Sheet1']
        ws.column_dimensions['G'].width = 31
        ws.row_dimensions[i+2].height = 165
        ws.add_image(pic, f'G{i+2}')
        wb.save(f'./{file_name}.xlsx')


if __name__ == '__main__':
    crawler = AliexpressCrawler()
    aliexpress_search_results = crawler.search
    # print(aliexpress_search_results)
    if aliexpress_search_results:
        # click.echo(aliexpress_search_results[:60])
        save_file(aliexpress_search_results, f'./{crawler.search_name}')
    pic_to_excel(f'{crawler.search_name}')
