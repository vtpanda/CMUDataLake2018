from django.shortcuts import render
from pyathena import connect


def index(request):
    return render(request, 'dashboard/index.html')


# table: browse_condition(healthy), eligibilities(gender), countries(country), age(optional),
def connectAthena(request, tablename):
    cursor = connect(aws_access_key_id='',
                     aws_secret_access_key='',
                     s3_staging_dir='s3://aws-athena-query-results-565635975808-us-east-2/',
                     region_name='us-east-2').cursor()
    query = "select * from clinic." + tablename + " limit 10"
    cursor.execute(query)
    rows = []
    for row in cursor:
        rows.append(row)
        rows.append("\n")
    context = {'rows': rows}
    return render(request, 'dashboard/patient-home.html', context)


# Create your views here.
def home(request):
    if request.method == "GET":
        return render(request, 'dashboard/patient-home.html', {})
    if request.method == 'POST':
        tablename = request.POST['tablename']
        cursor = connect(aws_access_key_id='',
                         aws_secret_access_key='',
                         s3_staging_dir='s3://aws-athena-query-results-565635975808-us-east-2/',
                         region_name='us-east-2').cursor()
        query = "select * from clinic." + tablename + " limit 10"
        cursor.execute(query)
        rows = []
        for row in cursor:
            rows.append(row)
            rows.append("\n")
        context = {'rows': rows}
        return render(request, 'dashboard/patient-home.html', context)
