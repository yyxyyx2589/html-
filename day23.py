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
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return f"当前时间：{formatted_time}。"

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

function_mapper = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time,
    "get_future_weather": get_future_weather
}

while True:
    user_input = input("请输入：")
    messages.append({"role": "user", "content": user_input})

    completion = function_calling()
    assistant_output = completion.choices[0].message

    if assistant_output.tool_calls:
        messages.append(assistant_output)
        for tool_call in assistant_output.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            function = function_mapper[function_name]
            function_output = function() if arguments == {} else function(arguments)
            messages.append({
                "role": "tool",
                "content": function_output,
                "tool_call_id": tool_call.id
            })
        completion = function_calling()




# import os
# from openai import OpenAI
#
# # 初始化OpenAI客户端，配置阿里云DashScope服务
# client = OpenAI(
#     # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
#     # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
#     api_key=os.getenv('QWEN_API_KEY'),
#     base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
# )
#
# # 定义可用工具列表
# tools = [
#     # 工具1 获取当前时刻的时间
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_time",
#             "description": "获取当前时刻的时间",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": []
#             }
#         }
#     },
#     # 工具2 获取指定城市的天气
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_weather",
#             "description": "当你想查询指定城市的天气时非常有用。",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "城市或县区，比如北京市、杭州市、余杭区等。"
#                     }
#                 },
#                 "required": ["location"]  # 必填参数
#             }
#         }
#     }
# ]
#
# messages = [{"role": "user", "content": input("请输入问题：")}]
#
# # 多模态模型的 message示例
# # messages = [{
# #     "role": "user",
# #     "content": [
# #              {"type": "image_url","image_url": {"url": "https://img.alicdn.com/imgextra/i4/O1CN014CJhzi20NOzo7atOC_!!6000000006837-2-tps-2048-1365.png"}},
# #              {"type": "text", "text": "根据图像上的地点，请问该地点当前的天气"}]
# #     }]
#
# completion = client.chat.completions.create(
#     # 此处以qwen3.6-plus为例，可更换为其它深度思考模型
#     model="qwen-plus",
#     messages=messages,
#     extra_body={
#         # 开启深度思考
#         "enable_thinking": True
#     },
#     tools=tools,
#     parallel_tool_calls=True,
#     stream=True,
#     # 解除注释后，可以获取到token消耗信息
#     # stream_options={
#     #     "include_usage": True
#     # }
# )
#
# reasoning_content = ""  # 定义完整思考过程
# answer_content = ""  # 定义完整回复
# tool_info = []  # 存储工具调用信息
# is_answering = False  # 判断是否结束思考过程并开始回复
# print("=" * 20 + "思考过程" + "=" * 20)
# for chunk in completion:
#     if not chunk.choices:
#         # 处理用量统计信息
#         print("\n" + "=" * 20 + "Usage" + "=" * 20)
#         print(chunk.usage)
#     else:
#         delta = chunk.choices[0].delta
#         # 处理AI的思考过程（链式推理）
#         if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
#             reasoning_content += delta.reasoning_content
#             print(delta.reasoning_content, end="", flush=True)  # 实时输出思考过程
#
#         # 处理最终回复内容
#         else:
#             if not is_answering:  # 首次进入回复阶段时打印标题
#                 is_answering = True
#                 print("\n" + "=" * 20 + "回复内容" + "=" * 20)
#             if delta.content is not None:
#                 answer_content += delta.content
#                 print(delta.content, end="", flush=True)  # 流式输出回复内容
#
#             # 处理工具调用信息（支持并行工具调用）
#             if delta.tool_calls is not None:
#                 for tool_call in delta.tool_calls:
#                     index = tool_call.index  # 工具调用索引，用于并行调用
#
#                     # 动态扩展工具信息存储列表
#                     while len(tool_info) <= index:
#                         tool_info.append({})
#
#                     # 收集工具调用ID（用于后续函数调用）
#                     if tool_call.id:
#                         tool_info[index]['id'] = tool_info[index].get('id', '') + tool_call.id
#
#                     # 收集函数名称（用于后续路由到具体函数）
#                     if tool_call.function and tool_call.function.name:
#                         tool_info[index]['name'] = tool_info[index].get('name', '') + tool_call.function.name
#
#                     # 收集函数参数（JSON字符串格式，需要后续解析）
#                     if tool_call.function and tool_call.function.arguments:
#                         tool_info[index]['arguments'] = tool_info[index].get('arguments',
#                                                                              '') + tool_call.function.arguments
#
# print(f"\n" + "=" * 19 + "工具调用信息" + "=" * 19)
# if not tool_info:
#     print("没有工具调用")
# else:
#     print(tool_info)