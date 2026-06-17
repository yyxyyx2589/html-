"""from openai import OpenAI
import time
from day6 import get_weather
client = OpenAI(
    api_key='sk-40054f70276144199c8817b745b4a068',
    base_url='https://api.deepseek.com/v1'
                )
"""
"""res=client.chat.completions.create(
    model='deepseek-chat',
    messages=[{'role':'system','content':'你是一名计算机专业的学生,回答简单清晰'},{'role':'user','content':'你认为ai是什么'}]
)

print(res.choices[0].message.content)

stream=client.chat.completions.create(
    model='deepseek-chat',
    messages=[{'role':'user','content':'写一段简短小故事'}],
    stream=True
)

for i in stream:
    if i.choices[0].delta.content:
        print(i.choices[0].delta.content,end='')
"""


"""
messages=[]
while True:

    user_input=input("请输入你的问题：")
    messages.append({'role':'user','content':user_input})

    stream=client.chat.completions.create(model='deepseek-chat',messages=messages)

    stream = client.chat.completions.create(
        model='deepseek-chat',
        messages=messages,
        stream=True  # ← 加这一行
    )

    ans=''
    print("AI：",end='')
    for i in stream:
        if i.choices and i.choices[0].delta and i.choices[0].delta.content:
            txt=i.choices[0].delta.content
            ans=ans+txt
            print(txt,end='')
    print()
    messages.append({'role':'assitant','content':ans})
"""


from openai import OpenAI
import time
from day6 import get_weather
import smtplib
from email.message import EmailMessage

#创建客户端
client = OpenAI(
    api_key='sk-40054f70276144199c8817b745b4a068',
    base_url='https://api.deepseek.com/v1'
)


def write_log(user_input,msg):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("AI_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{now} 用户：{user_input} \n AI：{msg}\n")


def clear():
    messages=[]
    main()

def send_email():
    to = input("收件人地址：")
    subject = input("邮件主题：")
    body = input("邮件内容：")

    sender = "2589485641@qq.com"
    password = "hjkqcgceqymldhjf"
    smtp_server = "smtp.qq.com"
    smtp_port = 587

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.starttls()  # 启用加密传输
            s.login(sender, password)  # 登录邮箱
            s.send_message(msg)  # 发送邮件
            print("邮件发送成功！")
        return
    except Exception as e:
        print(f"发送失败：{e}")
        return

def main():
    character=input("请输入系统人设：")
    messages=[{'role':'system','content':character}]
    write_log(character, '已设置系统人设！')
    while True:
        user_input = input("请输入你的问题（输入exit退出，clear清空上下文）：")
        if not user_input:
            print("输入不能为空，请重新输入！")
        elif user_input == 'exit':
            print("退出成功！")
            write_log(user_input, '用户已退出！')
            break
        elif user_input == 'clear':
            print("清除上下文成功！")
            clear()
            write_log(user_input, '清除上下文！')
            continue
        elif '天气' in user_input:
            ans=input("是否需要查询天气：（y/n）")
            if ans=='y':
                get_weather()
                continue
        elif '邮件'  in user_input:
            ans = input("是否需要发送邮件：（y/n）")
            if ans == 'y':
                send_email()
                continue

        messages.append({'role': 'user', 'content': user_input})

        #发送对话请求
        res = client.chat.completions.create(
            model='deepseek-chat',
            messages=messages,
            stream=True,
            max_tokens=512,
            temperature=2,
            top_p=0.1
        )

        ans = ''
        print("AI：", end='')
        for i in res:
            txt = i.choices[0].delta.content
            if txt:
                ans += txt
                print(txt, end='')
        print()
        messages.append({'role': 'assistant', 'content': ans})
        write_log(user_input, ans)

main()
