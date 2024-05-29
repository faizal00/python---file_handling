from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'sdfsdfsgsd'

# define user dan pass
user = "admin"
passw = "admin"

# melempar nama user ke html
def get_name():
    return user

# routing halaman utama dan cek session
@app.route("/")
def index():
    if 'username' in session:
        # menampilkan data di halaman index
        data = baca()
        return render_template('index.html', data=data, get_name=get_name)
    else:
        # mengembalikan ke halaman login
        return render_template('login.html')

# routing dan pengecekan login
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == user and password == passw:
            # jika user dan pass benar akan set session dan kirim ke index 
            session['username'] = username 
            return redirect(url_for('index'))
        else :
            return render_template('login-invalid.html')
    return render_template('login.html')

# mengosongkan session saat logout
@app.route('/logout')
def logout():
    # menghapus session dari username ke default
    session.pop('username', None)
    return redirect(url_for('index'))

# baca data txt
def baca():
    # membuka data dengan permission read
    with open('data.txt', 'r') as file:
        # variabel menampung hasil baca dari file ke list
        lines = file.readlines()
    # variabel menampung data yang telah di hapus spasi dan dipisahkan per baris    
    data = [line.strip().split(',') for line in lines]
    return data

# tulis data txt
def tulis(data):
    # membuka data dengan permission write
    with open('data.txt', 'w') as file:
        # iterasi tiap baris di data dan menuliskan file
        for row in data:
            file.write(','.join(row) + '\n')

# tambah data dengan post method
@app.route('/tambah', methods=['POST'])
def tambah():
    # define variabel baru yang berisi hasil kirim dari form html
    name = request.form['name']
    stock = request.form['stock']
    qty = request.form['qty']
    kategori = request.form['kategori']
    # define list dari hasil form
    input = [name,stock,qty,kategori]
    # define variabel yang berisi fungsi baca file
    data = baca()
    # menambahkan data (file yang dibaca) dengan input dari form
    data.append(input)
    tulis(data)
    return redirect(url_for('index'))

# edit data dengan post method
@app.route('/edit', methods=['POST'])
def edit():
    # define variabel baru yang berisi hasil kirim dari form html
    id = int(request.form['id'])
    name = request.form['name']
    stock = request.form['stock']
    qty = request.form['qty']
    kategori = request.form['kategori']
    # define variabel yang berisi fungsi baca file
    data = baca()
    # mengganti data yang memiliki id sesuai dengan nilai baru
    data[id] = [name,stock,qty,kategori]
    tulis(data)
    return redirect(url_for('index'))

#hapus data
@app.route('/hapus', methods=['POST'])
def hapus():
    # define id untuk dari html
    id = int(request.form['id'])
    # define variabel yang berisi fungsi baca file
    data = baca()
    # menghapus data dari id yang terpilih dan menulis hasil yang baru
    del data[id]
    tulis(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)