x = input()
y = []
for i in range(len(x)):
    y.append(x[i])
y = y[::-1]
print("输出个十百位")
for i in range(3):
    print(y[i])
print("逆序输出")
for i in range(len(y)):
    print(y[i], end="")

a=input()
b=input()
c=input()
if a>b:
    b,a=a,b
if a>c:
    c,a=c,a
if b>c:
    c,b
print(a,b,c)

print(bin(555))
print(oct(555))
print(hex(555))

print("请输入两个数")
a,b = map(float,input().split())
if a > 0 and b > 0:
    c = a ** 2 + b ** 2
    print(c ** (1 / 2))
else:
    print("错误")


a = input()
b=[]
c=0
for i in range(len(a)):
    if ord(a[i]) >= 97 and ord(a[i]) <= 122:
        c=chr(ord(a[i]) - 32)
        b.append(c)
    elif ord(a[i]) >= 65 and ord(a[i]) <= 90:
        c=chr(ord(a[i]) + 32)
        b.append(c)
    else:
        print("错误")
for i in range(len(b)):
    print(b[i],end="")