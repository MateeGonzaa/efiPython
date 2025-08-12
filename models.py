#Mateo Gonzalez y Lucas Aruza 
from app import db  # Importa la instancia de la base de datos (MySQL) desde la aplicación principal
from flask_login import UserMixin  # Clase auxiliar para integrar el modelo de usuario con Flask-Login

# Tabla intermedia para la relación muchos-a-muchos entre Posteos y Categorias
post_categorias = db.Table(
    "post_categorias",  # Nombre de la tabla en la base de datos(MySQL)
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),  # ID del posteo
    db.Column(
        "categoria_id", db.Integer, db.ForeignKey("categoria.id"), primary_key=True  # ID de las categorías
    ),
)

# Modelo de usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Identificador 
    username = db.Column(db.String(100), nullable=False, unique=True)  # Nombre de usuario 
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email 
    password_hash = db.Column(db.String(256), nullable=False)  # Contraseña en formato hash
    is_activate = db.Column(db.Boolean, default=True)  # Estado de activación del usuario

    def __str__(self):
        return self.username  # Representación en texto del usuario (su nombre de usuario)

# Modelo de posteo o publicación
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador 
    titulo = db.Column(db.String(150), nullable=False)  # Título de la publicación
    contenido = db.Column(db.Text, nullable=False)  # Contenido de la publicación
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())  # Fecha de creación automática
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Relación con usuario
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Estado de activación

    # Relación: un posteo pertenece a un usuario
    usuario = db.relationship("User", backref=db.backref("posts", lazy=True))

    # Relación muchos-a-muchos: un posteo puede tener varias categorías
    categorias = db.relationship(
        "Categoria",
        secondary=post_categorias,  # Usa la tabla intermedia definida anteriormente
        lazy="subquery",  # Carga anticipada de datos
        backref=db.backref("posts", lazy=True),  # Desde categoría se puede acceder a sus posteos
    )

# Modelo de comentario
class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador 
    texto = db.Column(db.Text, nullable=False)  # Texto del comentario
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())  # Fecha de creación automática
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Usuario autor
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)  # Posteo al que pertenece

    # Relación: un comentario pertenece a un usuario
    usuario = db.relationship("User", backref=db.backref("comentarios", lazy=True))

    # Relación: un comentario pertenece a un posteo
    post = db.relationship("Post", backref=db.backref("comentarios", lazy=True))

# Modelo de categoría
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador 
    nombre = db.Column(db.String(100), nullable=False, unique=True)  # Nombre de la categoría
