from django.shortcuts import render
from pyathena import connect
#table: browse_condition(healthy), eligibilities(gender), countries(country), age(optional),
def connectAthena(request, tablename):
    cursor = connect(aws_access_key_id='AKIAICRP6ONOPQ2DH2EA',
                 aws_secret_access_key='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',
                 s3_staging_dir='s3://aws-athena-query-results-565635975808-us-east-2/',
                 region_name='us-east-2').cursor()
    query = "select * from clinic." + tablename + " limit 10"
    print(query)
    cursor.execute(query)
    rows = []
    for row in cursor:
        rows.append(row)
        rows.append("\n")
    context = {'rows' : rows}
    return render(request, 'home.html', context)
# Create your views here.
def home(request):
    if request.method == "GET":
        return render(request, 'home.html',{})
    if request.method == 'POST':
        tablename = request.POST['tablename']
        cursor = connect(aws_access_key_id='AKIAJWQTLCSUAX4ZAO6A',
                         aws_secret_access_key='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',
                         s3_staging_dir='s3://aws-athena-query-results-565635975808-us-east-2/',
                         region_name='us-east-2').cursor()
        query = "select * from clinic." + tablename + " limit 10"
        print(query)
        cursor.execute(query)
        rows = []
        for row in cursor:
            rows.append(row)
            rows.append("\n")
        context = {'rows': rows}
        return render(request, 'home.html', context)

