# from openai import OpenAI
# import json
# import os
# import re
# import requests
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor
# import time  # 新增计时模块
#
# client=OpenAI(api_key=os.getenv("DS_API_KEY"),
#               base_url='https://api.deepseek.com/v1'
#               )
#
# messages = [
#     {
#         "role": "system",
#         "content": """你是一个很有帮助的助手。如果用户只提问关于今天天气的问题，请调用 ‘get_current_weather’ 函数;
#         如果用户只提问关于预测天气的问题，请调用 ‘get_future_weather’ 函数;
#         不能能同时调用‘get_current_weather’ 函数和‘get_future_weather’ 函数;
#         如果用户只要求“查询明天的天气”，则只输出未来一天的天气，不输出后面两天。
#      如果用户提问关于时间的问题，请调用‘get_current_time’函数。
#      请以友好的语气回答问题。""",
#     }
# ]
#
#
# tools = [
#     # 工具2：获取当前时间
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_time",
#             "description": "当用户询问现在几点、当前日期、当前时间时调用，不需要传入任何参数",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": []
#             },
#         },
#     },
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
#                         "description": "城市或县区，比如北京市、杭州市、余杭区等。",
#                     }
#                 },
#                 "required": ["location"]
#             }
#         }
#     },
# {
#         "type": "function",
#         "function": {
#             "name": "get_future_weather",
#             "description": "当你想查询指定城市的未来三天天气时非常有用。",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "城市或县区，比如北京市、杭州市、余杭区等。",
#                     }
#                 },
#                 "required": ["location"]
#             }
#         }
#     }
# ]
#
# def get_current_weather(arguments):
#     url = 'https://restapi.amap.com/v3/weather/weatherInfo'
#     params_base = {
#         'city': arguments["location"],
#         'key': '7197563b3bb5d59cd1e2cf3c88965600',
#         'extensions': 'base',
#         'output': 'json'
#     }
#     resp = requests.get(url, params=params_base)
#     resp_json = resp.json()
#     data = resp_json['lives']
#     return f"{data[0]['city']}今天的天气是{data[0]['weather']}，温度：{data[0]['temperature']}"
#
# def get_future_weather(arguments):
#     url = 'https://restapi.amap.com/v3/weather/weatherInfo'
#     params_base = {
#         'city': arguments["location"],
#         'key': '7197563b3bb5d59cd1e2cf3c88965600',
#         'extensions': 'all',
#         'output': 'json'
#     }
#     resp = requests.get(url, params=params_base)
#     resp_json = resp.json()
#     data = resp_json['forecasts']
#     fore = data[0]['casts']
#     weather_report=[]
#     for i in range(len(fore)-1):
#         day_info = (
#             f"第{i+1}天的天气情况："
#             f"日期：{fore[i+1]['date']}, "
#             f"白天天气：{fore[i+1]['dayweather']}, "
#             f"晚上天气：{fore[i+1]['nightweather']}, "
#             f"白天温度：{fore[i+1]['daytemp']}°C, "
#             f"晚上温度：{fore[i+1]['nighttemp']}°C"
#         )
#         weather_report.append(day_info)
#     result = "\n".join(weather_report)
#     return result
#
# def get_current_time(arguments):
#     """
#     获取当前本地日期时间
#     arguments 为空字典，不需要传参
#     """
#     now = datetime.now()
#     time_str = now.strftime("%Y年%m月%d日 %H:%M:%S 星期%w")
#     return f"\n======= 当前系统时间 =======\n{time_str}\n==========================\n"
#
#
#
# def get_response(messages):
#     start = time.time()
#     completion = client.chat.completions.create(
#         model="deepseek-chat",
#         extra_body={"enable_thinking": False},
#         messages=messages,
#         tools=tools,
#         parallel_tool_calls=True
#     )
#     cost = round(time.time() - start, 3)
#     print(f"\n[LLM接口耗时] {cost} s")
#     return completion
#
# # ====================== 3. 工具注册表 + 分发器 ======================
# tool_registry = {
#     "get_current_weather": get_current_weather,
#     "get_current_time": get_current_time,
#     "get_future_weather": get_future_weather
# }
#
#
# def dispatch_tool(func_name, func_args):
#     """通用工具分发器，自动匹配函数"""
#     if func_name not in tool_registry:
#         return f"❌ 不存在工具：{func_name}"
#     return tool_registry[func_name](func_args)
#
#
# # 线程池专用：单个工具执行包装函数
# def run_single_tool(tool_call):
#     """接收单个tool_call，执行工具并返回id+结果"""
#     func_name = tool_call.function.name
#     func_args = json.loads(tool_call.function.arguments)
#     print(f"[并行线程] 调用工具 [{func_name}]，参数：{func_args}")
#     res = dispatch_tool(func_name, func_args)
#     return {
#         "tool_call_id": tool_call.id,
#         "content": res
#     }
#
# while True:
#     total_start = time.time()  # 全局总计时起点
#     user_input = input("请输入：")
#     messages.append({"role": "user", "content": user_input})
#
#     completion = get_response(messages)
#     assistant_output = completion.choices[0].message
#
#     if assistant_output.content is None:
#         assistant_output.content = ""
#     messages.append(assistant_output)
#
#     if not assistant_output.tool_calls:
#         print(f"无需调用工具，直接回复：{assistant_output.content}")
#     else:
#         print(f"\n模型一次性下发 {len(assistant_output.tool_calls)} 个工具任务，开启多线程并行执行...")
#         tool_start = time.time()
#         # 创建线程池，最大并发10个线程
#         with ThreadPoolExecutor(max_workers=10) as pool:
#             # map自动把每个tool_call分给不同线程同时执行
#             all_tool_results = list(pool.map(run_single_tool, assistant_output.tool_calls))
#         tool_cost = round(time.time() - tool_start, 3)
#         print(f"\n[全部工具并行执行总耗时] {tool_cost} s")
#
#         # 循环把并行拿到的全部工具结果存入对话上下文
#         for item in all_tool_results:
#             print(f"\n[工具返回结果]\n{item['content']}")
#             messages.append({
#                 "role": "tool",
#                 "tool_call_id": item["tool_call_id"],
#                 "content": item["content"]
#             })
#
#         # 所有工具并行执行完成，统一请求大模型整合全部信息
#         final_response = get_response(messages)
#         final_ans = final_response.choices[0].message.content
#         print("\n===== 助手最终整合回复 =====")
#         print(final_ans)
#
#         # 全局总耗时计算
#         total_cost = round(time.time() - total_start, 3)
#         print(f"\n===================== 程序整体总耗时：{total_cost} 秒 =====================")
#
#
#





from openai import OpenAI
import json
import os
import re
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time  # 新增计时模块
from pydantic import BaseModel,Field,ValidationError

class Get_news(BaseModel):
    mode:str = Field(default='1',pattern=r'^[12]$',description='1=爬取最新技术，2=爬取最热门技术')


def get_news(params=None):
    """
    根据参数获取GitHub热门或最新技术
    params: 包含 mode 字段的字典
    """
    # 设置默认值
    mode = "2"  # 默认为热门
    if params and isinstance(params, dict):
        mode = params.get("mode", "2")

    # 构建搜索参数
    search_params = {
        "q": "stars:>100",  # 基础搜索条件
        "order": "desc",
        "per_page": 8
    }

    if mode == "1":
        search_params["sort"] = "created"  # 最新
    else:
        search_params["sort"] = "stars"  # 最热门 (默认)

    resp = requests.get(
        "https://api.github.com/search/repositories",
        params=search_params
    )
    data = resp.json()
    news_list = []
    i = 1
    for item in data["items"]:
        news_list.append(f"{i}. {item['full_name']} ⭐{item['stargazers_count']}")
        i += 1
    return "\n".join(news_list)

def pydantic_to_tool_definition(model,name,desc):
    json_schema = model.model_json_schema()
    return {
        'type':'function',
        'function':{
            'name':name,
            'description':desc,
            'parameters':json_schema
        }
    }

tools=[
    pydantic_to_tool_definition(
        Get_news,
        'get_news',
        '到github网站去爬取页面的最新或热门技术资讯。如果用户没有明确指定，请默认使用 mode="2"（最热门技术）。'
    )
]

print("\n自动生成的tools工具定义：")
print(json.dumps(tools,indent=2,ensure_ascii=False))


client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )

messages = [
    {
        "role": "system",
        "content": """你是一个很有帮助的助手。如果用户提问到相关网站去爬取github的最新热门技术资讯，请调用 ‘get_news’ 函数;
        注意：如果用户输入了666，请故意将 mode 参数设置为 '999' 来测试系统。
        """,
    }
]


def get_response(messages):
    start = time.time()
    completion = client.chat.completions.create(
        model="deepseek-chat",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        parallel_tool_calls=True
    )
    cost = round(time.time() - start, 3)
    print(f"\n[LLM接口耗时] {cost} s")
    return completion

# ====================== 3. 工具注册表 + 分发器 ======================
tool_registry = {
    "get_news": (get_news, Get_news) ,

}


def dispatch_tool(func_name, func_args):
    """通用工具分发器，自动匹配函数"""
    if func_name not in tool_registry:
        return f"❌ 不存在工具：{func_name}"
    tool_func,param_model=tool_registry[func_name]
    try:
        valid_params=param_model(**func_args)
        clean_args = valid_params.model_dump()
        return tool_func(clean_args)
    except ValidationError as e:
        return f"参数校验失败：{e}"



# 线程池专用：单个工具执行包装函数
def run_single_tool(tool_call):
    """接收单个tool_call，执行工具并返回id+结果"""
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)
    print(f"[并行线程] 调用工具 [{func_name}]，参数：{func_args}")
    res = dispatch_tool(func_name, func_args)
    return {
        "tool_call_id": tool_call.id,
        "content": res
    }

while True:
    total_start = time.time()  # 全局总计时起点
    user_input = input("请输入：")
    messages.append({"role": "user", "content": user_input})

    completion = get_response(messages)
    assistant_output = completion.choices[0].message

    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)

    if not assistant_output.tool_calls:
        print(f"无需调用工具，直接回复：{assistant_output.content}")
    else:
        print(f"\n模型一次性下发 {len(assistant_output.tool_calls)} 个工具任务，开启多线程并行执行...")
        tool_start = time.time()
        # 创建线程池，最大并发10个线程
        with ThreadPoolExecutor(max_workers=10) as pool:
            # map自动把每个tool_call分给不同线程同时执行
            all_tool_results = list(pool.map(run_single_tool, assistant_output.tool_calls))
        tool_cost = round(time.time() - tool_start, 3)
        print(f"\n[全部工具并行执行总耗时] {tool_cost} s")

        # 循环把并行拿到的全部工具结果存入对话上下文
        for item in all_tool_results:
            print(f"\n[工具返回结果]\n{item['content']}")
            messages.append({
                "role": "tool",
                "tool_call_id": item["tool_call_id"],
                "content": item["content"]
            })

        # 所有工具并行执行完成，统一请求大模型整合全部信息
        final_response = get_response(messages)
        final_ans = final_response.choices[0].message.content
        print("\n===== 助手最终整合回复 =====")
        print(final_ans)

        # 全局总耗时计算
        total_cost = round(time.time() - total_start, 3)
        print(f"\n===================== 程序整体总耗时：{total_cost} 秒 =====================")



