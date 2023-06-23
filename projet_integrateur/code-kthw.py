from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuration de l'extension Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'votre_adresse_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'votre_mot_de_passe'

mail = Mail(app)

# Connexion à la base de données MySQL pour stocker les emplois du temps 
db = mysql.connector.connect(
    host='localhost',
    user='username',
    password='password',
    database='emplois_du_temps'
)

# Fonction pour ajouter un nouvel événement à l'emploi du temps et envoyer une notification par e-mail aux étudiants concernés 
def add_event(course_id, start_time, end_time, day):
    cursor = db.cursor()
    
    # Ajout d'un nouvel événement dans la base de données avec les informations fournies 
    sql_insert_event = "INSERT INTO schedule (course_id, start_time, end_time, day) VALUES (%s,%s,%s,%s)"
    
    values_insert_event =(course_id,start_time,end_time ,day)
    
 	cursor.execute(sql_insert_event ,values_insert_event )
  	
  	# Validation des modifications dans la base de données 
  	db.commit()

  	# Récupération des adresses e-mails des étudiants inscrits au cours spécifié  
	sql_get_emails ="SELECT email FROM students WHERE course_id=%s"
	
	values_get_emails =(course_id,)
	
	cursor.execute(sql_get_emails, values_get_emails)
	emails = cursor.fetchall()
  	
  	# Envoi de la notification par e-mail à chaque étudiant concerné 
	for email in emails:
	    msg = Message(subject='Nouvel événement ajouté',
	                  sender=app.config['MAIL_USERNAME'],
	                  recipients=[email])
	    msg.body = f"Un nouvel événement a été ajouté pour le cours {course_id} le {day} de {start_time} à {end_time}. Veuillez consulter l'emploi du temps en ligne pour plus d'informations."
	    mail.send(msg)

# Exemple d'utilisation de la fonction add_event() 
add_event('MATH101', '13:00', '15:00', 'Friday')
