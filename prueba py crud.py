#--------------------------------------------------------------------
#IMPORTACION DE FRAMEWORKS Y MODULOS NECESARIOS 

from flask import Flask # Se importa el framework Flask
from flask import render_template, request, redirect # Se importa una función que llamar un doc. HTML en el Return de la app
from flaskext.mysql import MySQL # Importamos el módulo que permite conectarnos a la BD

#--------------------------------------------------------------------
# Se crea una applicación con Flask
app= Flask(__name__) 


#--------------------------------------------------------------------
#CONFIGURACIÓN DE LA CONEXIÓN CON LA BASE DE DATOS

mysql = MySQL() # Creamos la conexión con la base de datos
app.config['MYSQL_DATABASE_HOST']='localhost' # Creamos la referencia al host
app.config['MYSQL_DATABASE_USER']='root' # Indicamos el usuario
app.config['MYSQL_DATABASE_PASSWORD']='root' # Indicamos el pass
app.config['MYSQL_DATABASE_BD']='world' # Indicamos el Nombre de nuestra BD

mysql.init_app(app) # Creamos la conexión con los datos

#------------------------------------------------------------------


# Index: Se muestra la base de datos
@app.route('/')
def index():

    sql = "SELECT * FROM world.city ORDER by ID DESC" # Creamos una variable que va a contener la consulta sql:

    conn = mysql.connect() # Conectamos a la conexión mysql.init_app(app)
    cursor = conn.cursor() # creamos el cursor: un objeto que puede interactuar con el Servidor SQL
    cursor.execute(sql) # Ejecutamos la sentencia SQL
    datosRecibidos=cursor.fetchall() #Capturamos el resultado de la consulta
    conn.commit() # "Commiteamos" (Cerramos la conexión)

    return render_template("index.html",datosRecibidos=datosRecibidos) # Cargamos la web y le enviamos la tabla con la lista de ciudades


#------------------------------------------------------------------
# Create: Renderiza la web que permite ingresar un nuevo registro
@app.route('/create')
def create():
  
  sql= "SELECT Code, Name FROM `world`.`country`;" # Obtenemos una lista de los países disponibles
  
  conn = mysql.connect() # Conectamos a la conexión mysql.init_app(app)
  cursor = conn.cursor() # creamos el cursor: un objeto que puede interactuar con el Servidor SQL
  cursor.execute(sql) # Ejecutamos la sentencia SQL
  registro=cursor.fetchall() #Capturamos el resultado de la consulta
  conn.commit() # "Commiteamos" (Cerramos la conexión)
  
  return render_template("create.html", registro=registro) # Cargamos la web y le enviamos la tabla con la lista de los paises disponibles


#------------------------------------------------------------------

# Store: Metodo que guarda en la base de datos el nuevo regitro.
@app.route("/store", methods=["POST"]) # La indicación de POST avisa a la función que va a recibir datos de la web que lo llama
def store():
  # Capturamos los datos ingresados en el formulario web:
  _ciudad=request.form["txtCiudad"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web
  _codigo=request.form["txtCodigo"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web
  _distrito=request.form["txtDistrito"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web
  _poblacion=request.form["txtPoblacion"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web

  datos=(_ciudad,_codigo,_distrito,_poblacion)
  sql = "INSERT INTO `world`.`city` (`ID`, `Name`, `CountryCode`, `District`,`Population` )\
  VALUES (NULL, %s, %s, %s, %s);" # Creamos una variable que va a contener la consulta sql:

  conn = mysql.connect() # Conectamos a la conexión mysql.init_app(app)
  cursor = conn.cursor() # creamos el cursor: un objeto que puede interactuar con el Servidor SQL
  cursor.execute(sql, datos) # Ejecutamos la sentencia SQL
  conn.commit() # "Commiteamos" (Cerramos la conexión)

  return redirect ("/") # Luego de procesar la carga del nuevo registro redirigimos al index

#------------------------------------------------------------------

# Destroy: Metodo que elimina de la base de datos el Registro seleccionado
@app.route('/destroy/<int:id>') # el ID del registro a eliminar viene en la URL
def destroy(id): # Se toma como parametro de la función de eliminación el ID que viene en el URL
  
  sql = "DELETE FROM `world`.`city` WHERE ID=%s;" # Creamos una variable que va a contener la consulta sql:

  conn = mysql.connect() # Conectamos a la conexión mysql.init_app(app)
  cursor = conn.cursor() # creamos el cursor: un objeto que puede interactuar con el Servidor SQL
  cursor.execute(sql, id) # Ejecutamos la sentencia SQL
  conn.commit() # "Commiteamos" (Cerramos la conexión)
  
  return redirect ("/") # Luego de procesar la eliminación del  registro redirigimos al index

#------------------------------------------------------------------
# Edit: Renderiza la web que permite editar un registro
@app.route('/edit/<int:id>') # el ID del registro a modificar viene en la URL
def edit(id): # Se toma como parametro de la función de edición el ID que viene en el URL
  
  sql = "SELECT * FROM `world`.`city` WHERE ID=%s;" # consulta sql que captura el registro a editar
  sql2= "SELECT Code, Name FROM `world`.`country`;" # consulta sql que obtiene la lista de paises

  conn = mysql.connect() # Conectamos a la conexión mysql.init_app(app)
  cursor = conn.cursor() # creamos el cursor: un objeto que puede interactuar con el Servidor SQL
  cursor.execute(sql, id) # Ejecutamos la 1º sentencia SQL
  registro=cursor.fetchall() #Capturamos el resultado de la 1º consulta
  cursor.execute(sql2) # Ejecutamos la 2º sentencia SQL
  registro2=cursor.fetchall() #Capturamos el resultado de la 2º consulta
  conn.commit() # "Commiteamos" (Cerramos la conexión)
  
  return render_template("edit.html", registro=registro, registro2=registro2) # Cargamos la web y le enviamos los datos del registro a editar y la tabla con la lista de los paises disponibles


#------------------------------------------------------------------

# Update: Metodo que actualiza en la base de datos la información del regitro.
@app.route("/update", methods=["POST"])  # La indicación de POST avisa a la función que va a recibir datos de la web que lo llama
def update():
  # Capturamos los datos ingresados en el formulario web:
  _id=request.form["txtID"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web
  _ciudad=request.form["txtCiudad"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web
  _codigo=request.form["txtCodigo"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web
  _distrito=request.form["txtDistrito"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web
  _poblacion=request.form["txtPoblacion"] # El texto entre corchetes [] debe coincidir con el "Name" del elemento en el formulario web

  datos=(_ciudad,_codigo,_distrito,_poblacion,_id)
  
  sql = "UPDATE `world`.`city` SET `Name`=%s, `CountryCode`=%s, `District`=%s,`Population`=%s WHERE id=%s;" # Creamos una variable que va a contener la consulta sql:

  conn = mysql.connect() # Conectamos a la conexión mysql.init_app(app)
  cursor = conn.cursor() # creamos el cursor: un objeto que puede interactuar con el Servidor SQL
  cursor.execute(sql, datos) # Ejecutamos la sentencia SQL
  conn.commit() # "Commiteamos" (Cerramos la conexión)

  return redirect ("/") # Luego de procesar la eliminación del  registro redirigimos al index


#------------------------------------------------------------------


# Metodo de Inicio de la aplicación Web
if __name__ == "__main__": # Si el nombre de la aplicación es "main" entonces...
    app.run(debug=True, port=8055) # se ejecuta la aplicación. debug true hace que la pagina se actualice sin necesidad de volver a ejecutar la apliación
