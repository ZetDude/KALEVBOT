from datetime import datetime, timedelta
import calendar
import webbrowser
    
def deadline_time():
    time_now = datetime.utcnow() #get current UTc time
    return time_now + timedelta(hours=96) #add 96 hours to the current UTC time

def deadline_format(tdo):

    date_after_month = tdo
    new_time_day = date_after_month.strftime('%d')
    new_time_els = date_after_month.strftime('%b %Y %H:%M')
    calendar_date = calendar.day_abbr[date_after_month.weekday()]
    string = 'Deadline time: ' + str(calendar_date) + ", " + str(new_time_day) + " " + str(new_time_els) + " (UTC)™"
    return string

def time_remain_string(deadline):
    time_now = datetime.utcnow() #get current UTc time
    td = deadline - time_now
    return (str(td.days) + " Days, " + str(td.seconds//3600) + " Hours and " + str((td.seconds//60)%60) + " Minutes")

def format_time(tdo):
    date_after_month = tdo
    new_time_day = date_after_month.strftime('%d')
    new_time_els = date_after_month.strftime('%b %Y %H:%M:%S')
    calendar_date = calendar.day_abbr[date_after_month.weekday()]
    string = str(calendar_date) + ", " + str(new_time_day) + " " + str(new_time_els)
    return string
