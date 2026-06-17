from openai import OpenAI
import json
import os
import re
import requests



class ConversationManager:
    """多轮对话管理器"""

    def __init__(
        self,
        system_prompt: str,
        model: str = "deepseek-chat",
        max_history: int = 4,       # 最多保留几轮历史
        max_tokens: int = 4000       # 历史区预留 token 上限（粗略估算）
    ):
        self.system_prompt = system_prompt
        self.model = model
        self.max_history = max_history
        self.max_tokens = max_tokens
        self.history: list[dict] = []
        self.turn_count = 0

    def _estimate_tokens(self, text: str) -> int:
        """粗略估算 token 数（中文约1.5字/token，英文约4字/token）"""
        chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_count = len(text) - chinese_count
        return int(chinese_count / 1.5 + other_count / 4)

    def _trim_history(self):
        """修剪历史记录：超过限制则删除最早的对话轮"""
        # 先按轮数限制
        while len(self.history) > self.max_history * 2:
            self.history.pop(0)  # 删除最早的 user
            self.history.pop(0)  # 删除对应的 assistant

        # 再按 token 估算限制
        total_tokens = sum(self._estimate_tokens(m["content"]) for m in self.history)
        while total_tokens > self.max_tokens and len(self.history) >= 2:
            removed_user = self.history.pop(0)
            removed_ai   = self.history.pop(0)
            total_tokens -= (
                self._estimate_tokens(removed_user["content"]) +
                self._estimate_tokens(removed_ai["content"])
            )

    def chat(self, user_input: str, verbose: bool = False) -> str:
        """发送消息，自动管理上下文"""
        self.turn_count += 1
        self.history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": self.system_prompt}] + self.history

        if verbose:
            total_msg_tokens = sum(self._estimate_tokens(m["content"]) for m in messages)
            print(f"[轮次 {self.turn_count}] 历史轮数: {len(self.history)//2}, 预计 token: ~{total_msg_tokens}")

        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})

        # 添加后再修剪（保证本轮完整）
        self._trim_history()
        return reply


class SummaryConversationManager:
    """带摘要压缩的对话管理器"""

    def __init__(
        self,
        system_prompt: str,
        model: str = "qwen-turbo",
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

