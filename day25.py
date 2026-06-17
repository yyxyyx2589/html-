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

class Read_file(BaseModel):
    file_name: str = Field(description='在当前根目录下寻找相应名字的文件，并读取其内容')


def read_file(file_name):
    with open(file_name,'r',encoding='utf-8') as f:
        return f.read()



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
        Read_file,
        'read_file',
        '根据用户提供文件名，在当前目录寻找该文件，并读取其内容'
    )
]


def get_response(messages):
    completion = client.chat.completions.create(
        model="deepseek-chat",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        parallel_tool_calls=True,
        response_format={'type':'json_object'},
    )
    return completion

# ====================== 3. 工具注册表 + 分发器 ======================
tool_registry = {"read_file":(read_file, Read_file)}


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


def safe_parse_json(text:str) -> dict |None:
    #1.直接纯解析json
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    #2.提取markdown json代码块
    pattern_code=r'(?:json)?\s*([\s\S]+?)'
    match=re.search(pattern_code,text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    #3.提取全文第一个[]json对象
    pattern_obj=r'\{[\s\S]+?\}'
    match=re.search(pattern_obj,text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

#蓝色牛仔裤，售价179元，库存50件  白色运动鞋，售价299元，库存30件

# messages = [
#     {
#         "role": "system",
#         "content": """你是一个很有帮助的助手。只输出json格式内容。
#         输入：红色T恤，售价89元，库存200件  输出：{{name:T恤},{price:89元},{color:红色},{number:200件}}
#
#
#         """,
#     }
# ]


messages=[{'role':'system','content':'提取json文件'},{'role': 'user', 'content': '提取：蓝色牛仔裤，售价179元，库存50件'}]

while True:
    user_input = input("请输入：")
    messages.append({"role": "user", "content": user_input})

    completion = get_response(messages)
    assistant_output = completion.choices[0].message

    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)

    if not assistant_output.tool_calls:
        print(f"{assistant_output.content}")
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




