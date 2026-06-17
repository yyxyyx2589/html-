import os
from openai import OpenAI


def ai(user_prompt:str):
    global messages
    client = OpenAI(
        api_key=os.getenv('DS_API_KEY'),
        base_url='https://api.deepseek.com/v1'
                    )

    messages.append({'role': 'user', 'content': user_prompt})

    stream=client.chat.completions.create(
        model='deepseek-chat',
        messages=messages,
        stream=True,
        temperature=0.8
    )



    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    print(f"原始消息（{res.choices[0].message.content}）：{i}")

    prompt = f"""
    将以下消息分别翻译成英文和中文，并写成
    中文翻译：xxx
    英文翻译：yyy
    的格式：
    ```{i}```
    """
    messages = [{'role': 'system', 'content': prompt}]
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    print(f"{res.choices[0].message.content}\n")

    """ans1=eval(res.choices[0].message.content)

    for i in range(len(ans1)):
        print(ans1[i])
        if ans1[i].get('美国航空航天局') == 1:
            print("新闻通知：美国航空航天局")"""



    """ans = ''
    print("AI：", end='')
    for i in stream:
        txt = i.choices[0].delta.content
        if txt:
            ans += txt
            print(txt, end='')

    messages.append({'role': 'assistant', 'content': ans})"""

def write(user_prompt,ans):
    with open("AI_log.txt", "a", encoding="utf-8") as f:
        f.write(f" \n 用户：{user_prompt} \n AI：{ans}\n")


user_messages = [
"La performance du système est plus lente que d'habitude.",
"Mi monitor tiene píxeles que no se iluminan.",
"Il mio mouse non funziona",
"Mój klawisz Ctrl jest zepsuty",
"我的屏幕在闪烁"
]

for i in user_messages:
    prompt=f"告诉我以下文本是什么语种，直接输出语种，如法语，无需输出标点符号:{i}"
    messages=[{'role':'system','content':prompt}]
    ai(' ')



"""while True:
    user_prompt=input("请输入：")
    ai(user_prompt)"""

