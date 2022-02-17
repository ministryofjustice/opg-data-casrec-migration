import aiohttp
import asyncio
import requests
import time
import sys
import os
import psycopg2
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
import custom_logger
import logging

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")
# Update to DEBUG for extra logging whilst developing
custom_logger.setup_logging(
    env=environment, level="INFO", module_name="API light-touch tests"
)
from helpers import get_config


class AsyncResponse:
    def __init__(self):
        self.environment = os.environ.get("ENVIRONMENT")
        self.config = get_config(environment)
        self.base_url = os.environ.get("SIRIUS_FRONT_URL")
        self.user = os.environ.get("SIRIUS_FRONT_USER")
        self.password = os.environ.get("API_TEST_PASSWORD")
        self.total_records = os.environ.get("LIGHT_TOUCH_COUNT")
        self.chunk_size = 50
        self.headers_dict = {}
        self.client_ids = []
        self.correct_status_count = 0
        self.incorrect_status_count = 0
        self.incorrect_status_list = []

    def authenticate(self):
        response = requests.get(self.base_url)
        cookie = response.headers["Set-Cookie"]
        xsrf = response.headers["X-XSRF-TOKEN"]
        self.headers_dict = {"Cookie": cookie, "x-xsrf-token": xsrf}
        data = {"email": self.user, "password": self.password}
        with requests.Session() as s:
            p = s.post(
                f"{self.base_url}/auth/login", data=data, headers=self.headers_dict
            )
            log.info(f"Login to sirius returns: {p.status_code}")

    async def get_response_status(self, session, url):
        async with session.get(url) as resp:
            if resp.status != 200:
                self.incorrect_status_list.append(f"status: {resp.status}, url: {url}")
            return resp.status

    async def main_loop(self, ids):
        async with aiohttp.ClientSession(headers=self.headers_dict) as session:

            tasks = []
            for id in ids:
                url = f"{self.base_url}/api/v1/clients/{id}"
                tasks.append(
                    asyncio.ensure_future(self.get_response_status(session, url))
                )

            status_list = await asyncio.gather(*tasks)
            for status in status_list:
                if status == 200:
                    self.correct_status_count += +1
                else:
                    self.incorrect_status_count += +1

    def get_client_id_subset(self):
        sql = f"SELECT id FROM public.persons WHERE clientsource = 'CASRECMIGRATION' LIMIT {self.total_records}"
        conn_target = psycopg2.connect(self.config.get_db_connection_string("target"))
        cursor_target = conn_target.cursor()
        cursor_target.execute(sql)
        id_rows = cursor_target.fetchall()
        cursor_target.close()
        for id_row in id_rows:
            self.client_ids.append(int(id_row[0]))

    def run_async_requests(self):
        count = 0
        expected_chunks = round(int(len(self.client_ids)) / self.chunk_size)
        for chunk in self.chunks():
            count += 1
            log.info(f"Processing chunk {count} of {expected_chunks}")
            asyncio.run(self.main_loop(chunk))

    def chunks(self):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(self.client_ids), self.chunk_size):
            yield self.client_ids[i : i + self.chunk_size]


async_response = AsyncResponse()
async_response.authenticate()
async_response.get_client_id_subset()

start_time = time.time()
async_response.run_async_requests()
log.info(
    f"Correct responses: {async_response.correct_status_count}, Incorrect responses: {async_response.incorrect_status_count}"
)
for msg in async_response.incorrect_status_list:
    log.info(msg)
log.info("--- %s seconds ---" % (time.time() - start_time))
