# personal_ai.py - 完整项目核心

import json
import os
from openai import OpenAI
from datetime import datetime

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )


# ── 角色定义 ────────────────────────────────────────────────
ROLES = {
    "qa": {
        "name": "知识助手",
        "prompt": """你是一个知识渊博的问答助手。
回答问题时，输出 JSON 格式：
{"answer": "回答内容", "confidence": "高/中/低", "related_topics": ["相关话题1", "相关话题2"]}""",
        "output": "json",
        "tools": """工具tool。当用户想要获取当前时间相关信息时，调用get_current_time函数。"""
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
    }
}

class PersonalAI:
    def __init__(self):
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
        print(f"✓ 已切换到【{ROLES[role_id]['name']}】")

    def auto_route(self,user_input: str):
        classify_prompt="""
        你是一个意图分类助手，根据用户的输入，判断应该分类为哪一类角色
角色说明：
qa（知识助手）：回答知识性问题、事实查询、科普解释、信息检索
task（任务管家）：创建任务、管理待办、设置截止日期、安排计划
writing（写作助手）：写作、文案、创作、润色、翻译、文章生成
tutor（学习导师）：编程、AI 知识、技术教学、学习辅导

只返回一个词：qa / task / writing / tutor
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
            reply = response.choices[0].message.content
            if reply in ROLES:
                return reply
        except Exception:
            pass

    def compress_history(self,role_id: str):
        history = self.histories[role_id]
        if len(history) <5:
            return

        compressed_history = history[:-2]
        msg=[{"role": "system", "content": f"总结以下对话{compressed_history}的核心内容和关键信息，保留重要的点和AI回复的关键内容，简洁全面，不超过200字"}]

        try:
            response=client.chat.completions.create(
                model="deepseek-chat",
                messages=msg
            )
            summary=response.choices[0].message.content
            self.summaries[role_id] = summary
            self.histories[role_id]=history[-2:]
            print(f"摘要：{summary} \n 最近历史：{history[-2:]}")
        except Exception:
            pass


    def chat(self, user_input: str) -> str:
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

        response = client.chat.completions.create(**kwargs)
        reply = response.choices[0].message.content
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
            action()
            continue

        if user_input == "/help":
            for cmd, (desc, _) in COMMANDS.items():
                print(f"  {cmd:12} {desc}")
            continue

        # 自动路由：检测用户意图，必要时切换角色
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