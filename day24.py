from openai import OpenAI
import json
import os
import re
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time  # 新增计时模块

# ====================== 1. 工具1：高德天气查询 ======================
KEY = "769e0205a897baeeb8c0c0289a8f8be8"


def get_current_weather(arguments):
    city = arguments.get("location", "").strip()
    option = arguments.get("mode", "1")
    url = "https://restapi.amap.com/v3/weather/weatherInfo"

    # 中文名校验
    if not city:
        return "❌ 错误：城市名称不能为空"
    if not re.search(r'[\u4e00-\u9fa5]', city):
        return "❌ 错误：请输入中文城市名，例如南昌市、北京市"
    if option not in ("1", "2"):
        return "⚠️ 错误：仅支持模式1(实时天气) / 模式2(4天预报)"

    # 实时实况天气
    if option == '1':
        params_base = {
            "city": city,
            "key": KEY,
            "extensions": "base",
            "output": "json"
        }
        try:
            res_base = requests.get(url, params=params_base, timeout=10)
            data_base = res_base.json()
            if data_base["status"] != "1":
                return f"❌ 查询失败：未找到城市【{city}】"
            if not data_base["lives"]:
                return f"❌ 查询失败：无{city}实时天气数据"
            weather = data_base["lives"][0]
            return (
                f"\n======= {weather['city']} 当前天气 =======\n"
                f"天气：{weather['weather']}\n"
                f"温度：{weather['temperature']}℃\n"
                f"风向：{weather['winddirection']}风 {weather['windpower']}级\n"
                f"湿度：{weather['humidity']}%\n"
                f"更新时间：{weather['reporttime']}\n"
                "======================================\n"
            )
        except Exception:
            return "🌐 网络异常，天气接口请求失败"

    # 未来4天预报
    elif option == '2':
        params_all = {
            "city": city,
            "key": KEY,
            "extensions": "all",
            "output": "json"
        }
        try:
            res_all = requests.get(url, params=params_all, timeout=10)
            data_all = res_all.json()
            if data_all["status"] != "1":
                return f"❌ 查询失败：未找到城市【{city}】"
            if not data_all["forecasts"]:
                return f"❌ 查询失败：无{city}预报数据"
            forecasts = data_all["forecasts"][0]["casts"]
            text = f"\n======= {city} 未来4天天气预报 =======\n"
            for day in forecasts:
                text += (
                    f"【{day['date']} 星期{day['week']}】\n"
                    f"白天：{day['dayweather']}，最高 {day['daytemp']}℃\n"
                    f"夜间：{day['nightweather']}，最低 {day['nighttemp']}℃\n"
                    f"风向：{day['daywind']}，风力 {day['daypower']} 级\n"
                    "----------------------------------------\n"
                )
            return text
        except Exception:
            return "🌐 网络异常，天气接口请求失败"


# ====================== 2. 工具2：获取当前系统时间 ======================
def get_current_time(arguments):
    """
    获取当前本地日期时间
    arguments 为空字典，不需要传参
    """
    now = datetime.now()
    time_str = now.strftime("%Y年%m月%d日 %H:%M:%S 星期%w")
    return f"\n======= 当前系统时间 =======\n{time_str}\n==========================\n"


# ====================== 3. 工具注册表 + 分发器 ======================
tool_registry = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time

}


def dispatch_tool(func_name, func_args):
    """通用工具分发器，自动匹配函数"""
    if func_name not in tool_registry:
        return f"❌ 不存在工具：{func_name}"
    return tool_registry[func_name](func_args)


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


# ====================== 4. LLM客户端初始化 ======================
client = OpenAI(
    api_key=os.getenv("DS_API_KEY"),
    base_url='https://api.deepseek.com/v1',
)

# ====================== 5. 工具列表定义 ======================
tools = [
    # 工具1：天气查询
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "查询指定中文城市的天气，1=实时实况天气，2=未来4天天气预报",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "中文城市/区县，如南昌市、上海市"
                    },
                    "mode": {
                        "type": "string",
                        "description": "查询模式：'1'实时天气 / '2'四天预报，默认1",
                        "enum": ["1", "2"]
                    }
                },
                "required": ["location"]
            },
        },
    },
    # 工具2：获取当前时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当用户询问现在几点、当前日期、当前时间时调用，不需要传入任何参数",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            },
        },
    }
]


# ====================== 6. LLM请求封装 ======================
def get_response(messages):
    start = time.time()
    completion = client.chat.completions.create(
        model="qwen3.6-plus",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        parallel_tool_calls=True  # 关键：允许模型一次返回多个工具任务
    )
    cost = round(time.time() - start, 3)
    print(f"\n[LLM接口耗时] {cost} s")
    return completion


# ====================== 7. 主逻辑：线程池并行执行全部工具 ======================
if __name__ == "__main__":
    total_start = time.time()  # 全局总计时起点

    # 测试提问：同时触发时间+多个城市天气工具
    USER_QUESTION = "现在几点了？帮我查北京实时天气和上海4天天气预报"
    messages = [{"role": "user", "content": USER_QUESTION}]

    response = get_response(messages)
    assistant_output = response.choices[0].message
    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)

    # 无工具调用，直接输出
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