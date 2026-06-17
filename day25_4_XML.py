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

def parse_ai_xml(xml_text:str):
    #安全解析AI的AML输出
    xml_text=re.sub(r'```(?:xml)?\a*','',xml_text)
    xml_text=xml_text.replace('```','').strip()
    try:
        return ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"XML解析失败：{e}")
        return None

def review_to_dict(root: ET.Element) -> dict:
    """将 review XML 转为字典"""
    result = {
        "sentiment": root.findtext("sentiment", ""),
        "score":     int(root.findtext("score", "0")),
        "pros":      [item.text for item in root.findall("pros/item")],
        "cons":      [item.text for item in root.findall("cons/item")],
        "summary":   root.findtext("summary", "")
    }
    return result

xml_prompt="""
请分析这段评论，以xml格式输出，只输出xml
评论：这款手机屏幕清晰，拍照不错，电池续航差，价格偏贵。
输出格式：
<review>
    <sentiment>正面/负面/中性/混合</sentiment>
    <score>1-5</score>
    <pros><item>优点</item></pros>
    <cons><item>缺点</item></cons>
    <summary>一句话总结<summary>
<review>
"""

response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[{'role': 'user', 'content': xml_prompt}],
)

xml_output=response.choices[0].message.content
print(xml_output)

root=parse_ai_xml(xml_output)
if root is not None:
    data = review_to_dict(root)
    print(f"情感：{data['sentiment']}，评分：{data['score']}/5")
    print(f"优点：{', '.join(data['pros'])}")
    print(f"缺点：{', '.join(data['cons'])}")
    print(f"总结：{data['summary']}")


structured_prompt="""
<task>
    <role>你是专业的代码工程师</role>
    <input>
        <code language="python">
            def add(a,b):
                return a-b
        <code> 
    <input>
    <requirements>
        <item>找出代码中的bug</item>
        <item>给出修复建议</item>
        <item>评估代码质量</item>
    <requirements>
    <output_format>
        JSON:{"bug":"...","fix":"...","score":数字}
    </output_format>
</task>
"""

response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[{'role': 'user', 'content': structured_prompt}],
    response_format={"type":"json_object"}
)
print(json.loads(response.choices[0].message.content))
