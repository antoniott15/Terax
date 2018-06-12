from sqlalchemy import create_engine, Column, Integer, String, PickleType, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, session, redirect, jsonify, Response, send_from_directory, url_for
from flask_bootstrap import Bootstrap

import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'

Base = declarative_base()


class User(Base):
	__tablename__='user_profesor'
	id = Column('id', Integer, primary_key=True)
	username = Column('username', String(15))
	password = Column('password', String(15))
	email = Column('email', String(20), unique=True)
	ciudad = Column('ciudad', String(40))
	telf = Column('telf', String(10))
	grado = Column('grado',String(20))
	institucion = Column('institucion', String(20))

class User2(Base):
	__tablename__='user_profesor2'
	id = Column('id', Integer, primary_key=True)
	edad = Column('edad', String(100))
	gender = Column('gender',String(10))

class User3(Base):
	__tablename__='cursos_profesor'
	id = Column('id', Integer, primary_key=True)
	dni = Column('dni', String(40))
	dniinput = Column('dniinput', String(10))
	experiencia = Column('experiencia', String(20))
	materias = Column('materias',String(100))



class User4(Base):
	__tablename__='user_alumno'
	id = Column('id', Integer, primary_key=True)
	username = Column('username', String(30))
	password = Column('password', String(20))
	email = Column('email', String(60), unique=True)
	direccion = Column('direccion', String(10))
	grado = Column('grado',String(20))
	institucion = Column('institucion', String(20))
	edad = Column('edad', String(100))


class Profesor(Base):
	__tablename__ = 'profesor'
	profesor = Column('profesor', Integer, primary_key=True)
	materias = Column('materias',String(100))
	telf = Column('telf', String(10))
	username = Column('username', String(15))
	ciudad = Column('ciudad', String(40))
	grado = Column('grado',String(20))



class Calendario(Base):
	__tablename__='data_calendario'
	AppointmentId = Column('AppointmentId',Integer, primary_key=True)
	Description = Column('Description', String(300))
	startDateExpr = Column('StartDate', DateTime)
	endDateExpr = Column('EndDate', DateTime)
	textExpr = Column('text', String(100))
	allDayExpr=Column('AllDay', Boolean)


class Ayuda(Base):
	__tablename__='Ayuda'
	id = Column('id', Integer, primary_key=True)
	nombres=Column('nombres', String(100))
	email=Column('email', String(35))
	texto=Column('texto',String(1000))



engine = create_engine('sqlite:////Users/antoniotoche/Desktop/my_project/database.db', echo = True)
Base.metadata.create_all(bind=engine)


class AlchemyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
			fields = {}
			for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
				data = obj.__getattribute__(field)
				try:
					json.dumps(data)
					fields[field] = data
				except TypeError:
					fields[field] = None

			return fields

		return json.JSONEncoder.default(self, obj)


@app.route('/users_profesores', methods = ['GET'])
def users_profesores():
	Session = sessionmaker(bind=engine)
	session=Session()
	users=session.query(User)
	usuarios_array=[]

	for us in users:
		usuarios_array.append(us)
	return Response(json.dumps(usuarios_array, cls=AlchemyEncoder), mimetype='application/json')


@app.route('/users_alumnos', methods = ['GET'])
def users_alumnos():
	Session = sessionmaker(bind=engine)
	session=Session()
	users2=session.query(User4)
	usuarios2_array=[]

	for us in users2:
		usuarios2_array.append(us)
	return Response(json.dumps(usuarios2_array, cls=AlchemyEncoder), mimetype='application/json')



@app.route('/data_calendario', methods = ['GET'])
def data_calendario():
	print('LLEGO AQUI')
	Session = sessionmaker(bind=engine)
	session=Session()
	users3=session.query(Calendario)
	usuarios3_array=[]

	for us in users3:
		usuarios3_array.append(us)
	return Response(json.dumps(usuarios3_array, cls=AlchemyEncoder), mimetype='application/json')


@app.route('/tabla_profesores')
def tabla_profesores():
	return render_template("tabla_profesores.html")

@app.route('/tabla_alumnos')
def tabla_alumnos():
	return render_template("tabla_alumnos.html")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/opciones_de_registro')
def registrarse_op():
    return render_template("registrarse_op.html")


@app.route('/opciones_de_ingreso')
def login_op():
    return render_template("entrar_op.html")

@app.route('/login_profesor')
def login_profesor():
	return render_template("entrar_profesores.html")


@app.route('/login_alumno')
def login_alumnos():
	return render_template("entrar_alumnos.html")


@app.route('/registro_alumno')
def registro_alumno():
    return render_template("register_alumno.html")

@app.route('/registro_profesor')
def registro_profesor():
    return render_template("register_profesor.html")

@app.route('/next')
def next():
    return render_template("next.html")


@app.route('/enter')
def enter():
    return render_template("enter.html")


@app.route('/calendar')
def calendario():
	return render_template("calendar.html")


@app.route('/box_deayuda', methods = ['POST'])
def ayuda():
    print('siayuda')
    Session = sessionmaker(bind=engine)
    session = Session()
    new_ayuda = Ayuda(nombres = request.form['nombres'],email = request.form["email"], texto=request.form["texto"])
    session.add(new_ayuda)
    session.commit()
    return redirect('/')



@app.route("/docalendar_save", methods=['POST'])
def calendars():
    print('LLEGO AQUI')
    Session = sessionmaker(bind=engine)
    session = Session()
    new_calendario = Calendario(Description = request.form['Description'],StartDate = request.form["StartDate"], EndDate=request.form["EndDate"], textExpr = request.form["text"], allDayExpr = request.form["AllDay"])
    session.add(new_calendario)
    session.commit()
    return redirect('/calendar')


@app.route("/doregister_profesores",methods=['POST'])
def create_user_profesores():
    Session = sessionmaker(bind=engine)
    session = Session()
    print("users")
    if request.form['password'] == request.form['password2']:
        new_user = User(username = request.form['username'], password = request.form['password'],email = request.form['email'],ciudad = request.form["ciudad"], telf=request.form["telf"], grado=request.form["grado"], institucion=request.form["institucion"])
        new_user2 = User2(edad = request.form['edad'], gender = request.form['gender'])
        session.add(new_user)
        session.add(new_user2)
        session.commit()
        return print('nada')


@app.route("/doregister_parte2_profesores", methods=['POST'])
def create_user2_profesores():
	Session = sessionmaker(bind=engine)
	session = Session()
	print(request.form.getlist('materias[]'))
	new_user3 = User3( dni = request.form['dni'],dniinput = request.form['dniinput'],experiencia = request.form['experiencia'], materias = request.form['materias'])
	session.add(new_user3)
	session.commit()
	return redirect("/")



@app.route("/doregister_alumno", methods=['POST'])
def create_user_alumno():
    Session = sessionmaker(bind=engine)
    session = Session()
    print("users")
    if request.form['password'] == request.form['password2']:
        new_user4 = User4(username = request.form['username'], password = request.form['password'],email = request.form['email'], direccion=request.form["direccion"], grado=request.form["grado"], institucion=request.form["institucion"], edad = request.form['edad'])
        session.add(new_user4)
        session.commit()
        return redirect("/")



@app.route('/dologin_profesores', methods=['POST'])
def dologin2():
    print("user")
    Session = sessionmaker(bind=engine)
    session=Session()
    user = session.query(User).filter_by(email = request.form['email']).first()
    if user:
        if user.password == request.form['password']:
            return redirect('/')
        else:
           return redirect('/')
    else:
        return redirect('/')



@app.route('/dologin_alumnos', methods=['POST'])
def dologin3():
    print("user")
    Session = sessionmaker(bind=engine)
    session=Session()
    user2 = session.query(User4).filter_by(email = request.form['email']).first()
    if user2:
        if user2.password == request.form['password']:
            return redirect('/enter')
        else:
           return redirect('/')
    else:
        return redirect('/')





@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(debug = True )
