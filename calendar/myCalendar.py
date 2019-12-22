from flask import Flask, request, render_template
import calendar, datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route('/' ,methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        baseDate = datetime.date.today()
        htmlCal = calendar.HTMLCalendar()
        cal = htmlCal.formatmonth(baseDate.year, baseDate.month)
    else:
        htmlCal = calendar.HTMLCalendar()
        baseDate = datetime.datetime.strptime(request.form['baseDate'], "%Y-%m-%d")
        baseDate = datetime.date(baseDate.year,baseDate.month,1)
        if request.form['changeMonth'] == 'prev':
            baseDate = baseDate - relativedelta(months=1)
        else:
            baseDate = baseDate + relativedelta(months=1)
        cal = htmlCal.formatmonth(baseDate.year, baseDate.month)

    cal = cal.replace('<table', '<table id="cal-table" ')
    cal = cal.replace('border="0"', 'border="1"')
    return render_template('index.html', cal=cal,baseDate=baseDate )

if __name__ == '__main__':
    app.debug = True
    app.run()
        