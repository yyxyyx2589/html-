def jia(m, n):
    return m + n


def jian(m, n):
    return m - n


def cheng(m, n):
    return m * n


def chu(m, n):
    return m / n
def caculate():
    while True:
        print("输入：1加法，2减法，3乘法，4除法,5退出")
        y = int(input())
        if y==1:
            print("输入两个数进行运算")
            m, n = map(float, (input().split()))
            print("结果为：", end="")
            print(jia(m,n))
        if y==2:
            print("输入两个数进行运算")
            m, n = map(float, (input().split()))
            print("结果为：", end="")
            print(jian(m,n))
        if y==3:
            print("输入两个数进行运算")
            m, n = map(float, (input().split()))
            print("结果为：", end="")
            print(cheng(m,n))
        if y==4:
            print("输入两个数进行运算")
            m, n = map(float, (input().split()))
            print("结果为：", end="")
            print(chu(m,n))
        if y==5:
            print("结束")
            break

