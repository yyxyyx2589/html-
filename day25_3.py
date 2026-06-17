from openai import OpenAI
import json
import os
import re
import requests
from jsonschema import validate,ValidationError

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )


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

order_schema = {
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "string",
            "description": "情感倾向，如正面 负面 中性",
            "enum":['正面','负面','中性']
        },
        "score": {
            "type": "string",
            "description": "情感评分，1-5分，5分评价最高"
        },
        "keywords": {
            "type": "array",            # 数组类型
            "description": "用户评论的关键词",
            "items": {                  # 数组每个元素的格式
                "type": "string"
                }
        },
        "needs_review": {
            "type": "boolean",
            "description": "是否需要人工处理"
        }
    },
    "required": ["sentiment", "score", "keywords"]
}

def extract_with_schema(text:str,schema:dict,model:str='deepseek-chat') -> dict:
    schema_str=json.dumps(schema,ensure_ascii=False,indent=2)
    prompt=f"""请从以下文本中提取信息，严格按照json schema输出，只输出json不加任何说明：
    json schema:{schema_str}  待提取文本:{text}
    注意：1.只输出符合schema的json
    2.required字段必须存在
    3.enum字段只能使用给定的值"""

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{'role': 'system', 'content': ''},
                  {'role': 'user', 'content': prompt}],
        response_format={'type': 'json_object'},
    )
    return json.loads(completion.choices[0].message.content)

def validate_ai_output(data:dict,schema:dict)->tuple[bool,str]:
    try:
        validate(instance=data,schema=schema)
        return True,"通过"
    except ValidationError as e:
        return False,f"校验失败:{e.message}"

messages=[{'role':'system','content':''},
          {'role': 'user', 'content': ''}]

text="这款手机屏幕很清晰，就是电池差"
result=extract_with_schema(text,order_schema)
is_valid,msg=validate_ai_output(result,order_schema)

print(json.dumps(result,ensure_ascii=False,indent=2))

if is_valid:
    print("提取成功")
    print(f"情感倾向：{result['sentiment']}")
    print(f"评分：{result['score']}")
    print(f"关键词：{result['keywords']}")
else:
    print(f"数据不合规：{msg}")


