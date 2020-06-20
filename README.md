# medium-star-search

A search engine that allows you to search articles previously scraped from medium.   
(Scrapy + Selenium + Elasticsearch + Django + Redis)

## Quick Start

```python
# Windows
# Download source code
git clone https://github.com/cardinalion/medium-star-search.git
# Create virtual environment
cd medium-star-search
pipenv install
pipenv shell
# Install dependencies
pip install -r requirements.txt
# Start Elasticsearch and initialize Document
${Elasticsearch}\bin\elasticsearch.bat
python medium\medium\model\es_types.py
# Start Spider
cd medium
python main.py
# Start Django
python ..\starsearch\manage.py runserver
```

## Others

Elasticsearch-Head and Kibana are helpful for interacting with elasticsearch.   
Please modify webdriver location according to your computer.   
Thanks Iconfinder for png icons. I named this search engine after the logo icon.   
