from airflow import DAG
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import uuid


# Scraper class defined here
class Scraper:
    articles = []

    def scraper(self, source):
        news_source = self._get_scraper(source["source"])
        news_source(source)
        return self.articles

    def _get_scraper(self, source):
        match source:
            case "hespress":
                return self._hespressScraper
            case "hibapress":
                return self._hibapressScraper
            case "alalam":
                return self._alalamScraper
            case "assabah":
                return self._assabahScraper
            case _:
                raise ValueError(source)

    def _hespressScraper(self, source):
        response = requests.get(source["link"]).text
        soup = BeautifulSoup(response, "lxml")
        data = soup.findAll("div", {"class": "carousel-item"})
        for i, row in enumerate(data):
            if i == 0 or i == len(data) - 1:
                continue
            link_tag = row.find("a")
            title = link_tag.get("title")
            link = link_tag.get("href")
            img = row.find("img").get("src")

            # Only add if all fields are not None
            if title and link and img:
                article = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "link": link,
                    "img": img,
                    "source": source["source"],
                    "created_at": datetime.now().isoformat(),
                }
                self.articles.append(article)

    def _hibapressScraper(self, source):
        response = requests.get(source["link"]).text
        soup = BeautifulSoup(response, "lxml")
        data = soup.findAll("li", {"class": "post-item"})
        for row in data:
            img = row.find("img")
            link_tag = row.find("a")
            link = link_tag.get("href")
            title = link_tag.get("aria-label")
            src = img.get("src") if img else None

            # Only add if all fields are not None
            if title and link and src:
                article = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "link": link,
                    "img": src,
                    "source": source["source"],
                    "created_at": datetime.now().isoformat(),
                }
                self.articles.append(article)

    def _alalamScraper(self, source):
        response = requests.get(source["link"]).text
        soup = BeautifulSoup(response, "lxml")
        data = soup.find_all("div", {"class": "cel1 id1 last"})
        for row in data:
            img = row.find("img")
            link_tag = row.find("a")
            link = link_tag.get("href")
            src = img.get("src") if img else None
            title = img.get("title") if img else None

            # Only add if all fields are not None
            if title and link and src:
                article = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "link": source["link"] + link,
                    "img": src,
                    "source": source["source"],
                    "created_at": datetime.now().isoformat(),
                }
                self.articles.append(article)

    def _assabahScraper(self, source):
        response = requests.get(source["link"]).text
        soup = BeautifulSoup(response, "lxml")
        data = soup.find_all("a", {"class": "post-thumb"})
        for row in data:
            img = row.find("img")
            link = row.get("href")
            title = row.get("aria-label")
            src = img.get("src") if img else None

            # Only add if all fields are not None
            if title and link and src:
                article = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "link": link,
                    "img": src,
                    "source": source["source"],
                    "created_at": datetime.now().isoformat(),
                }
                self.articles.append(article)


# Define the scraping function to be called by the DAG
def scrape_articles(ti):
    scraper = Scraper()
    sources = [
        {"source": "assabah", "link": "https://assabah.ma/category/24-24"},
        {"source": "hespress", "link": "https://www.hespress.com/"},
        {"source": "hibapress", "link": "https://ar.hibapress.com/"},
        {"source": "alalam", "link": "https://www.alalam.ma/"},
    ]

    articles = []
    for source in sources:
        articles.extend(scraper.scraper(source))

    # Push the unique articles to XCom
    ti.xcom_push(key="news_data", value=list(articles))


def insert_news_data_into_postgres(ti):
    news_data = ti.xcom_pull(key="news_data", task_ids="scrape_articles")
    if not news_data:
        raise ValueError("No news data found")

    postgres_hook = PostgresHook(postgres_conn_id="news")
    insert_query = """
    INSERT INTO news (title, source, image, link, created_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    for article in news_data:
        postgres_hook.run(
            insert_query,
            parameters=(
                article["title"],
                article["source"],
                article["img"],
                article["link"],
                article["created_at"],
            ),
        )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 6, 20),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "fetch_and_store_news",
    default_args=default_args,
    description="A simple DAG to fetch news data and store it in Postgres",
    schedule_interval=timedelta(days=1),
)

create_table_task = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="news",
    sql="""
    CREATE TABLE IF NOT EXISTS news (
        id SERIAL PRIMARY KEY,
        title TEXT NULL,
        source TEXT NULL,
        image TEXT NULL,
        link TEXT NULL,
        created_at DATE NULL
    );
    """,
    dag=dag,
)

scrape_task = PythonOperator(
    task_id="scrape_articles",
    python_callable=scrape_articles,
    dag=dag,
)

insert_news_data_task = PythonOperator(
    task_id="insert_news_data",
    python_callable=insert_news_data_into_postgres,
    dag=dag,
)

# Dependencies
scrape_task >> create_table_task >> insert_news_data_task
