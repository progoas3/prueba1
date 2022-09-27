#Importar Librerias Instaladas
#pip install flask
#pip install flask-sqlalchemy   -----Para Conectar a una BD SQL
#pip install flack-marshmallow  -----Definir Esquema con la BD
#pip install marshmallow-sqlalchemy
#pip install pymysql            ------Para Conectar a MySQL Driver MySQL
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Instancia de FLASK mi aplicacion
app = Flask(__name__)
#Dando la configuracion a app Cadena de Conexion
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@35.184.165.166:3306/principal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#SQL alchemy pasar la configuracion
db = SQLAlchemy(app)
#Instanciar Marshmellow utiliza la instacion de app (Marshemellow sirve para esquema)
ma = Marshmallow(app)

class seguimiento(db.Model):
    
    accion = db.Column(db.String(1000), nullable=True)
    numero_accion = db.Column(db.String(50), nullable=True, primary_key=True)
    proceso = db.Column(db.String(50), nullable=True)
    correctiva = db.Column(db.String(50), nullable=True)
    mejora = db.Column(db.String(50), nullable=True)
    fecha_definicion = db.Column(db.String(50), nullable=True)
    fecha_cierre_propuesta = db.Column(db.String(50), nullable=True)
    fecha_cierre_real = db.Column(db.String(50), nullable=True)
    eficaz = db.Column(db.String(50), nullable=True)
    nueva_accion_al_no_ser_eficaz = db.Column(db.String(1000), nullable=True)
    observaciones = db.Column(db.String(1000), nullable=True)
    pendientes = db.Column(db.String(1000), nullable=True)
    hallazgo = db.Column(db.String(1000), nullable=True)
    
    def __init__(self,accion,numero_accion,proceso,correctiva,mejora,fecha_definicion,fecha_cierre_propuesta,fecha_cierre_real,eficaz,nueva_accion_al_no_ser_eficaz,observaciones,pendientes,hallazgo):
        self.accion = accion
        self.numero_accion = numero_accion
        self.proceso = proceso
        self.correctiva = correctiva
        self.mejora = mejora
        self.fecha_definicion = fecha_definicion
        self.fecha_cierre_propuesta = fecha_cierre_propuesta
        self.fecha_cierre_real = fecha_cierre_real
        self.eficaz = eficaz
        self.nueva_accion_al_no_ser_eficaz = nueva_accion_al_no_ser_eficaz
        self.observaciones = observaciones
        self.pendientes = pendientes
        self.hallazgo = hallazgo

db.create_all()
#Esquema Categoria
class SeguimientoSchema(ma.Schema):
    class Meta:
        fields = ('accion','numero_accion','proceso','correctiva','mejora','fecha_definicion','fecha_cierre_propuesta','fecha_cierre_real','eficaz','nueva_accion_al_no_ser_eficaz','observaciones','pendientes','hallazgo')
#una sola respuesta        
seguimiento_schema = SeguimientoSchema()
#muchas respuestas
seguimientos_schema = SeguimientoSchema(many=True)

#GET
@app.route('/seguimiento', methods=['GET'])
def get_seguimiento():
    all_seguimientos = seguimiento.query.all()
    result = seguimientos_schema.dump(all_seguimientos)
    return jsonify(result)


#GET ID
@app.route('/seguimiento/<numero_accion>', methods=['GET'])
def get_seguimiento_x_id(numero_accion):
    un_seguimiento = seguimiento.query.get(numero_accion)
    return seguimiento_schema.jsonify(un_seguimiento)

#POST
@app.route('/seguimiento', methods=['POST'])
def insert_seguimiento():
    data = request.get_json(force=True)
    accion = data['accion']
    numero_accion = data['numero_accion']
    proceso = data['proceso']
    correctiva = data['correctiva']
    mejora = data['mejora']
    fecha_definicion = data['fecha_definicion']
    fecha_cierre_propuesta = data['fecha_cierre_propuesta']
    fecha_cierre_real = data['fecha_cierre_real']
    eficaz = data['eficaz']
    nueva_accion_al_no_ser_eficaz = data['nueva_accion_al_no_ser_eficaz']
    observaciones = data['observaciones']
    pendientes = data['pendientes']
    hallazgo = data['hallazgo']
    nuevo_registro = seguimiento(accion,numero_accion,proceso,correctiva,mejora,fecha_definicion,fecha_cierre_propuesta,fecha_cierre_real,eficaz,nueva_accion_al_no_ser_eficaz,observaciones,pendientes,hallazgo)
    
    db.session.add(nuevo_registro)
    db.session.commit()
    return seguimiento_schema.jsonify(nuevo_registro)

#PUT
@app.route('/seguimiento/<numero_accion>', methods=['PUT'])
def update_seguimiento(numero_accion):
    id_seguimiento = seguimiento.query.get(numero_accion)
    
    data = request.get_json(force=True)
    accion = data['accion']
    proceso = data['proceso']
    correctiva = data['correctiva']
    mejora = data['mejora']
    fecha_definicion = data['fecha_definicion']
    fecha_cierre_propuesta = data['fecha_cierre_propuesta']
    fecha_cierre_real = data['fecha_cierre_real']
    eficaz = data['eficaz']
    nueva_accion_al_no_ser_eficaz = data['nueva_accion_al_no_ser_eficaz']
    observaciones = data['observaciones']
    pendientes = data['pendientes']
    hallazgo = data['hallazgo']
    
    id_seguimiento.accion = accion
    id_seguimiento.proceso = proceso
    id_seguimiento.correctiva = correctiva
    id_seguimiento.mejora = mejora
    id_seguimiento.fecha_definicion = fecha_definicion
    id_seguimiento.fecha_cierre_propuesta = fecha_cierre_propuesta
    id_seguimiento.fecha_cierre_real = fecha_cierre_real
    id_seguimiento.eficaz = eficaz
    id_seguimiento.nueva_accion_al_no_ser_eficaz = nueva_accion_al_no_ser_eficaz
    id_seguimiento.observaciones = observaciones
    id_seguimiento.pendientes = pendientes
    id_seguimiento.hallazgo = hallazgo
    
    db.session.commit()
    
    return seguimiento_schema.jsonify(id_seguimiento)
       
#Mensaje de Bienvenida
@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido al tutorial API REST Python'})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5050,debug=True)