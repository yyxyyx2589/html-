import jieba
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

"""# 1.精准模式分词
text='我爱自然语言处理'
seg_list=jieba.lcut(text,cut_all=True)
print(seg_list)
print("分词结果："+'/'.join(seg_list))

# 2.停用词过滤
stopwords={'的','了','在'}
filtered=[w for w in ['我','爱','的','自然的语言处理'] if w not in stopwords]
print(filtered)"""

# 1.数据集
data_list = [
    # 正面
    ("味道超棒，服务好", 1),
    ("电影太好看了，强烈推荐", 1),
    ("商品质量不错，物流很快", 1),
    ("环境优雅，性价比很高", 1),
    ("非常满意，下次还来", 1),
    ("味道好，干净卫生", 1),
    ("超出预期，体验极佳", 1),
    ("客服态度好，问题解决快", 1),
    ("产品做工精细，细节到位", 1),
    ("价格实惠，物超所值", 1),
    ("服务周到，让人舒服", 1),
    ("效果远超预期，非常满意", 1),
    ("物流快，包装好", 1),
    ("口味正宗，分量十足", 1),
    ("质量上乘，值得购买", 1),
    ("体验感满分，强烈安利", 1),
    ("环境干净整洁，体验很好", 1),
    ("态度热情，全程很愉快", 1),
    ("效果很好，会回购的", 1),
    ("各方面都很满意，好评", 1),
    # 负面
    ("太难吃了，再也不会来这家店", 0),
    ("电影剧情无聊，浪费时间", 0),
    ("商品质量差，发货很慢", 0),
    ("价格贵，体验很差", 0),
    ("非常失望，不推荐购买", 0),
    ("卡顿严重，体验极差", 0),
    ("做工粗糙，不值这个价", 0),
    ("客服态度差，解决不了问题", 0),
    ("物流太慢了，等了半个月", 0),
    ("味道难吃，完全踩雷", 0),
    ("质量堪忧，用了两天就坏了", 0),
    ("价格虚高，完全不值", 0),
    ("服务态度恶劣，再也不来", 0),
    ("效果很差，完全没用", 0),
    ("体验糟糕，差评", 0),
    ("环境脏乱差，太失望了", 0),
    ("态度冷漠，全程很糟心", 0),
    ("发货错误，售后也不管", 0),
    ("质量问题严重，不建议买", 0),
    ("完全不符合预期，避雷", 0)
]

texts=[i[0] for i in data_list]
labels=[i[1] for i in data_list]
df=pd.DataFrame({'text':texts,'label':labels})
#print(df.head())

# 2.自定义停用词
stop_words=['的','了','也','很','都','就','是','会','来','这','还','会','再']

# 3.分词 过滤停用词
def cut_and_filter(text):
    words=jieba.lcut(text)
    words=[w for w in words if w not in stop_words]
    return " ".join(words)
#print(df['text'])
df['cut_text']=df['text'].apply(cut_and_filter)
#print(df['cut_text'])
x=df['cut_text']
y=df['label']

# 4. TF-IDF调参
tfidf=TfidfVectorizer(ngram_range=(1,2))
x_tfidf=tfidf.fit_transform(x)
#print(x_tfidf)

# 5. 划分数据集
x_train,x_text,y_train,y_text=train_test_split(x_tfidf,y,test_size=0.2,random_state=0,stratify=y)

# 6. 训练模型
clf=MultinomialNB(alpha=0.8)
clf.fit(x_train,y_train)

# 评估
#print(x_text)
y_pred=clf.predict(x_text)
#print(y_pred)
print(f'测试集准确度:{accuracy_score(y_text,y_pred):.2f}')

# 预测函数
def pred_sent(text):
    txt=cut_and_filter(text)
    print(txt)
    vec=tfidf.transform([txt])
    print(vec)

    res=clf.predict(vec)[0]
    return '正面' if res==1 else '负面'

print('\n 测试预测')
print(pred_sent('服务很好'))


"""
import jieba
import pandas as pd
import tensorflow
from tensorflow import keras
from tensorflow.keras import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D,Dense,LSTM
from snownlp import SnowNLP

# 1.数据集
data_list = [
    # 正面
    ("味道超棒，服务好", 1),
    ("电影太好看了，强烈推荐", 1),
    ("商品质量不错，物流很快", 1),
    ("环境优雅，性价比很高", 1),
    ("非常满意，下次还来", 1),
    ("味道好，干净卫生", 1),
    ("超出预期，体验极佳", 1),
    ("客服态度好，问题解决快", 1),
    ("产品做工精细，细节到位", 1),
    ("价格实惠，物超所值", 1),
    ("服务周到，让人舒服", 1),
    ("效果远超预期，非常满意", 1),
    ("物流快，包装好", 1),
    ("口味正宗，分量十足", 1),
    ("质量上乘，值得购买", 1),
    ("体验感满分，强烈安利", 1),
    ("环境干净整洁，体验很好", 1),
    ("态度热情，全程很愉快", 1),
    ("效果很好，会回购的", 1),
    ("各方面都很满意，好评", 1),
    # 负面
    ("太难吃了，再也不会来这家店", 0),
    ("电影剧情无聊，浪费时间", 0),
    ("商品质量差，发货很慢", 0),
    ("价格贵，体验很差", 0),
    ("非常失望，不推荐购买", 0),
    ("卡顿严重，体验极差", 0),
    ("做工粗糙，不值这个价", 0),
    ("客服态度差，解决不了问题", 0),
    ("物流太慢了，等了半个月", 0),
    ("味道难吃，完全踩雷", 0),
    ("质量堪忧，用了两天就坏了", 0),
    ("价格虚高，完全不值", 0),
    ("服务态度恶劣，再也不来", 0),
    ("效果很差，完全没用", 0),
    ("体验糟糕，差评", 0),
    ("环境脏乱差，太失望了", 0),
    ("态度冷漠，全程很糟心", 0),
    ("发货错误，售后也不管", 0),
    ("质量问题严重，不建议买", 0),
    ("完全不符合预期，避雷", 0)
]

texts=[i[0] for i in data_list]
labels=[i[1] for i in data_list]
df=pd.DataFrame({'text':texts,'label':labels})
#print(df.head())

# 2.自定义停用词
stop_words=['的','了','也','很','都','就','是','会','来','这','还','会','再']

# 3.分词 过滤停用词
def cut_and_filter(text):
    words=jieba.lcut(text)
    words=[w for w in words if w not in stop_words]
    return " ".join(words)

#print(df['text'])
df['cut_text']=df['text'].apply(cut_and_filter)
#print(df['cut_text'])
x=df['cut_text'].values
y=df['label'].values

VOCAB_SIZE=2000
MAX_LEN=30


tokenizer = Tokenizer(num_words=VOCAB_SIZE)
tokenizer.fit_on_texts(x)
x_seq=tokenizer.texts_to_sequences(x)
x_pad=pad_sequences(x_seq,maxlen=MAX_LEN)


# 5. 划分数据集
x_train,x_text,y_train,y_text=train_test_split(x_pad,y,test_size=0.2,random_state=0,stratify=y)

# 6. 训练模型
model=Sequential(
    [
        Embedding(VOCAB_SIZE,32,input_length=MAX_LEN),
        LSTM(32),
        Dense(16,activation='relu'),
        Dense(1,activation='sigmoid')
    ]
)
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.fit(x_train,y_train,epochs=8,batch_size=4,verbose=1)

loss,acc=model.evaluate(x_train,y_train,verbose=0)


print(f'测试集准确度:{acc:.2f}')

# 预测函数
def pred_sent(text):
    txt=cut_and_filter(text)
    seq=tokenizer.texts_to_sequences([txt])
    pad_seq=pad_sequences(seq,maxlen=MAX_LEN)
    score=model.predict(pad_seq,verbose=0)[0][0]
    return '正面' if score<0.5 else '负面'

def chinese_sentiment(text):
    s=SnowNLP(text)
    score=s.sentiments
    return score

def sentiment_label(text):
    score=chinese_sentiment(text)
    if score >0.6:
        return "正向",score
    elif score < 0.4:
        return "负向",score
    else:
        return "中性",score


print('\n 测试预测')
print(pred_sent('体验很糟糕'))
"""