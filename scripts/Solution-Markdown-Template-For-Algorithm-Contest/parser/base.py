from abc import abstractmethod, abstractproperty
import os
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class BaseParser():
    
    def __init__(self) -> None:
        self._log = []
        self._title = ""
        self.problem_num = 0

    @abstractproperty
    def name(self) -> str: ...
    @abstractmethod
    def _title_method(self) -> str: ...
    @abstractmethod
    def problem_url(self, problem_id: str) -> str: ...

    @abstractproperty
    def contest_id(self) -> str: ...
    @abstractproperty
    def code_path(self) -> str: ...
    @abstractproperty
    def problem_table(self) -> str:
        return ""

    @property
    def request_header(self):
        return {}

    @property
    def request_cookie(self):
        return {}

    @property
    def abbr(self) -> str: 
        return ""

    @property
    def template(self) -> str:
        return '''## [{} ({}{} {})]({})
### 题目大意

<++>

### 解题思路

<++>

### 代码
```cpp
{}
```

'''

    @property
    def header(self) -> str:
        title = self.title()
        return f'''---
layout: post
title: {title}
categories: AtCoder
excerpt: {title.replace("Solution", "题解")}
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} +0800
---

'''

    @property
    def output_dir(self) -> str:
        """输出目录，默认为当前目录。子类可以重写此属性来自定义输出目录"""
        return "../../_posts"  # 默认输出到_posts目录

    def get_problem(self) -> list:
        table_node = self.soup.find_all("table", class_=self.problem_table)
        trs = table_node[0].find_all("tr")
        self.problem_num = len(trs) - 1
        problems = []
        for i in range(self.problem_num):
            tr = trs[i + 1]
            tds = tr.find_all("td")
            a_tag = tds[1].find('a')

            problem_id = tds[0].get_text().strip()
            problem_name = problem_id + " - " + a_tag.get_text().strip()
            problem_url = urljoin(self.url, a_tag['href'])

            problems.append((problem_id, problem_name, problem_url))

        return problems

    def start(self, url: str):
        self.url = url
        res = self.request(self.url)
        res.raise_for_status()
        self.soup = BeautifulSoup(res.text, features="html.parser")
        self.log(self.header)

        problems = self.get_problem()
        self.problem_num = len(problems)
        print(f"find {self.problem_num} problem")

        for problem_id, problem_name, problem_url in problems:
            print(f"find [{problem_name}]")
            self.log(self.make_problem(problem_id, problem_name, problem_url))
        self.write()

    def request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.request_header, cookies=self.request_cookie)

    def title(self) -> str:
        if not self._title:
            self._title = self._title_method()
            print(f"title: {self._title}")
        return self._title

    def get_code(self, problem_id: str) -> str:
        p = problem_id.lower()
        fp = os.path.join(self.code_path, self.contest_id, p, f"{p}.cpp")
        if not os.path.exists(fp):
            print(f"{fp} not found!")
            return ""
        with open(fp, "r") as f:
            return f.read()

    def make_problem(self, problem_id: str, problem_name: str, problem_url: str) -> str:
        code = self.get_code(problem_id)
        return self.template.format(problem_name, self.abbr, self.contest_id, problem_id, problem_url, code)

    def get_contest_number(self) -> str:
        """从标题中提取比赛编号，如 ABC123"""
        title = self.title()
        import re
        # 尝试匹配 ABC\d+ 格式
        match = re.search(r'ABC(\d+)', title)
        if match:
            return f"ABC{match.group(1)}"
        return title  # 如果没有匹配到，返回完整标题

    def write(self):
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 生成文件名：YYYY-MM-DD-ABCXXX.md
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        contest_id = self.get_contest_number()
        filename = f"{date_prefix}-{contest_id}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding='utf-8') as f:
            f.write('\n'.join(self._log))
        print(f"Save in {filepath}")

    def log(self, text:str):
        self._log.append(text)
