from django.shortcuts import render
from pyathena import connect
import os


def index(request):
    return render(request, 'dashboard/index.html')


def readAccessKey():
    return 0


def readSecretKey():
    return 0


# reported event:
# table: browse_condition(healthy), eligibilities(gender), countries(country), age(optional),


def getColumnName(tablename):
    query = "select column_name from information_schema.columns where table_name = " + "'" + tablename + "'"
    cursor = connect(aws_access_key_id=os.environ["accessKey"],
                     aws_secret_access_key=os.environ["secretKey"],
                     s3_staging_dir='s3://aws-athena-query-results-565635975808-us-east-2/',
                     region_name='us-east-2').cursor()
    cursor.execute(query)
    columnName = []
    for row in cursor:
        line = str(row)
        print(line)
        start = line.index("'", 0, len(line))
        end = line.index("'", start + 1, len(line))
        columnName.append(line[start + 1: end])
    print(columnName)
    return columnName


# Create your views here.

def home(request):
    if request.method == "GET":
        return render(request, 'dashboard/patient-home.html', {"show": False})
    if request.method == 'POST':
        cursor = connect(aws_access_key_id=os.environ["accessKey"],
                         aws_secret_access_key=os.environ["secretKey"],
                         s3_staging_dir='s3://aws-athena-query-results-565635975808-us-east-2/',
                         region_name='us-east-2').cursor()

        if 'tablename' in request.POST:
            tablename = request.POST['tablename']
            columnNames = getColumnName(tablename)
            attributeLine = []
            for column in columnNames:
                query = "select " + column + " from clinic." + tablename + " limit 10"
                print(query)
                cursor.execute(query)
                attributes = []
                for row in cursor:
                    line = str(row)
                    start = -1
                    end = len(line)
                    if line.find("'") != -1:
                        start = line.index("'", 0, len(line))
                        end = line.index("'", start + 1, len(line))
                    attributes.append(line[start + 1: end])
                attributeLine.append(attributes)
            a = map(list, zip(*attributeLine))
            context = {"tablename": tablename, "columnNames": columnNames, "attributeLine": a, "show": True}
            return render(request, 'dashboard/patient-home.html', context)
        else:
            condition = request.POST['health_condition']
            gender = request.POST['gender']
            country = request.POST['country']
            print(condition)
            print(gender)
            print(country)
            query = "select s.nct_id, brief_title, array_agg(distinct adverse_event_term) adverse_event" \
                    + " from clinic.studies s" \
                    + " join clinic.reported_events r" \
                    + " on s.nct_id = r.nct_id" \
                    + " join" \
                    + " (" \
                    + " select nct_id" \
                    + "	from clinic.countries" \
                    + "	where name = '" + country + "'" \
                    + " ) c" \
                    + " on s.nct_id = c.nct_id" \
                    + " join" \
                    + " (" \
                    + " select nct_id" \
                    + " 	from clinic.browse_conditions" \
                    + " 	where downcase_mesh_term = '" + condition + "'" \
                    + " ) bc" \
                    + " on s.nct_id = bc.nct_id" \
                    + " join" \
                    + " (" \
                    + "	select nct_id" \
                    + " 	from clinic.eligibilities" \
                    + " 	where gender = '" + gender + "'" \
                    + " ) e" \
                    + " on s.nct_id = e.nct_id" \
                    + " group by s.nct_id, brief_title" \
                    + " limit 10;"
            print(query)
            cursor.execute(query)
            columnNames = ['nct_id', 'brief_title', 'adverse_events']
            attributeLine = []
            for row in cursor:
                attributes = []
                attributes.append(row[0])
                attributes.append(row[1])
                attributes.append(row[2])
                attributeLine.append(attributes)
            context = {"tablename": 'result table', "columnNames": columnNames, "attributeLine": attributeLine,
                       "show": True}
            return render(request, 'dashboard/patient-home.html', context)
