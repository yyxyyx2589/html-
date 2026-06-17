import json
import os
from collections import defaultdict
from openai import OpenAI
from datetime import datetime

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )

#  角色定义
ROLES = {
    "qa": {
        "name": "知识助手",
        "prompt": """你是一个知识渊博的问答助手。
回答问题时，输出 JSON 格式：
{"answer": "回答内容", "confidence": "高/中/低", "related_topics": ["相关话题1", "相关话题2"]}""",
        "output": "json"
    },
    "task": {
        "name": "任务管家",
        "prompt": """你是一个任务管理助手。
当用户描述任务时，提取任务信息输出 JSON：
{"task_name": "任务名", "deadline": "截止日期或null", "priority": "高/中/低", "tags": ["标签"]}
当用户查询任务列表时，以文字形式回复。""",
        "output": "json"
    },
    "writing": {
        "name": "写作助手",
        "prompt": """你是一个专业写作助手，擅长各种文体。
用户可以指定写作风格（正式/轻松/文艺/幽默）。
默认风格：轻松自然。""",
        "output": "text"
    },
    "tutor": {
        "name": "学习导师",
        "prompt": """你是一位耐心细致的学习导师，擅长 Python 和 AI 领域。
根据学员水平调整讲解深度，多用类比和例子。
遇到学员不理解时，换一种方式解释。""",
        "output": "text"
    },
    "bill": {
        "name": "账单管家",
        "prompt": """你是一个账单管理助手，负责记录消费和收入。

规则：
1. 当用户描述一笔消费或收入时，调用 record_expense 函数来记录，然后**直接输出 JSON**（amount、category、type、note），不用额外文字。日期由系统自动使用当前时间。
2. **必须调用** query_monthly_summary 函数来获取真实数据，然后**直接输出返回的 JSON**，不要自己编造数字。
3. 用户可以设置月度预算：调用 set_monthly_budget 函数，回复 "月度预算已设为 xxx 元"。

注意：所有输出以函数返回的真实数据为准，不要编造。如果函数返回 total=0 但历史上已有记录，务必先检查函数返回是否正确。""",
        "output": "text"
    }
}

#  Function Calling 基础设施 + 账单管理
#  账单 Schema
EXPENSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'amount':   {'type': 'number',  'description': '金额 (元)'},
        'category': {'type': 'string',
                     'enum': ['餐饮','交通','购物','娱乐','住房','医疗','其他']},
        'note':     {'type': 'string',  'description': '备注说明'},
        'type':     {'type': 'string',  'enum': ['支出', '收入']}
    },
    'required': ['amount', 'category', 'type']
}

# 工具定义
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "record_expense",
            "description": "记录一笔消费或收入，保存到本地文件",
            "parameters": EXPENSE_SCHEMA
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_monthly_summary",
            "description": "查询本月的消费月度汇总，按类别统计金额，含预算提醒",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_monthly_budget",
            "description": "设置月度预算金额",
            "parameters": {
                "type": "object",
                "properties": {
                    "budget": {"type": "number", "description": "预算金额（元）"}
                },
                "required": ["budget"]
            }
        }
    }
]

#  持久化
EXPENSES_FILE = "expenses.json"


def _save_expenses():
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(_expenses, f, ensure_ascii=False, indent=2)


def _load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


_expenses: list[dict] = _load_expenses()
_monthly_budget: float = 5000.0


#  工具函数实现
def record_expense(amount: float, category: str, type: str,
                   note: str = ""):
    """记录一笔账单（消费或收入），日期始终使用当前系统时间"""
    global _expenses
    record = {
        "amount": amount,
        "category": category,
        "type": type,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "note": note or ""
    }
    _expenses.append(record)
    _save_expenses()
    return json.dumps({"ok": True, "record": record}, ensure_ascii=False)


def query_monthly_summary():
    """查询本月消费月度汇总（含预算提醒）"""
    global _expenses, _monthly_budget
    print(f"[debug] _expenses 共 {len(_expenses)} 条: {_expenses}")
    this_month = datetime.now().strftime("%Y-%m")
    monthly = [
        r for r in _expenses
        if r.get("date", "").startswith(this_month) and r.get("type") == "支出"
    ]
    by_category: dict[str, float] = {}
    total = 0.0
    for r in monthly:
        cat = r["category"]
        by_category[cat] = by_category.get(cat, 0) + r["amount"]
        total += r["amount"]

    remaining = _monthly_budget - total
    result = {
        "total": round(total, 2),
        "by_category": by_category,
        "budget": _monthly_budget,
        "remaining": round(remaining, 2),
    }
    #  预算提醒
    ratio = total / _monthly_budget if _monthly_budget > 0 else 0
    if ratio >= 1.0:
        reminder = f"️ 本月预算已超支！已花费 {total:.0f} 元，超出预算 {(-remaining):.0f} 元。"
    elif ratio >= 0.8:
        reminder = f" 预算已使用 {ratio*100:.0f}%（{total:.0f}/{_monthly_budget:.0f} 元），剩余 {remaining:.0f} 元，请注意控制开支。"
    elif ratio >= 0.5:
        reminder = f" 预算已使用 {ratio*100:.0f}%（{total:.0f}/{_monthly_budget:.0f} 元），剩余 {remaining:.0f} 元，预算充足。"
    else:
        reminder = f" 预算使用良好（{ratio*100:.0f}%），剩余 {remaining:.0f} 元。"
    result["reminder"] = reminder
    return json.dumps(result, ensure_ascii=False)


def set_monthly_budget(budget: float):
    """设置月度预算金额"""
    global _monthly_budget
    _monthly_budget = budget
    return json.dumps({"ok": True, "budget": budget}, ensure_ascii=False)


#  函数注册表
function_mapper = {
    "record_expense": record_expense,
    "query_monthly_summary": query_monthly_summary,
    "set_monthly_budget": set_monthly_budget,
}


class PersonalAI:
    def __init__(self):
        self._manual_override = False
        self.current_role = "qa"
        self.histories: dict[str, list] = {role_id: [] for role_id in ROLES}
        self.summaries: dict[str, str] = {role_id: "" for role_id in ROLES}
        self.tasks: list[dict] = []    # 任务列表
        self.turn_counts: dict[str, int] = {role_id: 0 for role_id in ROLES}

    def switch(self, role_id: str):
        if role_id not in ROLES:
            print(f"无效角色ID，可选：{', '.join(ROLES.keys())}")
            return
        self.current_role = role_id
        print(f" 已切换到【{ROLES[role_id]['name']}】")

    def auto_route(self, user_input: str):
        """智能路由：判断用户意图最适合哪个角色，返回 role_id 或 None"""
        # 用户刚手动切换了角色，跳过自动路由
        if self._manual_override:
            self._manual_override = False
            return None

        classify_prompt = """
你是一个意图分类助手，根据用户的输入，判断应该分类为哪一类角色

角色说明：
qa（知识助手）：回答知识性问题、事实查询、科普解释、信息检索
task（任务管家）：创建任务、管理待办、设置截止日期、安排计划
writing（写作助手）：写作、文案、创作、润色、翻译、文章生成
tutor（学习导师）：编程、AI 知识、技术教学、学习辅导
bill（账单管家）：记录消费收入、记账、查询账单、月度汇总、预算管理

只返回一个词：qa / task / writing / tutor / bill
        """
        messages = [
            {"role": "system", "content": classify_prompt},
            {"role": "user", "content": user_input}
        ]
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages
            )
            reply = response.choices[0].message.content.strip().lower()
            if reply in ROLES:
                return reply
        except Exception:
            pass
        return None

    def compress_history(self, role_id: str):
        """摘要压缩：对话超过 10 轮时压缩早期内容为摘要并裁剪历史"""
        history = self.histories[role_id]
        if len(history) < 20:
            return

        compressed = history[:-8]  # 除最近4轮外的全部内容
        msg = [
            {"role": "system", "content": "总结以下对话的核心内容和关键信息，保留重要的用户需求和AI回复要点，简洁全面，不超过200字。"},
            *compressed
        ]
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=msg
            )
            summary = response.choices[0].message.content
            self.summaries[role_id] = summary
            self.histories[role_id] = history[-8:]  # 只保留最近4轮
            print(f"\n📝 对话超过10轮，已生成摘要并自动裁剪历史")
        except Exception:
            pass

    def chat(self, user_input: str):
        role = ROLES[self.current_role]
        history = self.histories[self.current_role]
        summary = self.summaries[self.current_role]

        history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": role["prompt"]}]
        if summary:
            messages.append({"role": "system", "content": f"[历史摘要]\n{summary}"})
        messages.extend(history[-12:])  # 最近6轮

        kwargs = {"model": "deepseek-chat", "messages": messages}
        if role["output"] == "json":
            kwargs["response_format"] = {"type": "json_object"}
        else:
            kwargs["tools"] = TOOLS
            kwargs["tool_choice"] = "auto"

        response = client.chat.completions.create(**kwargs)
        msg = response.choices[0].message

        #  Function Calling 循环
        if msg.tool_calls and role["output"] != "json":
            history.append(msg)  # 保存带 tool_calls 的 assistant 消息

            for tc in msg.tool_calls:
                func_name = tc.function.name
                func_args = json.loads(tc.function.arguments)
                func = function_mapper.get(func_name)
                if func:
                    result = func(**func_args)
                else:
                    result = json.dumps({"error": f"未知函数 {func_name}"}, ensure_ascii=False)
                history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })

            # query_monthly_summary 直接使用函数返回的真实数据，不走第二次 API
            if any(tc.function.name == "query_monthly_summary" for tc in msg.tool_calls):
                reply = result
                history.append({"role": "assistant", "content": reply})
            else:
                # 第二次 API 调用，带上 tool 结果
                messages2 = [{"role": "system", "content": role["prompt"]}]
                messages2.extend(history[-12:])
                kwargs2 = {"model": "deepseek-chat", "messages": messages2}
                if role["output"] == "json":
                    kwargs2["response_format"] = {"type": "json_object"}

                response2 = client.chat.completions.create(**kwargs2)
                reply = response2.choices[0].message.content
                history.append({"role": "assistant", "content": reply})
        else:
            reply = msg.content
            history.append({"role": "assistant", "content": reply})

        # 任务管理：解析并保存任务
        if self.current_role == "task":
            try:
                task_data = json.loads(reply)
                if "task_name" in task_data:
                    task_data["created_at"] = datetime.now().strftime("%m-%d %H:%M")
                    task_data["id"] = len(self.tasks) + 1
                    self.tasks.append(task_data)
            except (json.JSONDecodeError, KeyError):
                pass

        self.compress_history(self.current_role)
        self.turn_counts[self.current_role] += 1
        return reply

    def show_tasks(self):
        if not self.tasks:
            print("暂无任务")
            return
        print("\n=== 任务列表 ===")
        for t in self.tasks:
            deadline = t.get('deadline') or '无截止日期'
            print(f"  [{t['id']}] {t['task_name']} | {t.get('priority','中')}优先 | {deadline}")

    def status(self):
        print(f"\n当前角色：【{ROLES[self.current_role]['name']}】")
        print(f"任务数量：{len(self.tasks)}")
        print(f"账单数量：{len(_expenses)}")
        for rid, count in self.turn_counts.items():
            if count > 0:
                print(f"  {ROLES[rid]['name']}: {count} 轮对话")


def main():
    ai = PersonalAI()
    print("PersonalAI 启动！输入 /help 查看命令\n")

    COMMANDS = {
        "/qa":      ("切换知识助手",    lambda: ai.switch("qa")),
        "/task":    ("切换任务管家",    lambda: ai.switch("task")),
        "/write":   ("切换写作助手",    lambda: ai.switch("writing")),
        "/tutor":   ("切换学习导师",    lambda: ai.switch("tutor")),
        "/bill":    ("切换账单管家",    lambda: ai.switch("bill")),
        "/expenses":("查看所有账单",    lambda: print(json.dumps(_expenses, ensure_ascii=False, indent=2)) if _expenses else print("暂无账单")),
        "/tasks":   ("查看任务列表",    lambda: ai.show_tasks()),
        "/status":  ("查看系统状态",    lambda: ai.status()),
        "/quit":    ("退出",           lambda: exit(0)),
    }

    while True:
        user_input = input(f"\n[{ROLES[ai.current_role]['name']}] > ").strip()
        if not user_input:
            continue

        if user_input in COMMANDS:
            desc, action = COMMANDS[user_input]
            ai._manual_override = True  # 标记手动切换，阻止 auto_route 覆盖
            action()
            continue

        if user_input == "/help":
            for cmd, (desc, _) in COMMANDS.items():
                print(f"  {cmd:12} {desc}")
            continue

        # 智能路由：检测用户意图，必要时自动切换角色
        best_role = ai.auto_route(user_input)
        if best_role and best_role != ai.current_role:
            ai.switch(best_role)

        reply = ai.chat(user_input)

        # 格式化输出
        if ROLES[ai.current_role]["output"] == "json":
            try:
                data = json.loads(reply)
                print(json.dumps(data, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print(reply)
        else:
            print(f"\n{reply}")


if __name__ == "__main__":
    main()
