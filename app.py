from flask import Flask, render_template,request,redirect,url_for,session,send_from_directory
import json
from Get_data import *
app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route("/",methods=['POST','GET'])
def load_home():
    if request.method == 'POST':
        text = request.form['artist']
        processed_text = text.upper()
        get_data(processed_text)
        session['name'] = processed_text
        return redirect(url_for('loading'))
    else:
        return render_template('home_page.html')

@app.route("/loading")
def loading():
    return render_template('loading.html')

@app.route("/map")
def load_map():
    test=False
    if test==True:
        with open('data_for_map.txt') as json_file:
            data = json.load(json_file)
    else:
        name = session.get('name')
        data=get_data(name)
    return render_template('map_page.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
