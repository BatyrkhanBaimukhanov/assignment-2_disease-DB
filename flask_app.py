from flask import Flask
from flask import render_template, url_for, flash, redirect, request, abort
import sqlalchemy as sa
import json

url = 'mysql+pymysql://badb04229bde53:d5284d88@us-cdbr-east-06.cleardb.net/heroku_fc7fa66378cc86a'


engine = sa.create_engine(url, echo=True)
conn = engine.connect()

getCountriesQuery = sa.text('''
    select *
    from Country
''')

getDiscoveriesQuery = '''
    select *
    from Discover
'''

getDiseasesQuery = '''
    select *
    from Disease
'''

getDiseaseTypesQuery = '''
    select *
    from DiseaseType
'''

getUsersQuery = '''
    select *
    from Users
'''

getDoctorsQuery = '''
    select *
    from Doctor
'''

getPublicServantsQuery = '''
    select *
    from PublicServant
'''

getSpecializationsQuery = '''
    select *
    from Specialize
'''

getRecordsQuery = '''
    select *
    from Record
'''

def row_to_dict(request):
    old_row = request.values.get('oldRow')
    old_row = old_row.replace("\'", "\"")
    index = old_row.find("datetime.date(")
    if index != -1:
        old_row = old_row.replace("datetime.date(", "\"")
        old_row_start = old_row[0:index]
        old_row_end = old_row[index:]
        old_row_end = old_row_end.replace(", ", "-")
        old_row_end = old_row_end.replace(")", "\"")
        old_row = old_row_start + old_row_end
    print('old row')
    print(old_row)
    old_row = json.loads(old_row)
    return old_row


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/country", methods=['GET', 'POST'])
def country():
    if request.method == 'GET':
        try:
            rows = conn.execute(getCountriesQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('country.html', title="Country", rows=rows.mappings().all())

    elif request.method == 'POST':
        print(request.form['cname'])
        print(request.values.get('cname'))
        print(request)
        print(request.form)

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update Country
                set cname = :x, population = :y
                where cname = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {"x": request.values.get('cname'),
                                     'y': int(request.values.get('population')),
                                     'z': old_row['cname']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from Country
                where cname = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'z': old_row['cname']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into Country (cname, population)
                values (:x, :y)            
            ''')
            try:
                conn.execute(query, {"x": request.values.get('cname'),
                                     'y': int(request.values.get('population'))})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getCountriesQuery)
        return render_template('country.html', title="Country", rows=rows.mappings().all())


@app.route("/discover", methods=['GET', 'POST'])
def discover():
    if request.method == 'GET':
        try:
            rows = conn.execute(getDiscoveriesQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('discover.html', title="Discover", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update Discover
                set cname = :yc, disease_code = :yd, first_enc_date = :yf
                where cname = :xc and disease_code = :xd
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'yc': request.values.get('cname'),
                                     'yd': request.values.get('disease_code'),
                                     'yf': request.values.get('first_enc_date'),
                                     'xc': old_row['cname'],
                                     'xd': old_row['disease_code']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from Discover
                where cname = :x and disease_code = :y
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'x': old_row['cname'],
                                     'y': old_row['disease_code']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into Discover (cname, disease_code, first_enc_date)
                values (:x, :y, :z)            
            ''')
            try:
                conn.execute(query, {"x": request.values.get('cname'),
                                     'y': request.values.get('disease_code'),
                                     'z': request.values.get('first_enc_date')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getDiscoveriesQuery)
        return render_template('discover.html', title="Discover", rows=rows.mappings().all())


@app.route("/disease", methods=['GET', 'POST'])
def disease():
    if request.method == 'GET':
        try:
            rows = conn.execute(getDiseasesQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('disease.html', title="disease", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update Disease
                set disease_code = :x, pathogen = :y, description = :z
                where disease_code = :d
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {"x": request.values.get('disease_code'),
                                     'y': request.values.get('pathogen'),
                                     'z': request.values.get('description'),
                                     'd': old_row['disease_code']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from Disease
                where disease_code = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'z': old_row['disease_code']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into Disease (disease_code, pathogen, description, id)
                values (:x, :y, :z, :id)            
            ''')
            try:
                conn.execute(query, {"x": request.values.get('disease_code'),
                                     "y": request.values.get('pathogen'),
                                     "z": request.values.get('description'),
                                     "id": request.values.get('id'), })
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getDiseasesQuery)
        return render_template('disease.html', title="disease", rows=rows.mappings().all())


@app.route("/disease_type", methods=['GET', 'POST'])
def disease_type():
    if request.method == 'GET':
        try:
            rows = conn.execute(getDiseaseTypesQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('disease_type.html', title="Disease Type", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update DiseaseType
                set id = :x, description = :y
                where id = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {"x": request.values.get('id'),
                                     'y': request.values.get('description'),
                                     'z': old_row['id']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from DiseaseType
                where id = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'z': old_row['id']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into DiseaseType (id, description)
                values (:x, :y)            
            ''')
            try:
                conn.execute(query, {"x": request.values.get('id'),
                                     'y': request.values.get('description')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getDiseaseTypesQuery)
        return render_template('disease_type.html', title="Disease Type", rows=rows.mappings().all())


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        try:
            rows = conn.execute(getUsersQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('users.html', title="Users", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update Users
                set email = :e, name = :n, surname = :sn, salary = :s, 
                    phone = :p, cname = :c
                where email = :z
            ''')
            old_row = row_to_dict(request)
            print(request.values.get('salary'))
            try:
                conn.execute(query, {"e": request.values.get('email'),
                                     'n': request.values.get('name'),
                                     'sn': request.values.get('surname'),
                                     's': int(request.values.get('salary')),
                                     'p': request.values.get('phone'),
                                     'c': request.values.get('cname'),
                                     'z': old_row['email']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from Users
                where email = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'z': old_row['email']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into Users (email, name, surname, salary, phone, cname)
                values (:e, :n, :sn, :s, :p, :c)            
            ''')
            try:
                conn.execute(query, {"e": request.values.get('email'),
                                     'n': request.values.get('name'),
                                     'sn': request.values.get('surname'),
                                     's': int(request.values.get('salary')),
                                     'p': request.values.get('phone'),
                                     'c': request.values.get('cname')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getUsersQuery)
        return render_template('users.html', title="Users", rows=rows.mappings().all())


@app.route("/doctor", methods=['GET', 'POST'])
def doctor():
    if request.method == 'GET':
        try:
            rows = conn.execute(getDoctorsQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('doctor.html', title="Doctor", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update Doctor
                set email = :x, degree = :y
                where email = :z
            ''')
            try:
                conn.execute(query, {"x": request.values.get('email'),
                                     'y': request.values.get('degree'),
                                     'z': request.values.get('oldEmail')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from Doctor
                where email = :z
            ''')
            try:
                conn.execute(query, {'z': request.values.get('oldEmail')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into Doctor (email, degree)
                values (:x, :y)            
            ''')
            try:
                conn.execute(query, {"x": request.values.get('email'),
                                     'y': request.values.get('degree')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getDoctorsQuery)
        return render_template('doctor.html', title="Doctor", rows=rows.mappings().all())


@app.route("/public_servant", methods=['GET', 'POST'])
def public_servant():
    if request.method == 'GET':
        try:
            rows = conn.execute(getPublicServantsQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('public_servant.html', title="Public Servant", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update PublicServant
                set email = :x, department = :y
                where email = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {"x": request.values.get('email'),
                                     'y': request.values.get('department'),
                                     'z': old_row['email']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from PublicServant
                where email = :z
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'z': old_row['email']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into PublicServant (email, department)
                values (:x, :y)            
            ''')
            try:
                conn.execute(query, {"x": request.values.get('email'),
                                     'y': request.values.get('department')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getPublicServantsQuery)
        return render_template('public_servant.html', title="Public Servant", rows=rows.mappings().all())


@app.route("/specialize", methods=['GET', 'POST'])
def specialize():
    if request.method == 'GET':
        try:
            rows = conn.execute(getSpecializationsQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('specialize.html', title="Specialize", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update Specialize
                set id = :x, email = :y
                where id = :z and email = :e
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {"x": request.values.get('id'),
                                     'y': request.values.get('email'),
                                     'z': old_row['id'],
                                     'e': old_row['email']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from Specialize
                where id = :z and email = :e
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'z': old_row['id'],
                                     'e': old_row['email']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into Specialize (id, email)
                values (:x, :y)            
            ''')
            try:
                conn.execute(query, {"x": request.values.get('id'),
                                     'y': request.values.get('email')})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getSpecializationsQuery)
        return render_template('specialize.html', title="Specialize", rows=rows.mappings().all())


@app.route("/record", methods=['GET', 'POST'])
def record():
    if request.method == 'GET':
        try:
            rows = conn.execute(getRecordsQuery)
        except sa.exc.OperationalError:
            flash(f"Please try again", 'danger')
            return render_template('home.html')
        else:
            return render_template('record.html', title="Record", rows=rows.mappings().all())

    elif request.method == 'POST':

        if (request.form['action'] == 'edit'):
            query = sa.text('''
                update Record
                set email = :e, cname = :c, disease_code = :d, 
                    total_deaths = :td, total_patients = :tp
                where email = :xe and cname = :xc and disease_code = :xd
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {"e": request.values.get('email'),
                                     "c": request.values.get('cname'),
                                     "d": request.values.get('disease_code'),
                                     'td': int(request.values.get('total_deaths')),
                                     'tp': int(request.values.get('total_patients')),
                                     'xe': old_row['email'],
                                     'xc': old_row['cname'],
                                     'xd': old_row['disease_code']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Updated the row", 'success')

        elif (request.form['action'] == 'delete'):
            query = sa.text('''
                delete
                from Record
                where email = :xe and cname = :xc and disease_code = :xd
            ''')
            old_row = row_to_dict(request)
            try:
                conn.execute(query, {'xe': old_row['email'],
                                     'xc': old_row['cname'],
                                     'xd': old_row['disease_code']})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Deleted the row", 'success')

        elif (request.form['action'] == 'insert'):
            query = sa.text('''
                insert into Record (email, cname, disease_code, 
                                    total_deaths, total_patients)
                values (:e, :c, :d, :td, :tp)            
            ''')
            try:
                conn.execute(query, {"e": request.values.get('email'),
                                     "c": request.values.get('cname'),
                                     "d": request.values.get('disease_code'),
                                     'td': int(request.values.get('total_deaths')),
                                     'tp': int(request.values.get('total_patients'))})
            except sa.exc.IntegrityError:
                flash(f"Exception: integrity constraint is violated", 'danger')
            except sa.exc.OperationalError:
                flash(f"Please try again", 'danger')
            except Exception as err:
                flash(f"Unexpected {err=}, {err}", 'danger')
            else:
                flash(f"Inserted the row", 'success')

        rows = conn.execute(getRecordsQuery)
        return render_template('record.html', title="Record", rows=rows.mappings().all())


if __name__ == '__main__':
    app.run()
