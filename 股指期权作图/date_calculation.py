#这段代码可用于判断当前时点的主力和次主力合约月份
import datetime


def get_third_friday(current_year, current_month):
    first_day = datetime.date(year=current_year, month=current_month, day=1)
    #suppose first day is Monday(0), the first Friday is +4,  Thursday(3) +1,
    # if it's Friday(4) +0, if Saturday(5) +6, if Sunday(6) +5
    if first_day.weekday() <= 4:
        first_friday = first_day + datetime.timedelta(days=4-first_day.weekday())
    else:
        first_friday = first_day + datetime.timedelta(days=11 - first_day.weekday())
    third_friday = first_friday + datetime.timedelta(weeks=2)
    return third_friday


def get_current_dom_subdom_month():
    """每个月上旬，主力合约为当月合约，次主力合约为次月合约；
    每个月下旬，主力合约为次月合约，次主力合约为下下月合约。
    此处的上下旬由每个月第三个周五分割
    """
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month
    next_month = current_month % 12 + 1
    next_next_month = next_month % 12 + 1
    third_friday = get_third_friday(current_year, current_month)
    months = [current_month, next_month, next_next_month]
    if next_month > next_next_month:
        #11,12,1的情况
        current_month = f"{str(current_year)[2:]}11"
        next_month = f"{str(current_year)[2:]}12"
        next_next_month = f"{str(current_year+1)[2:]}01"
    elif current_month > next_month:
        #12,1,2的情况
        current_month = f"{str(current_year)[2:]}12"
        next_month = f"{str(current_year+1)[2:]}01"
        next_next_month = f"{str(current_year+1)[2:]}02"
    else:
        for i, month in enumerate(months):
            if len(str(month)) == 1:
                months[i] = f"{str(current_year)[2:]}0{str(month)}"
            else:
                months[i] = f"{str(current_year)[2:]}{str(month)}"
        current_month, next_month, next_next_month = months
    if current_date <= third_friday:
        return current_month, next_month
    else:
        return next_month, next_next_month
