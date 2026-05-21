class BankAccount:
    interest_rate=0.015

    def __init__(self,account_id,name,initial_balance=0,password=0):
        self.account_id=account_id
        self.name=name
        self.__balance=initial_balance
        self.__password=password
        print(f'账户{self.account_id}创建成功,用户名:{self.name}')

    def show_balance(self):
        print('账户余额:',self.__balance)
        return self.__balance

    def deposit(self,amount):
        if amount>0:
            self.__balance+=amount
            print(f"存款成功,存入{amount}元")
            self.show_balance()
        else:
            print("请输入正确数字")

    def withdraw(self,amount,password):
        if password!=self.__password:
            print("密码错误")
            return
        if amount>self.__balance:
            print("取款失败，余额不足")
            return
        elif amount<0:
            print("请输入正确数字")
            return
        self.__balance-=amount
        print(f"取款成功，已取出{amount}元,余额:{self.__balance}")

    def change_password(self,password):
        if password!=self.__password:
            print("密码错误，请重新输入")
            return
        print("密码正确，请输入新密码:")
        new_password=input()
        self.__password=new_password
        print("修改成功")

    def calculate_interest(self,years):
        total=self.__balance
        for year in range(1,years+1):
            interest=total*self.interest_rate
            total+=interest
            print(f'第{year}年:本金+利息共{total:.2f}元,当年利息:{interest:.2f}元')
        print(f'初始金额:{self.__balance}元,存{years}年,最终总额:{total:.2f}元,总利息:{total-self.__balance:.2f}元')
        return total

    @staticmethod
    def open_account():
        print('===== 欢迎开户 =====')
        account_id=input('请输入账号:')
        name=input('请输入用户名:')
        password=int(input('请输入密码:'))
        initial_balance=int(input('请输入初始存款金额:'))
        return BankAccount(account_id,name,initial_balance,password)

print('作业2:银行账户系统')
q1=BankAccount.open_account()
#q1=BankAccount(123456,'张三',10000,0)
q1.show_balance()
q1.deposit(100)
q1.withdraw(200,0)
q1.withdraw(100,1111)
q1.withdraw(99999,0)
q1.calculate_interest(3)
q1.change_password(0)
q1.withdraw(500,0)
q1.show_balance()