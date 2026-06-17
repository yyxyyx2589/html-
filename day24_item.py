from openai import OpenAI
import json
import os
import re
import requests
from datetime import datetime
from datetime import date
from concurrent.futures import ThreadPoolExecutor
import time  # 新增计时模块
from pydantic import BaseModel,Field,ValidationError

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )

messages = [
    {
        "role": "system",
        "content": """你是一个很有帮助的助手。只要用户在对话中提供了两个数字，无论是否明确指定了计算方式，都必须调用 'number_calculate' 函数。
                        如果用户未指定计算方式，请默认使用加法（mode='1'）进行计算。;
                如果用户在对话中提供了一个文件名，则调用'read_file'函数来读取文件内容。
                如果用户在对话中提供了两个日期，则调用'date_calculate'函数来进行计算两个日期的差值;如果只提供一个日期，则另一个日期默认使用当前时间。
        """,
    }
]


class Number_calculate(BaseModel):
    number1: int=Field(description='1号数字')
    number2: int = Field(description='2号数字')
    mode:str = Field(default='1',pattern=r'^[12345]$',description='对两个数字进行计算，1=加，2=减，3=乘，4=除，5=开方')

class Read_file(BaseModel):
    file_name: str = Field(description='在当前根目录下寻找相应名字的文件，并读取其内容')

class Date_calculate(BaseModel):
    date1: str = Field(default=f'{date.today().strftime("%Y-%m-%d")}',description='用户给的第一个日期，如果没给出日期则获取当前时间')
    date2: str = Field(default=f'{date.today().strftime("%Y-%m-%d")}',description='用户给的第二个日期,如果没给出日期则获取当前时间')


def number_calculate(number1,number2,mode):
    if mode=='1':
        return number1+number2
    if mode=='2':
        return number1-number2
    if mode=='3':
        return number1*number2
    if mode=='4':
        return number1/number2
    if mode=='5':
        return number1**(1/2)

def read_file(file_name):
    with open(file_name,'r',encoding='utf-8') as f:
        return f.read()

def date_calculate(date1,date2):
    fmt = "%Y-%m-%d"
    d1 = datetime.strptime(date1, fmt).date()
    d2 = datetime.strptime(date2, fmt).date()
    return abs((d1 - d2).days)


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
        Number_calculate,
        'number_calculate',
        '根据用户提供的数字，以及计算方式（如加减乘除开方），给出计算结果'
    ),
    pydantic_to_tool_definition(
        Read_file,
        'read_file',
        '根据用户提供文件名，在当前目录寻找该文件，并读取其内容'
    ),
    pydantic_to_tool_definition(
        Date_calculate,
        'date_calculate',
        '根据用户提供的日期，计算两个日期的差值，给出计算结果'
    )
]

# print("\n自动生成的tools工具定义：")
# print(json.dumps(tools,indent=2,ensure_ascii=False))


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
    #print(f"\n[LLM接口耗时] {cost} s")
    return completion

# ====================== 3. 工具注册表 + 分发器 ======================
tool_registry = {"number_calculate": (number_calculate, Number_calculate) ,
                "read_file":(read_file, Read_file),
                 "date_calculate":(date_calculate, Date_calculate),
                 }


def dispatch_tool(func_name, func_args):
    """通用工具分发器，自动匹配函数"""
    if func_name not in tool_registry:
        return f"❌ 不存在工具：{func_name}"
    tool_func,param_model=tool_registry[func_name]
    try:
        valid_params=param_model(**func_args)
        clean_args = valid_params.model_dump()
        return tool_func(**clean_args)
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
        "content": str(res)
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
        #print(f"\n[全部工具并行执行总耗时] {tool_cost} s")

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
        #print(f"\n===================== 程序整体总耗时：{total_cost} 秒 =====================")



