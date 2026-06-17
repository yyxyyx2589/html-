from openai import OpenAI
import json
import os
import re
import requests
from jsonschema import validate,ValidationError
import xml.etree.ElementTree as ET

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )


# structured_prompt="""
# <task>
#     <role>你是专业的代码工程师</role>
#     <input>
#         <code language="python">
#             def add(a,b):
#                 return a-b
#         <code>
#     <input>
#     <requirements>
#         <item>找出代码中的bug</item>
#         <item>给出修复建议</item>
#         <item>评估代码质量</item>
#     <requirements>
#     <output_format>
#         JSON:{"bug":"...","fix":"...","score":数字}
#     </output_format>
# </task>
# """
#
# response=client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[{'role': 'user', 'content': structured_prompt}],
#     response_format={"type":"json_object"}
# )
# print(json.loads(response.choices[0].message.content))



news_prompt="""
<task>
    <role>你是专业的英文新闻分析师</role>
    <input>
        City Launches Free Public Wi-Fi in Downtown Parks
        Author: Emily Carter  
        Date: June 12, 2026  
        Summary: Oakridge has introduced solar-powered public Wi-Fi in its downtown parks to improve digital access, with a three-month trial underway.
        Body:
        The city of Oakridge has launched free high-speed Wi-Fi across five downtown parks to bridge the digital divide. Mayor Linda Torres announced that the solar-powered network will be available daily from 6 a.m. to midnight. While officials estimate over 10,000 monthly users and assure no personal data will be collected, some residents have raised privacy concerns. A three-month trial is now underway to evaluate usage before making the project permanent.
    <input>
    <requirements>
        <item>对新闻的标题、作者、时间、摘要进行分析</item>
        <item>给出新闻的关键词3-5个</item>
    <requirements>
    <output_format>
        JSON:{"title":"...",
        "author":"...",
        "time":"...",
        "abstract":"...",
        "keywords":"..."
        }
    </output_format>
</task>
"""

news_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "新闻标题"
        },
        "author": {
            "type": "string",
            "description": "新闻作者"
        },
        "time": {
            "type": "string",
            "description": "新闻时间"
        },
        "abstract":  {"type": "string",  "description": "新闻的摘要"},
        "keywords": {
            "type": "string",
            "description": "新闻关键词"
        }
    },
    "required": ["author", "time", "abstract", "keywords"]
}

def validate_ai_output(data:dict,schema:dict)->tuple[bool,str]:
    try:
        validate(instance=data,schema=schema)
        return True,"通过"
    except ValidationError as e:
        return False,f"校验失败:{e.message}"


def analyze_news_with_schema(prompt: str, schema: dict) -> dict:
    """使用 Schema 约束提取新闻信息"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # 确保模型名称正确
            messages=[{'role': 'user', 'content': news_prompt}],
            response_format={"type": "json_object"}
        )

        # 获取模型输出
        content = response.choices[0].message.content
        data = json.loads(content)

        # 校验 JSON 结构
        validate(instance=data, schema=schema)
        return data

    except Exception as e:
        print(f"Error: {e}")
        return {}

result = analyze_news_with_schema(news_prompt, news_schema)
print(json.dumps(result, indent=2, ensure_ascii=False))