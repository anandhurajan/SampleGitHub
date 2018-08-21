from flask import Flask, render_template, flash, request,url_for,redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from dbconnect import connection 

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'anandhu1509'

class newForm(Form):
	title = TextField('Cont Title:')
	name = TextField('Cont Name:')
	email = TextField('Email ID:',validators=[validators.required(),validators.Length(min=6,max=50)])
	user_type = TextField('User Type :',validators=[validators.required()])
	merchant = TextField('Merchant :')
	Chain = TextField('Chain:')
	store = TextField('Store:')
@app.route('/')
def index():
	return render_template('index.html')

@app.route("/create", methods =['GET','POST'])
def contact():
	
	#import pdb;pdb.set_trace()
	form = newForm(request.form)
	c,conn = connection()
	print (form.errors)
	if request.method == 'POST':
		print(form.validate())
		if form.validate() == False:
			#return render_template('index.html')
			return redirect(url_for('index'))
		else:
			title = request.form['title']
			name = request.form['name']
			email = request.form['email']
			user_type = request.form['user_type']
			merchant = request.form['merchant']
			chain = request.form['chain']
			store = request.form['store']
			print (title," ",name," ",email," ",user_type," ",merchant," ",chain," ",store," ")
			c,conn = connection()
			mer_id=''
			chain_id=''
			store_code=''
			x=c.execute("select * from contact_create where email=%s",[email])
			print (int(x))
			if int(x) > 0:
				q=c.execute("select user_type from contact_create where email=%s",[email])
				re=c.fetchone()
				re1=(str(re[0]))
				flash('Email already exist with '+re1)
				return render_template('sample.html',form=form)
			if int(x) == 0:
				if user_type.lower() == 'merchant':
					z=merchant.split(',',1)
					print(z)
					l1=[]
					l2=[]
					for i in range(len(z)):
						'''a=','.join(z)
						b=','.join(z)'''
						q1=c.execute("select mer_id,mer_name from merchant where mer_name= %s",[z[i]])
						res=c.fetchone()
						res1=(str(res[0]))
						res2=(str(res[1]))
						'''l1=res[0].split(',',1)
						l2=res[1].split(',',1)'''
						l1.append(res1)
						l2.append(res2)
					print(l1,l2)
					r1 = ','.join(l1[:])
					r2 = ','.join(l2[:])
					print("hai",r1,r2)
					q1=c.execute("insert into contact_create( title, name, email, user_type, mer_id, merchant) values(%s,%s,%s,%s,%s,%s)",( title, name, email, user_type, r1, r2))
					flash("User Registered at " +user_type)	
				elif user_type.lower() == 'chain':
					z=chain.split(',',1)
					l1=[]
					l2=[]
					l3=[]
					l4=[]
					for i in range(len(z)):
						qu1=c.execute("select M.mer_id,M.mer_name,C.chain_id,C.chain_name from merchant M join chain_type C on M.mer_id=C.mer_id where C.chain_name=%s",[z[i]])
						re=c.fetchone()
						re1=(str(re[0]))
						re2=(str(re[1]))
						re3=(str(re[2]))
						re4=(str(re[3]))
						l1.append(re1)
						l2.append(re2)
						l3.append(re3)
						l4.append(re4)
					print(l1,l2,l3,l4)
					r1 = ','.join(l1[:])
					r2 = ','.join(l2[:])
					r3 = ','.join(l3[:])
					r4 = ','.join(l4[:])
					q2=c.execute("insert into contact_create( title, name, email, user_type, mer_id,merchant,chain_id,chain) values( %s, %s, %s, %s, %s, %s, %s, %s)",( title, name, email, user_type, r1, r2,r3,r4))
					flash("User Registered at " +user_type)
				elif user_type.lower() == 'store':
					z=store.split(',',1)
					l1=[]
					l2=[]
					l3=[]
					l4=[]
					l5=[]
					l6=[]
					for i in range(len(z)):
						qu2=c.execute("select M.mer_id,M.mer_name,C.chain_id,C.chain_name,S.store_code,S.store_name from merchant M join chain_type C on M.mer_id=C.mer_id join store S on S.chain_id=C.chain_id where S.store_name=%s",[z[i]])
						r=c.fetchone()
						r1=(str(r[0]))
						r2=(str(r[1]))
						r3=(str(r[2]))
						r4=(str(r[3]))
						r5=(str(r[4]))
						r6=(str(r[5]))
						l1.append(r1)
						l2.append(r2)
						l3.append(r3)
						l4.append(r4)
						l5.append(r5)
						l6.append(r6)
					r1 = ','.join(l1[:])
					r2 = ','.join(l2[:])
					r3 = ','.join(l3[:])
					r4 = ','.join(l4[:])
					r5 = ','.join(l5[:])
					r6 = ','.join(l6[:])
					q3=c.execute("insert into contact_create( title, name, email, user_type, mer_id,merchant,chain_id,chain, store_code, store) values( %s,%s,%s, %s, %s, %s, %s, %s, %s, %s)",( title, name, email, user_type, r1, r2,r3,r4,r5,r6))
					flash("User Registered at " +user_type)
			else :
				flash("Enter Details")
			conn.commit()
	#flash("User Registered at " +user_type)
		#conn.commit()
			c.close()
			conn.close()
		
	return render_template('sample.html',form=form)
	

if __name__ =='__main__':
	app.run()
	

