"""
#AI接入天气API 查询天气 给出穿衣建议
from openai import OpenAI
import os
import requests
api_key=os.getenv('DS_API_KEY')

class LLM:
    PLATFORMS={
        'ds':{'base_url':'https://api.deepseek.com/v1',
            'model':'deepseek-chat'},
        'qwen': {'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
               'model': 'qwen-plus'},
        'qf':{
            'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
            'model': 'qf-plus'
            }
        }


    def __init__(self,platform:str):
        config=self.PLATFORMS[platform]
        self.client=OpenAI(api_key=api_key,base_url=config['base_url'])
        self.model=config['model']


    def get_weather(self,city:str):

        url = 'https://restapi.amap.com/v3/weather/weatherInfo'
        params_base = {
            'city': city,
            'key': '7197563b3bb5d59cd1e2cf3c88965600',
            'extensions': 'base',
            'output': 'json'
        }

        params_base['city'] = city
        resp = requests.get(url, params=params_base)
        resp_json = resp.json()
        data = resp_json['lives']
        live = data[0]
        return {
                'province': live['province'],
                'city': live['city'],
                'weather': live['weather'],
                'temperature': live['temperature'],
                'humidity': live['humidity'],
                'winddirection': live['winddirection'],
                'windpower': live['windpower'],
                'reporttime': live['reporttime'],
            }


    def get_advice(self,city:str):
        weather = self.get_weather(city)
        prompt = (
            f"今天{weather['city']}{weather['temperature']}℃{weather['weather']}，"
            f"湿度{weather['humidity']}%，"
            f"风向{weather['winddirection']}，风力{weather['windpower']}级。\n"
            f"给出穿衣建议。"
        )

        # 发送对话请求
        res = self.client.chat.completions.create(
            model='deepseek-chat',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=512
        )

        return res.choices[0].message.content


if __name__=='__main__':
    ai=LLM('ds')
    print(ai.get_advice('北京'))

"""

"""
import os, time
from datetime import datetime
from openai import OpenAI

BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

class Debater:
    def __init__(self,name,model,api_key,base_url):
        self.name=name
        self.model=model
        self.client=OpenAI(api_key=api_key, base_url=base_url)

    def reply(self,prompt):
        res=self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", 'content': prompt}],
            max_tokens=512
        )
        return res.choices[0].message.content

class QwenDebater(Debater):
    def __init__(self,name,model):
        Debater.__init__(self,name,model,os.getenv("QWEN_API_KEY"),BASE)

class Judge:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("DS_API_KEY"),
                             base_url="https://api.deepseek.com/v1")

    def score(self,topic, transcript):
        res = self.client.chat.completions.create(
            model="deepseek-chat", max_tokens=1024,
            messages=[{"role": "user", "content":
                f"你是一辩论裁判。辩题：{topic}\n记录：\n{transcript}\n评价双方，指出胜负及理由。"}])
        return res.choices[0].message.content

def main():
    topic = input("辩题：")
    debaters = [
        QwenDebater("千问-plus", "qwen-plus"),
        QwenDebater("千问-max", "qwen-max"),
    ]

    history=[]
    lines=[f"辩题：{topic}\n"]

    for i in range(1,4):
        print(f"第{i}轮\n")
        for d in debaters:
            ctx = "".join(f"[{h['name']}] {h['content']}\n" for h in history)
            prompt = f"辩题：{topic}\n{ctx}\n你是{d.name}，请辩论（200字内）："
            print(f"  {d.name}...")
            resp = d.reply(prompt)
            history.append({"name": d.name, "content": resp})
            lines.append(f"[{d.name}] {resp}\n")
            print(f"    {resp[:80]}...")

    text = "".join(lines)
    print("\n裁判打分...")
    result = Judge().score(topic, text)

    fname = f"debate.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"辩题：{topic}\n")
        f.writelines(lines)
        f.write(f"\n裁判评语：\n{result}\n")
    print(f"\n保存：{fname}\n裁判：{result}")

if __name__ == "__main__":
    main()
"""


#文章摘要生成器
"""import os, re, jieba
from collections import Counter
from datetime import datetime
from openai import OpenAI
from wordcloud import WordCloud
import matplotlib.pyplot as plt

api_key=os.getenv("DS_API_KEY")
base_url='https://api.deepseek.com/v1'
model='deepseek-chat'


def read_source(source):
    with open(source,'r',encoding='utf-8') as f:
        text=f.read()
    return clean_text(text)

def clean_text(text):
    text=re.sub(r"<[^>]+>",'',text) #去html标签
    #text=re.sub("\s+",'',text) #去除多余空白 留一个
    lines = []  #清除空格
    for l in text.split("\n"):
        l = l.strip()
        if l:
            lines.append(l)
    return '\n'.join(lines)

def jieba_clean(text,top_n=10):
    words=jieba.lcut(text)
    wtopwords=set("的了在是我有和就不人都一个上也很到说要去你会着没看好自己这"
                    "被能那为所如之将与等啊吧吗嗯哈呀呢嘛哎哦呵呸")
    filtered=[]
    for i in words:
        if i not in wtopwords and len(i)>=2 and not re.search(r"[0-9a-zA-Z]",i):
            filtered.append(i)
    result=[]
    counts=Counter(filtered)
    top=counts.most_common(top_n)
    for i ,count in top:
        result.append(i)
    return result

def llm_(prompt):
    client=OpenAI(api_key=api_key,base_url=base_url)
    res=client.chat.completions.create(
        model=model,
        messages=[{'role':'user','content':prompt}]
    )
    return res.choices[0].message.content

def generate(text):
    s1=llm_(f"用一句话概括核心观点： \n{text}")
    s2 = llm_(f"用3-5句话概括，保留关键论据： \n{text}")
    s3 = llm_(f"用Q&A格式，提炼3个核心问题+答案： \n{text}")
    return s1,s2,s3

def wordcloud(keywords,path):
    wc=WordCloud(
        font_path="C:/Windows/Fonts/simhei.ttf",
        width=800,height=400,background_color='white'
    )
    wc.generate(" ".join(keywords))
    wc.to_file(path)
    print("词云已保存",path)

if __name__=="__main__":
    source=input("输入文件地址：").strip()
    text=read_source(source)
    keywords=jieba_clean(text)

    s1,s2,s3=generate(text)
    print(f"简短：{s1}")
    print(f"标准：{s2}")
    print(f"详细：{s3}")

    img_path = "keywords.png"
    wordcloud(keywords, img_path)
    print(f"关键词：{'、'.join(keywords)}")

    with open("summary.md", "w", encoding="utf-8") as f:
        f.write("# 文章摘要\n\n")
        f.write(f"## 简短摘要（一句话）\n\n{s1}\n\n")
        f.write(f"## 标准摘要（3-5句）\n\n{s2}\n\n")
        f.write(f"## 详细摘要（Q&A）\n\n{s3}\n\n")
        f.write(f"## Top 10 关键词\n\n{'、'.join(keywords)}\n\n")
        f.write(f"![词云]({img_path})\n")
    print(f"已保存 summary.md")"""


#智能背单词工具
import mysql
import os, random, mysql.connector
from openai import OpenAI

API_KEY = os.getenv("DS_API_KEY")
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "vocab",
}


def init_db():
    """初始化数据库和表"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            word_en VARCHAR(100),
            word_cn VARCHAR(100),
            correct INT DEFAULT 0,
            wrong INT DEFAULT 0
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def update_record(en, cn, is_correct):
    """更新学习记录：正确+1 或 错误+1"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, correct, wrong FROM records WHERE word_en=%s", (en,))
    row = cur.fetchone()
    if row:
        if is_correct:
            c = row[1] + 1
            w = row[2]
        else:
            c = row[1]
            w = row[2] + 1
        cur.execute("UPDATE records SET correct=%s, wrong=%s WHERE id=%s",
                    (c, w, row[0]))
    else:
        if is_correct:
            c, w = 1, 0
        else:
            c, w = 0, 1
        cur.execute("INSERT INTO records(word_en, word_cn, correct, wrong) VALUES(%s,%s,%s,%s)",
                    (en, cn, c, w))
    conn.commit()
    cur.close()
    conn.close()


def get_wrong_words():
    """查询错题（错误次数 >= 1 的单词）"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT word_en, word_cn, wrong FROM records WHERE wrong>0 ORDER BY wrong")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# 加载单词库
def load_words(path_en, path_cn):
    """从两个 txt 文件加载英中对照单词表"""
    with open(path_en, "r", encoding="utf-8") as f:
        en_list = [line.strip() for line in f if line.strip()]
    with open(path_cn, "r", encoding="utf-8") as f:
        cn_list = [line.strip() for line in f if line.strip()]
    return list(zip(en_list, cn_list))  # [(apple, 苹果), (book, 书), ...]


#  LLM 生成例句 + 记忆技巧
def get_tips(word_en, word_cn):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    prompt = f"单词：{word_en}（{word_cn}）\n请给出：一个例句 一个记忆技巧"
    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256, temperature=0.5)
    return res.choices[0].message.content.strip()


# 主流程
def main():
    init_db()
    words = load_words("words100.txt", "words100_cn.txt")

    score, total = 0, 0
    print("  智能背单词工具")
    print("  输入英文，q 退出  h 查错题本  r 复习错题")

    while True:
        # 随机抽词
        en, cn = random.choice(words)
        total += 1

        ans = input(f"\n{cn} 的英文是：").strip()
        if ans.lower() == "q":
            break
        if ans.lower() == "h":
            print("\n 错题本 ")
            for e, c, w in get_wrong_words():
                print(f"  {e}（{c}）— 错 {w} 次")
            continue
        if ans.lower() == "r":
            wrong = get_wrong_words()
            if not wrong:
                print("\n 没有错题！全部正确")
                continue
            print(f"\n 复习错题（共 {len(wrong)} 个）──")
            r_score, r_total = 0, 0
            for e, c, w in wrong:
                r_total += 1
                a = input(f"\n{c} 的英文是：").strip()
                if a.lower() == e.lower():
                    r_score += 1
                    update_record(e, c, True)
                    print(" 正确！")
                    conn = mysql.connector.connect(**DB_CONFIG)
                    cur = conn.cursor()
                    cur.execute("SELECT id, correct, wrong FROM records WHERE word_en=%s", (e,))
                    row = cur.fetchone()
                    new_c = row[1] + 1
                    cur.execute("UPDATE records SET correct=%s, wrong=0 WHERE id=%s",
                                (new_c,  row[0]))
                    conn.commit()
                    cur.close()
                    conn.close()
                else:
                    update_record(e, c, False)
                    print(f" 错误，正确答案是：{e}")
                    print(f"  {get_tips(e, c)}")
            print(f"\n复习完成：{r_score}/{r_total}")
            continue

        if ans.lower() == en.lower():
            score += 1
            update_record(en, cn, True)
            print(f" 正确！（{score}/{total}）")
        else:
            update_record(en, cn, False)
            print(f" 错误，正确答案是：{en}")

            # 错题自动生成例句和记忆技巧
            print("  生成记忆帮助")
            tips = get_tips(en, cn)
            print(f"  {tips}")

    print(f"\n本次学习结束，得分：{score}/{total}")


if __name__ == "__main__":
    main()



