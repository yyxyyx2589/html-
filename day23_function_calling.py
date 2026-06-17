from openai import OpenAI
from datetime import datetime
import json
import os
import random
import requests

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )

messages = [
    {
        "role": "system",
        "content": """你是一个很有帮助的助手。如果用户只提问关于今天天气的问题，请调用 ‘get_current_weather’ 函数;
        如果用户只提问关于预测天气的问题，请调用 ‘get_future_weather’ 函数;
        不能能同时调用‘get_current_weather’ 函数和‘get_future_weather’ 函数;
        如果用户只要求“查询明天的天气”，则只输出未来一天的天气，不输出后面两天。
     如果用户提问关于时间的问题，请调用‘get_current_time’函数。
     如果用户想获取热门开源项目或最新技术资讯，请调用‘get_news’函数。
     请以友好的语气回答问题。""",
    }
]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"]
            }
        }
    },
{
        "type": "function",
        "function": {
            "name": "get_future_weather",
            "description": "当你想查询指定城市的未来三天天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"]
            }
        }
    },
{
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "当用户想获取热门开源项目或最新技术资讯时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]
def get_current_weather(arguments):

    url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    params_base = {
        'city': arguments["location"],
        'key': '7197563b3bb5d59cd1e2cf3c88965600',
        'extensions': 'base',
        'output': 'json'
    }

    resp = requests.get(url, params=params_base)
    resp_json = resp.json()
    data = resp_json['lives']

    return f"{data[0]['city']}今天的天气是{data[0]['weather']}，温度：{data[0]['temperature']}"

def get_future_weather(arguments):

    url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    params_base = {
        'city': arguments["location"],
        'key': '7197563b3bb5d59cd1e2cf3c88965600',
        'extensions': 'all',
        'output': 'json'
    }

    resp = requests.get(url, params=params_base)
    resp_json = resp.json()
    data = resp_json['forecasts']
    fore = data[0]['casts']
    weather_report=[]

    for i in range(len(fore)-1):
        day_info = (
            f"第{i+1}天的天气情况："
            f"日期：{fore[i+1]['date']}, "
            f"白天天气：{fore[i+1]['dayweather']}, "
            f"晚上天气：{fore[i+1]['nightweather']}, "
            f"白天温度：{fore[i+1]['daytemp']}°C, "
            f"晚上温度：{fore[i+1]['nighttemp']}°C"
        )
        weather_report.append(day_info)
    result = "\n".join(weather_report)
    return result


def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"

def get_news():
    resp = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": "stars:>100",  #搜索条件：stars:>100 表示"star 数大于 100 的仓库"
                "sort": "stars",    #按 stars（星标数）排序
                "order": "desc",    #desc = 降序，最热门的排在前面
                "per_page": 8}     #每页返回 8 条
    )
    data = resp.json()
    news_list = []
    i = 1
    for item in data["items"]:
        news_list.append(f"{i}. {item['full_name']} ⭐{item['stargazers_count']}")
        i += 1
    return "\n".join(news_list)

def function_calling():
    completion = client.chat.completions.create(
        model="deepseek-chat",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        parallel_tool_calls=True
    )
    content = completion.choices[0].message.content
    if content:
        print(content)
    return completion

# 创建一个函数映射表
function_mapper = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time,
    "get_future_weather": get_future_weather,
    "get_news": get_news
}

while True:
    user_input = input("请输入：")
    messages.append({
        "role": "user",
        "content": user_input
    })

    # 第一次调用 — 让模型决定是直接回答还是调用工具
    completion = function_calling()
    assistant_output = completion.choices[0].message

    if assistant_output.tool_calls:
        # 有工具调用：追加 assistant 消息（包含 tool_calls）
        messages.append(assistant_output)

        # 逐一执行工具调用
        for tool_call in assistant_output.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            function = function_mapper[function_name]

            if arguments == {}:
                function_output = function()
            else:
                function_output = function(arguments)

            messages.append({
                "role": "tool",
                "content": function_output,
                "tool_call_id": tool_call.id
            })

        # 第二次调用 — 让模型根据工具结果生成自然语言回答
        completion = function_calling()
    # 如果 assistant_msg.tool_calls 为空，模型已经在第一次调用时直接回答了
    # （function_calling 内部已有 print），无需重复处理
