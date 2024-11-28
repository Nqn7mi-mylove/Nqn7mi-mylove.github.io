from .base import BaseParser

class Atcoder(BaseParser):
    
    @property
    def code_path(self) -> str:
        return "code/AtCoder"

    @property
    def request_cookie(self): # 有时候比赛剩下不会做，想写题解，但由于比赛还没结束，需要登录才能看题，可以F12获取登录cookie
        return {
            "REVEL_SESSION": ""
        }

    @property
    def name(self) -> str:
        return "atcoder"

    def _title_method(self) -> str:
        contest_name = self.soup.head.title.get_text().strip("Tasks - ")
        # 从contest_name中提取比赛号（假设格式为"ABC123"或"AtCoder Beginner Contest 123"等）
        import re
        # 尝试匹配两种可能的格式
        abc_match = re.search(r'ABC(\d+)', contest_name)
        full_match = re.search(r'AtCoder Beginner Contest (\d+)', contest_name)
        
        if abc_match:
            contest_number = abc_match.group(1)
            return f"AtCoder Beginner Contest {contest_number} Solution"
        elif full_match:
            contest_number = full_match.group(1)
            return f"AtCoder Beginner Contest {contest_number} Solution"
        return f"{contest_name} Solution"  # 如果不是ABC比赛，返回原始名称

    @property
    def problem_table(self) -> str:
        return "table"

    @property
    def contest_id(self) -> str:
        return self.url.split('/')[-2]
