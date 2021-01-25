# Zapatos-Bernini
Este proyecto es una tienda enlinea de una zapateria Italiana llamada Bernini.
Utiliza django como servidor backend y reactjs como applicacion frontend.

## Descargar e Instalar
#### Python
	https://www.python.org/downloads/
	
#### Nodejs
	https://nodejs.org/en/
	
## Instalación
#### django y sus framework
    pip install -r requirment.txt
#### reactjs y sus framework
	npm i bootstrap
	npm i -g create-react-app
	npm install --save react-router-dom
	
## Configuracion del correo electronico
	En el server/bernini/settings.py encuentras los variables [SENDER_EMAIL], [SENDER_PASS], [RECIVER_EMAIL] y [SUBJECT_EMAIL]. Puedes cambiar estos variables para recivir el correo en tu cuenta
	
## Ejecución del Servidor
#### Commando
	cd server
    python manage.py runserver
	
#### Enlace
    http://127.0.0.1:8000/admin
	
#### Usuarios
	usuario: admin
	password: 123123

## Ejecución del Cliente
#### Commando
	cd cliente
	npm start

#### Enlace
	http://127.0.0.1:3000/
	
#### Usuarios
	usuario: usuario1
	password: qwe123123

	usuario: usuario2
	password: qwe123123


