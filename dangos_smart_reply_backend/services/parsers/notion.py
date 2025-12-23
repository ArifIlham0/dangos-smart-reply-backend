from bs4 import BeautifulSoup
from .base import BaseParser

class NotionParser(BaseParser):
    def parse(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        tasks = []

        rows = soup.select("div[role='row']")
        for row in rows:
            cells = row.select("div[role='cell']")
            if not cells:
                continue

            task = {
                "title": cells[0].get_text(strip=True),
                "assignee": None,
                "status": None
            }

            if len(cells) > 1:
                task["status"] = cells[1].get_text(strip=True)

            if len(cells) > 2:
                task["assignee"] = cells[2].get_text(strip=True)

            tasks.append(task)

        return tasks
