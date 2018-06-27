from sqlalchemy import create_engine, Column, Integer, String, PickleType, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, session, redirect, jsonify, Response, send_from_directory, url_for
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, Regexp, Length, EqualTo
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, AnonymousUserMixin

import json
#Iniciar
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'

Base = declarative_base()

login_manager = LoginManager()
login_manager.init_app(app)


#Declaracion de tablas para la base de datos
class User(Base):
    __tablename__='user_profesor'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(15))
    password = Column('password', String(15))
    email = Column('email', String(20))
    materias = Column('materias',String(100))
    telf = Column('telf', String(10))
    grado = Column('grado',String(20))
    institucion = Column('institucion', String(20))
    texto = Column('texto', String(400))

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
	direccion = Column('direccion', String(200))



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



class Ayuda(Base):
	__tablename__='Ayuda'
	id = Column('id', Integer, primary_key=True)
	nombres=Column('nombres', String(100))
	email=Column('email', String(35))
	texto=Column('texto',String(1000))
#CIERRE DE TABLAS

#CONEXION A BASE DE DATOS
engine = create_engine('sqlite:///database.db', echo = True)
Base.metadata.create_all(bind=engine)
#CIERRE DE LA CONECCION


#JSON
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
#CIERRE DE json


#TABLAS PARA JSON CON DEVEXTREME
#CRUD PROFESOR
@app.route('/users_profesores', methods = ['GET'])
def users_profesores():
	Session = sessionmaker(bind=engine)
	session=Session()
	users2=session.query(User)
	usuarios_array=[]
	for us in users2:
		usuarios_array.append(us)
	return Response(json.dumps(usuarios_array, cls=AlchemyEncoder), mimetype='application/json')

@app.route('/users_profesores', methods = ['DELETE'])
def remove_user_prof():
	id = request.form['key']
	Session = sessionmaker(bind=engine)
	session=Session()
	users2 = session.query(User).filter(User.id ==id)
	for user2 in users2:
		session.delete(user2)
	session.commit()
	return "Deleted User"


@app.route('/users_profesores', methods = ['POST'])
def create_user_prof():
	d =  json.loads(request.form['values'])
	print(d)
	user2 = User(
		id=d['id'],
		usuario=d['usuario'],
		password=d['password']
	)
	Session = sessionmaker(bind=engine)
	session=Session()
	session.add(user2)
	session.commit()
	return 'Created User'

@app.route('/users_profesores', methods = ['PUT'])
def update_user_prof():
	Session = sessionmaker(bind=engine)
	session=Session()
	id = request.form['key']
	user2 = session.query(User).filter(User.id == id).first()
	d =  json.loads(request.form['values'])
	for key in d.keys():
		setattr(user2, key, d[key])
	session.add(user2)
	session.commit()
	return 'Updated User'
#CIERRE DEL CRUD Profesor


@app.route('/cursos', methods = ['GET'])
def cursos():
	Session = sessionmaker(bind=engine)
	session=Session()
	users3=session.query(User3)
	usuarios_array=[]

	for us in users3:
		usuarios_array.append(us)
	return Response(json.dumps(usuarios_array, cls=AlchemyEncoder), mimetype='application/json')


#CRUD ALUMNOS
@app.route('/users', methods = ['GET'])
def users_alumnos():
	Session = sessionmaker(bind=engine)
	session=Session()
	users=session.query(User4)
	usuarios2_array=[]
	for us in users:
		usuarios2_array.append(us)
	return Response(json.dumps(usuarios2_array, cls=AlchemyEncoder), mimetype='application/json')


@app.route('/users', methods = ['DELETE'])
def remove_user():
	id = request.form['key']
	Session = sessionmaker(bind=engine)
	session=Session()
	users = session.query(User4).filter(User4.id ==id)
	for user in users:
		session.delete(user)
	session.commit()
	return "Deleted User"


@app.route('/users', methods = ['POST'])
def create_user():
	c =  json.loads(request.form['values'])
	print(c)
	user = User4(
		id=c['id'],
		usuario=c['usuario'],
		password=c['password']
	)
	Session = sessionmaker(bind=engine)
	session=Session()
	session.add(user)
	session.commit()
	return 'Created User'

@app.route('/users', methods = ['PUT'])
def update_user():
	Session = sessionmaker(bind=engine)
	session=Session()
	id = request.form['key']
	user = session.query(User4).filter(User4.id == id).first()
	c =  json.loads(request.form['values'])
	for key in c.keys():
		setattr(user, key, c[key])
	session.add(user)
	session.commit()
	return 'Updated User'
#FIN EDITAR ALUMNOS

#CIERRE DE tablas


#TABLAS PARA JSON EN HTML
@app.route('/tabla_profesores')
def tabla_profesores():
    return render_template("tabla_profesores.html")

@app.route('/tabla_alumnos')
def tabla_alumnos():
	return render_template("tabla_alumnos.html")
#CIERRE


#INDEX
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/box_deayuda', methods = ['POST'])
def ayuda():
    print('siayuda')
    Session = sessionmaker(bind=engine)
    session = Session()
    new_ayuda = Ayuda(nombres = request.form['nombres'],email = request.form["email"], texto=request.form["texto"])
    session.add(new_ayuda)
    session.commit()
    return redirect('/')


@app.route('/myprofile_alumno', methods=['GET'])
def myprofile_alumno():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User4).filter(User4.id==session['loged']).first()
    username = str(usuario.username)
    email = str(usuario.email)
    direccion = str(usuario.direccion)
    grado = str(usuario.grado)
    institucion = str(usuario.institucion)
    edad = str(usuario.edad)
    return render_template("my_profile_alumno.html",username=username,email=email,grado=grado,institucion=institucion,edad=edad, direccion=direccion)

@app.route('/myprofile_profesor', methods=['GET'])
def myprofile_profesor():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User).filter(User.id==session['login']).first()
    username = str(usuario.username)
    email = str(usuario.email)
    telf = str(usuario.telf)
    grado = str(usuario.grado)
    institucion = str(usuario.institucion)
    texto = str(usuario.texto)
    return render_template("my_profile_profesor.html",username=username,email=email,telf=telf,grado=grado,institucion=institucion, texto=texto)


#OPCIONES
@app.route('/opciones_de_registro')
def registrarse_op():
    return render_template("registrarse_op.html")


@app.route('/opciones_de_ingreso')
def login_op():
    return render_template("entrar_op.html")
#CIERRE


#RENDER DE LOGINS
@app.route('/login_profesor')
def login_profesor():
	return render_template("entrar_profesores.html")


@app.route('/login_alumno')
def login_alumnos():
	return render_template("entrar_alumnos.html")
#CIERRE


#REGISTRO
@app.route('/registro_alumno')
def registro_alumno():
    return render_template("register_alumno.html")

@app.route('/registro_profesor')
def registro_profesor():
    return render_template("register_profesor.html")

@app.route('/next')
def next():
    return render_template("next.html")
#CIERRE


#PAG PRINCIPAL DEL APP
@app.route('/enter_profesor', methods=['GET'])
def enter_profesor():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User).filter(User.id==session['login']).first()
    username = str(usuario.username)
    grado = str(usuario.grado)
    return render_template("enter_profesor.html", username=username, grado=grado)


@app.route('/enter_alumnos', methods=['GET'])
def enter_alumnos():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User4).filter(User4.id==session['loged']).first()
    username = str(usuario.username)
    return render_template("enter_alumnos.html", username=username)


@app.route('/atras_alumno', methods=['GET'])
def atras_alumno():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User4).filter(User4.id==session['loged']).first()
    username = str(usuario.username)
    return redirect(url_for('enter_alumnos'))


@app.route('/atras_profesor', methods=['GET'])
def atras_profesor():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User).filter(User.id==session['login']).first()
    username = str(usuario.username)
    return redirect(url_for('enter_profesor'))


@app.route('/calendar_alumno')
def calendario_alumno():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User4).filter(User4.id==session['loged']).first()
    username = str(usuario.username)
    return render_template("calendar_alumno.html",username=username)

@app.route('/calendar_profesor')
def calendario_profesor():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User).filter(User.id==session['login']).first()
    username = str(usuario.username)
    grado = str(usuario.grado)
    return render_template("calendar_profesor.html",username=username, grado= grado)
#CIERRE


#---------------EDITAR PERFIL/PROFE-----------
@app.route('/editar_perfil_profe')
def editar_profe():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User).filter(User.id==session['login']).first()
    username = str(usuario.username)
    grado = str(usuario.grado)
    return render_template("editar_perfil_profesor.html", username=username, grado = grado)

@app.route('/editar_perfil_profesor', methods = ['GET'])
def editar_perfil_profesor():
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	users=sessiondb.query(User).filter(User.id==session['login'])
	usuarios2_array=[]
	for us in users:
		usuarios2_array.append(us)
	return Response(json.dumps(usuarios2_array, cls=AlchemyEncoder), mimetype='application/json')


@app.route('/editar_perfil_profesor', methods = ['DELETE'])
def remove_profesor():
	id = request.form['key']
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	users = sessiondb.query(User).filter(User.id ==id)
	for user in users:
		sessiondb.delete(user)
	sessiondb.commit()
	return "Deleted User"


@app.route('/editar_perfil_profesor', methods = ['POST'])
def create_profesor():
	c =  json.loads(request.form['values'])
	print(c)
	user = User(
		id=c['id'],
		usuario=c['usuario'],
		password=c['password']
	)
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	sessiondb.add(user)
	sessiondb.commit()
	return 'Created User'

@app.route('/editar_perfil_profesor', methods = ['PUT'])
def update_profesor():
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	id = request.form['key']
	user = sessiondb.query(User).filter(User.id == id).first()
	c =  json.loads(request.form['values'])
	for key in c.keys():
		setattr(user, key, c[key])
	sessiondb.add(user)
	sessiondb.commit()
	return 'Updated User'

#----------------EDITAR ALUMNOS---

@app.route('/editar_perfil_alum')
def editar_alumnos():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    usuario = sessiondb.query(User4).filter(User4.id==session['loged']).first()
    username = str(usuario.username)
    return render_template("editar_perfil_alumnos.html", username=username)

@app.route('/editar_perfil_alumnos', methods = ['GET'])
def editar_perfil_alumnos():
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	users=sessiondb.query(User4).filter(User4.id==session['loged'])
	usuarios2_array=[]
	for us in users:
		usuarios2_array.append(us)
	return Response(json.dumps(usuarios2_array, cls=AlchemyEncoder), mimetype='application/json')


@app.route('/editar_perfil_alumnos', methods = ['DELETE'])
def remove_alumnos():
	id = request.form['key']
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	users = sessiondb.query(User4).filter(User4.id ==id)
	for user in users:
		sessiondb.delete(user)
	sessiondb.commit()
	return "Deleted User"


@app.route('/editar_perfil_alumnos', methods = ['POST'])
def create_alumnos():
	c =  json.loads(request.form['values'])
	print(c)
	user = User4(
		id=c['id'],
		usuario=c['usuario'],
		password=c['password']
	)
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	sessiondb.add(user)
	sessiondb.commit()
	return 'Created User'

@app.route('/editar_perfil_alumnos', methods = ['PUT'])
def update_alumnos():
	Session = sessionmaker(bind=engine)
	sessiondb=Session()
	id = request.form['key']
	user = sessiondb.query(User4).filter(User4.id == id).first()
	c =  json.loads(request.form['values'])
	for key in c.keys():
		setattr(user, key, c[key])
	sessiondb.add(user)
	sessiondb.commit()
	return 'Updated User'

#TOMA DE DATOS DEL REGISTRO
@app.route("/doregister_profesores",methods=['POST'])
def create_user_profesores():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    print("users")
    if request.form['password'] == request.form['password2']:
        new_user = User(username =request.form['username'], password = request.form['password'],email = request.form['email'],materias = request.form["materias"], telf=request.form["telf"], grado=request.form["grado"], institucion=request.form["institucion"])
        new_user2 = User2(edad = request.form['edad'], gender = request.form['gender'])
    sessiondb.add(new_user)
    sessiondb.add(new_user2)
    sessiondb.commit()
    return redirect("/next")


@app.route("/doregister_parte2_profesores", methods=['POST'])
def create_user2_profesores():
	Session = sessionmaker(bind=engine)
	sessiondb = Session()
	new_user3 = User3( dni = request.form['dni'],dniinput = request.form['dniinput'],experiencia = request.form['experiencia'], direccion = request.form['direccion'])
	sessiondb.add(new_user3)
	sessiondb.commit()
	return redirect("/")



@app.route("/doregister_alumno", methods=['POST'])
def create_user_alumno():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    print("users")
    if request.form['password'] == request.form['password2']:
        new_user4 = User4(username = request.form['username'], password = request.form['password'],email = request.form['email'], direccion=request.form["direccion"], grado=request.form["grado"], institucion=request.form["institucion"], edad = request.form['edad'])
    sessiondb.add(new_user4)
    sessiondb.commit()
    return redirect("/")
#CIERRE


#VALIDACION PARA EL LOGIN
@app.route('/dologin_profesores', methods=['POST'])
def dologin2():
    print("user")
    Session = sessionmaker(bind=engine)
    sessiondb=Session()
    user = sessiondb.query(User).filter_by(email = request.form['email']).first()
    if user:
        if user.password == request.form['password']:
         user2_id=str(user.id)
         session['login'] = user.id
         return redirect(url_for('enter_profesor', id_usuario=user2_id))
        else:
           flash('Wrong password')
           return redirect('/')
    else:
        flash('Wrong password')
        return redirect('/')



@app.route('/dologin_alumnos', methods=['POST'])
def dologin3():
    print("user")
    Session = sessionmaker(bind=engine)
    sessiondb=Session()
    user2 = sessiondb.query(User4).filter_by(email = request.form['email']).first()
    if user2:
        if user2.password == request.form['password']:
           user_id=str(user2.id)
           session['loged'] = user2.id
           return redirect(url_for('enter_alumnos', id_usuario=user_id))
        else:
           return redirect('/')
    else:
        return redirect('/')
#CIERRE



@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(debug = True )
