# -*- coding:utf-8

import bottle
from bottle import Bottle, request ,template, redirect
import sqlite3
import os.path

app = Bottle()
#_pdb = r'C:\Python\venv35\Project1\data\items.db'
mypasth = os.path.abspath(__file__)
_pdb = os.path(mypath,'data\items.db')
tpath = os.path(mypath,'views')
#bottle.TEMPLATE_PATH.insert(0, r'C:\Python\venv35\Project1\views')
bottle.TEMPLATE_PATH.insert(0, tpath)

@app.route('/')
def index():
    return "<h1>Hello World</h1>"

@app.route("/list")
def view_list():
    con = sqlite3.connect(_pdb)
    cur = con.cursor()
    cur.execute("select id, item from items order by id")
    item_list = []
    for row in cur.fetchall():
        item_list.append({
            "id":row[0]
           ,"item":row[1]
        })
    con.close()    
    return template("list_tmpl",item_list=item_list)

@app.route("/add", method=["GET","POST"])
def add_item():
    if request.method == "POST":
        #item_name = request.forms("item_name")
        item = request.forms.decode().get("item_name")
        #item = request.forms.item_name  #文字化け対策
        con = sqlite3.connect(_pdb)
        cur = con.cursor()
        new_id = cur.execute("select max(id) +1 from items ").fetchone()[0]
        cur.execute("insert into items values(?,?)",(new_id, item))
        con.commit()
        con.close()
        body = """
            SUCCESS<br/><a href="/list">戻る</a></td>
            """
        return body
    else:
        return template("add_tmpl")

@app.route("/del/<item_id:int>", method="GET")
def del_item(item_id):
    con = sqlite3.connect(_pdb)
    cur = con.cursor()
    cur.execute("delete from items where id=?",[item_id])
    con.commit()
    con.close()
    return redirect("/list")        
    
if __name__ == "__main__":
    app.run(host='localhost', reload=True, port=8000)
    
