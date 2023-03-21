from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
from os import getenv

app = Flask(__name__)
app.config["SECRET_KEY"] = "githubpro"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "codspecialops@gmail.com"
app.config["MAIL_PASSWORD"] = str(getenv("GOOGLEAPI"))
db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	email = db.Column(db.String(255))
	date = db.Column(db.Date)
	occupation = db.Column(db.String(255))


@app.route("/", methods=['GET', 'POST'])
def index():
	data = ""
	if request.method == 'POST':

		first_name = request.form["first_name"]

		data += f"{first_name}, your form was submitted successfully!"

		last_name = request.form["last_name"]
		email = request.form["email"]
		date = request.form["date"]
		date_obj = datetime.strptime(date, "%Y-%m-%d")
		occupation = request.form["occupation"]

		form = Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation)
		db.session.add(form)
		db.session.commit()

		message_body = f"Was it you, {first_name.capitalize()} {last_name.capitalize()} who applied to our company, " \
		               f"PythonHow. If yes, please reply to this email with YES (in uppercase). If no, immediately " \
		               f"contact newsgsnc@gmail.com to revoke the application or change it. You will go through a " \
		               f"series of tests after your job application has been reviewed an accepted to get hired at" \
		               f" PythonHow. For any questions, contact the mentioned email. We will reach out to you as soon" \
		               f" as possible.\n" \
		               f"Current Data:\n" \
		               f"Name: {last_name.capitalize()}, {first_name.capitalize()}\n" \
		               f"Email: {email}\n" \
		               f"Scheduled Start Date: {date}\n" \
		               f"Current Occupation: {occupation}\n"

		message = Message(subject="Job Application Confirmation", sender=app.config["MAIL_USERNAME"], recipients=[email],
		                  body=message_body)

		mail.send(message)

	return render_template("index.html", data=data)


if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		app.run(debug=True, port=6969)
