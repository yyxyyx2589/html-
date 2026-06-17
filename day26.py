# from enum import Enum
# from dataclasses import dataclass,field
# from datetime import datetime
# class SessionState(Enum):
#     START="初始化"
#     IDLE="空闲"
#     ACTIVATE="活跃"
#     WAITING = "等待"
#     SUMMARIZING="摘要中"
#     END="已结束"
#
# class ConversationSession:
#     def __init__(self, session_id, role_name, tags=None):
#         self.session_id = session_id
#         self.role_name = role_name
#         self.tags = tags if tags is not None else []
#         self.state = SessionState.START  # 初始状态设为 START
#         self.turn_count = 0  # 对话轮数初始化为 0
#
#     def start(self):
#         """启动会话，将状态切换为 ACTIVATE"""
#         self.state = SessionState.ACTIVATE
#
#     def end(self):
#         """关闭会话，将状态切换为 END"""
#         self.state = SessionState.END
#
#     def __str__(self):
#         """自定义打印格式，方便查看当前会话的状态和轮数"""
#         return (f"[Session ID: {self.session_id} | Role: {self.role_name} | "
#                 f"State: {self.state.value} | Turns: {self.turn_count}]")
#
# #创建一条会话
# session=ConversationSession(
#     session_id="sess_001",
#     role_name="学习助手",
#     tags=["python","面试备考"]
# )
#
# #打印初始状态 空闲
# print("初始化会话：",session)
#
# #启动会话
# session.start()
# print("会话启动：",session)
#
# #模拟对话3轮，更新轮数
# session.turn_count=3
# session.state=SessionState.WAITING
# print("聊完3轮，等待用户：",session)
#
# #执行摘要 切换状态
# session.state=SessionState.SUMMARIZING
# print("正在生成摘要：",session)
#
# #关闭会话
# session.end()
# print("会话结束：",session)



#多角色管理系统实现
from openai import OpenAI
import json
import os
import re
import requests

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )

class RoleManager:
    """多角色管理器"""

    def __init__(self, model: str = "deepseek-chat"):
        self.model = model
        self.roles: dict[str, dict] = {}        # 角色库
        self.role_histories: dict[str, list] = {}  # 各角色独立历史
        self.current_role: str | None = None    # 当前角色

    def register_role(self, role_id: str, name: str, system_prompt: str, description: str = ""):
        """注册一个角色"""
        self.roles[role_id] = {
            "name":          name,
            "system_prompt": system_prompt,
            "description":   description
        }
        self.role_histories[role_id] = []
        print(f"角色 [{name}] 注册成功 (id: {role_id})")

    def switch_role(self, role_id: str, keep_history: bool = False):
        """切换当前角色"""
        if role_id not in self.roles:
            raise ValueError(f"角色 {role_id} 不存在")

        old_role = self.current_role
        self.current_role = role_id

        if not keep_history:
            # 切换时可选择是否清空该角色的历史
            pass

        role_name = self.roles[role_id]["name"]
        print(f"角色切换：{self.roles[old_role]['name'] if old_role else '无'} → {role_name}")

    def chat(self, user_input: str) -> str:
        """用当前角色对话"""
        if self.current_role is None:
            raise RuntimeError("未设置当前角色，请先调用 switch_role()")

        role = self.roles[self.current_role]
        history = self.role_histories[self.current_role]

        history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": role["system_prompt"]}] + history

        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        return reply

    def auto_route(self, user_input: str) -> str:
        """自动路由：让 AI 判断该用哪个角色，然后切换并回答"""
        role_descriptions = "\n".join(
            f"- {rid}: {info['name']} - {info['description']}"
            for rid, info in self.roles.items()
        )

        routing_prompt = f"""根据用户输入，选择最合适的角色ID来回答。
只输出角色ID，不要任何其他内容。

可用角色：
{role_descriptions}

用户输入：{user_input}
"""
        routing_response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": routing_prompt}]
        )
        role_id = routing_response.choices[0].message.content.strip()

        # 容错：如果返回的不是有效 role_id，用第一个角色
        if role_id not in self.roles:
            role_id = list(self.roles.keys())[0]

        self.switch_role(role_id)
        return self.chat(user_input)

    def list_roles(self):
        """显示所有角色"""
        print("\n=== 已注册角色 ===")
        for rid, info in self.roles.items():
            marker = " ← 当前" if rid == self.current_role else ""
            print(f"  [{rid}] {info['name']}: {info['description']}{marker}")


# 构建一个客服系统
manager = RoleManager()

manager.register_role(
    "knowledge_teacher",
    "知识讲解老师",
    "你是一个大学计算机专业的老师，拥有浙大的计算机博士学位，精通人工智能、机器学习方向，对学生的问题耐心回答，并且会友好的举例子说明问题。",
    "详细解释概念"
)

manager.register_role(
    "quiz_master",
    "出题考官",
    "你是一个出题考官，会对学生出判断题，选择题，考察学生的能力。",
    "出判断题/选择题考察理解"
)

manager.register_role(
    "study_planner",
    "学习规划师",
    "你是一个学习规划师，可以根据学生量身定制学习计划。",
    "制定复习计划"
)


manager.list_roles()

# 自动路由测试
test_inputs = [
    "我的软件安装后报错，提示 dll 文件缺失",
    "你们产品多少钱？有没有优惠？",
    "我买了你们产品根本不能用，要退款！"
]

def extract_key_facts(conversation_history: list[dict], client) -> dict:
    """从对话中提取关键事实，用于后续会话"""
    history_text = "\n".join(
        f"{'用户' if m['role']=='user' else 'AI'}: {m['content']}"
        for m in conversation_history
    )

    prompt = f"""从以下对话中提取关键信息，输出 JSON 格式：

{history_text}

输出格式：
{{
    "user_name": "用户姓名（如果提到）",
    "preferences": ["偏好列表"],
    "constraints": ["限制条件列表"],
    "goals": ["目标列表"],
    "important_facts": ["其他重要事实"]
}}"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# for user_input in test_inputs:
#     print(f"\n用户：{user_input}")
#     reply = manager.auto_route(user_input)
#     print(f"AI [{manager.roles[manager.current_role]['name']}]：{reply[:100]}...")

# while True:
#     user_input_role = input("请输入角色：")
#     user_input = input("请输入内容：")
#     manager.switch_role(user_input_role)
#     print(manager.chat(user_input))

class SummaryConversationManager:
    """带摘要压缩的对话管理器"""

    def __init__(
        self,
        system_prompt: str,
        model: str = "deepseek-chat",
        compress_every: int = 6,   # 每 6 轮压缩一次
        keep_recent: int = 3       # 压缩后保留最近 3 轮原文
    ):
        self.system_prompt = system_prompt
        self.model = model
        self.compress_every = compress_every
        self.keep_recent = keep_recent
        self.history: list[dict] = []
        self.summary: str = ""     # 历史摘要（压缩的结果）
        self.turn_count = 0

    def _compress(self):
        """压缩历史：把早期历史总结成摘要"""
        print("\n[系统] 正在压缩对话历史...")

        # 准备要压缩的部分（保留最近 keep_recent 轮）
        keep_count = self.keep_recent * 2
        to_compress = self.history[:-keep_count] if len(self.history) > keep_count else []
        recent = self.history[-keep_count:] if len(self.history) > keep_count else self.history

        if not to_compress:
            return  # 没有需要压缩的内容

        # 生成新摘要
        history_text = "\n".join(
            f"{'用户' if m['role']=='user' else 'AI'}: {m['content']}"
            for m in to_compress
        )

        existing_summary = f"已有摘要：\n{self.summary}\n\n" if self.summary else ""

        compress_prompt = f"""{existing_summary}请将以下对话补充摘要到已有摘要中，保留关键事实、用户偏好、重要决策：

{history_text}

要求：
1. 摘要控制在200字以内
2. 用第三人称描述（"用户表示..."）
3. 突出关键信息"""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": compress_prompt}]
        )
        self.summary = response.choices[0].message.content

        # 用摘要替换旧历史
        self.history = recent
        print(f"[系统] 压缩完成，历史从 {len(to_compress)+len(recent)} 条压缩至 {len(recent)} 条")
        print(f"[摘要] {self.summary[:80]}...")

    def chat(self, user_input: str) -> str:
        """对话，自动触发摘要压缩"""
        self.turn_count += 1
        self.history.append({"role": "user", "content": user_input})

        # 构建消息：system + 摘要（如有）+ 近期历史
        messages = [{"role": "system", "content": self.system_prompt}]

        if self.summary:
            messages.append({
                "role": "system",
                "content": f"[对话摘要 - 之前聊过的内容]\n{self.summary}"
            })

        messages.extend(self.history)

        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})

        # 达到压缩阈值时触发压缩
        if self.turn_count % self.compress_every == 0:
            self._compress()

        return reply


# 测试长对话
mgr = SummaryConversationManager(
    system_prompt="你是一个旅游规划师，帮用户规划旅行。记住用户提到的偏好和需求。",
    compress_every=4,
    keep_recent=2
)

conversations = [
    "我想去日本旅游，喜欢安静的地方，不喜欢人多的景点",
    "我的预算大概是1万元，行程10天",
    "我对历史文化很感兴趣，喜欢寺庙和神社",
    "我不能吃海鲜，对花粉过敏",
    "出发时间大概是明年三月",
    "请给我推荐一个详细的10天行程"  # 这时已经压缩过了，看看 AI 还记得多少
]

for msg in conversations:
    print(f"\n用户：{msg}")
    reply = mgr.chat(msg)
    print(f"AI：{reply[:120]}...")

facts=extract_key_facts(mgr.history,client)
print(json.dumps(facts, indent=2,ensure_ascii=False))









