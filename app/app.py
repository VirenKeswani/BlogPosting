from flask import Flask, jsonify, redirect, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import datetime
import uuid
import os

app = Flask(__name__)
cred = credentials.Certificate("./serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Blogs')

@app.route('/')
def index():
    #get data from firestore and pass it to index.html
    docs = todo_ref.stream()
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    print("data is ",data)
    return render_template('index.html', data=data)


@app.route('/add', methods=['GET'])
def render_add():
    return render_template('addBlog.html')


@app.route('/', methods=['POST'])
def add_todo():
    # try:
    #     todo = request.json
    #     todo_ref.add(todo)
    #     return jsonify({"success": True}), 200
    # except Exception as e:
    #     return f"An Error Occurred: {e}"
    Author = request.form['Author']
    Title = request.form['Title']
    Blog = request.form['Blog']
    password = request.form['pass']
    Date = datetime.datetime.now()
    Date = str(Date.strftime("%d/%m/%Y %H:%M:%S"))
    id = uuid.uuid4().hex
    data = {
        "_id" : id,
        'Author': Author,
        'Title': Title,
        'Blog': Blog,
        'Date': Date,
        'password' : password
    }
    #current date and timestap
   
    #add data to firestore and set document id to the id of the data
    todo_ref.document(id).set(data)
    # return jsonify({"success": True}), 200

    # print(data)
    return redirect('/')

@app.route('/delete/<id>', methods=['GET'])
def delete_blog(id):
    #ask password and verify if same as the one in firestore then only delete
    #get data from firestore and pass it to update.html
    doc = todo_ref.document(id).get()
    data = doc.to_dict()
    #find password in data
    password = data['password']
    print("data is ",password)
    
    #delete data from firestore
    todo_ref.document(id).delete()

    print("deleted")
    # return jsonify({"success": True}), 200

    return redirect('/')

@app.route('/edit/<id>', methods=['GET'])
def render_update(id):
    #get data from firestore and pass it to update.html
    doc = todo_ref.document(id).get()
    data = doc.to_dict()
    print("data is ",data)
    return render_template('update.html', data=data)
@app.route('/update/<id>', methods=['POST'])
def update_blog(id):
    #get data from form and pass to firestore
    Author = request.form['Author']
    Title = request.form['Title']
    Blog = request.form['Blog']
    password = request.form['pass']
    Date = datetime.datetime.now()
    # check if password is same as the one in firestore only then update or else thorw error
    data = todo_ref.document(id).get().to_dict()
    if password == data['password']:
        print("password matched")
        Date = str(Date.strftime("%d/%m/%Y %H:%M:%S"))
        data = {
            'Author': Author,
            'Title': Title,
            'Blog': Blog,
            'Date': Date
        }
        #update data in firestore
        todo_ref.document(id).update(data)
        # return jsonify({"success": True}), 200

        print("data is ",data)
        return redirect('/')
    else:
        print("password not matched")
    #    throw error in html and back to update.html
    return render_template('update.html', data=data)


@app.route('/blog/<id>', methods=['GET'])
def render_blog(id):
    #get data from firestore and pass it to update.html
    doc = todo_ref.document(id).get()
    data = doc.to_dict()
    print("data is ",data)
    
    return render_template('blog.html', data=data)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
    # app.run(debug=True , host='0.0.0.0', port = int(os.environ.get('PORT', 8080))