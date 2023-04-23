import matplotlib.pyplot as plt
import numpy as np

# 工资个税与股权激励税率与速算扣除数
def get_income_rate_minus(x):
    if x <= 36 * 1000:
        return 0.03, 0
    elif x <= 144 * 1000:
        return 0.1, 2520
    elif x <= 300 * 1000:
        return 0.2, 16920
    elif x <= 420 * 1000:
        return 0.25, 31920
    elif x <= 660 * 1000:
        return 0.3, 52920
    elif x <= 960 * 1000:
        return 0.35, 85920
    else:
        return 0.45, 181920


'''
年终奖
根据《财政部 税务总局关于个人所得税法修改后有关优惠政策衔接问题的通知》（财税〔2018〕164号）规定，全年一次性奖金选择单独计税的，以全年一次性奖金收入除以12个月得到的数额，按照按月换算后的综合所得税率表，确定适用税率和速算扣除数，单独计算纳税。具体计算公式为：

应纳税额＝全年一次性奖金收入×适用税率－速算扣除数
'''
def get_year_bonus_rate_minus(x:float):
    if x <= 3 * 1000:
        return 0.03, 0
    elif x <= 12 * 1000:
        return 0.1, 210
    elif x <= 25 * 1000:
        return 0.2, 1410
    elif x <= 35 * 1000:
        return 0.25, 2660
    elif x <= 55 * 1000:
        return 0.3, 4410
    elif x <= 80 * 1000:
        return 0.35, 7160
    else:
        return 0.45, 15160

"""
计算本月的税收以及展示计算过程
"""
def cal_cur_month_tax(income: float, year_income_last=0, year_tax_last=0, month=1):
    year_income_till_now = year_income_last + income
    rate, minus = get_income_rate_minus(year_income_till_now)
    year_tax = year_income_till_now * rate - minus
    cur_month_tax = year_tax - year_tax_last
    detail = '(至上月累计收入:{} + {}月收入:{})*税率:{:.2f} - 扣除数:{} - 至上月累计税收:{:.2f} = 本月税收:{:.2f}, 至本月累计税收:{:.2f}'.format(
        year_income_last, month, income, rate, minus, year_tax_last, cur_month_tax, year_tax_last + cur_month_tax)
    return cur_month_tax, detail


"""
将总收入total分割为多份，每份大小为each, 返回分割列表
"""
def split_income(total, each):
    xs = []
    n = total//each
    for i in range(n):
        xs.append(each)
    if total - n*each>0:
        xs.append(total-n*each)
    return xs

def cal_all_tax_and_detail(sells:list):
    """
    计算多次卖出股票所交的税收
    sells:多次卖出的股票
    returns:
        taxs:税收
        details:计算税收的过程
    """
    year_income_last=0
    year_tax_last=0
    taxs = []
    details = []
    for ind,x in enumerate(sells):
        tax, detail=cal_cur_month_tax(x, year_income_last, year_tax_last, ind+1)
        year_income_last +=x
        year_tax_last+=tax
        taxs.append(tax)
        details.append(detail)
    return taxs, details

def test_month_tax_curve():
    """
    画月收入-税收曲线
    :return:
    """
    end = 200 * 1000
    x = np.arange(5000, end, 1)
    y = np.frompyfunc(lambda a: cal_cur_month_tax(a, 0, 0, 1)[0], nin=1, nout=1)(x)
    plt.figure()
    plt.plot(x, y)
    plt.show()

def test_apply_along_axis():
    def my_func(a):
        # 进行简单的运算
        return (a[0] + a[-1]) * 0.5
    b = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    print(np.apply_along_axis(my_func, 0, b))
    print(np.apply_along_axis(my_func, 1, b))


if __name__ == "__main__":
    if False:
        test_month_tax_curve()
    # 假设有价值50W的股票, 无论是分多次卖出，还是一次性卖出(卖出价格一样的情况下)，所交的税均为97080元, 所以多次卖出并不能减税
    print("\n".join(cal_all_tax_and_detail(split_income(500 * 1000, 36000 - 1))[1])) # 多次卖出，每次卖35999
    print("\n")
    print("\n".join(cal_all_tax_and_detail(split_income(500 * 1000, 144000 - 1))[1])) # 多次卖出，每次卖143999
    print("\n")
    print(cal_all_tax_and_detail(split_income(500 * 1000, 500 * 1000))[1]) # 一次性全部卖出
    #
    test_apply_along_axis()

