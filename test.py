import datetime
import calendar

def calculate_current_month_total():
    # 获取当前年份和月份
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    
    # 计算当前年份和月份的天数
    days_in_month = calendar.monthrange(year, month)[1]
    
    total = 0
    for day in range(1, days_in_month + 1):
        # 判断每一天是星期几，并根据条件给予不同的值
        weekday = calendar.weekday(year, month, day)
        if weekday in [0, 1, 3, 5]:  # Monday, Tuesday, Thursday, Saturday
            total += 3
        elif weekday in [2, 4]:  # Wednesday, Friday
            total += 1
        elif weekday == 6:  # Sunday
            total += 2

    return total

def main():
    # 调用函数计算当月总数
    total = calculate_current_month_total()
    
    print("当月总数为:", total)

if __name__ == "__main__":
    main()
