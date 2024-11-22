from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = "clave_secreta"

credenciales = {"paco": "1234"}
series = {"paco": {"por_ver": [],
                   "viendo": [],
                   "vistas": []}}


@app.route('/')
def home():
    return render_template('home.html',
                           logged_in=session.get('logged_in'),
                           username=session.get('username'),
                           lista_series=series)


@app.route('/register', methods=['GET', 'POST'])
def register_func():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        if user in credenciales:
            error = f"El usuario {user} ya existe"
            return render_template('register.html', error=error)
        credenciales[user] = password
        series[user] = {"por_ver": [],
                        "viendo": [],
                        "vistas": []}
        return redirect(url_for('login_func'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        user_form, passwd_form = request.form.get('username'), request.form.get('password')
        if user_form in credenciales and credenciales[user_form] == passwd_form:
            session['logged_in'] = True
            session['username'] = user_form
            return redirect(url_for('home'))
        error = "Usuario o contraseña equivocada"
        return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout_func():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login_func'))


@app.route('/agregar', methods=['GET', 'POST'])
def agregar_serie():
    user = session.get('username')
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        puntuacion = request.form.get('puntuacion')
        genero = request.form.get('genero')
        fecha = request.form.get('fecha')
        num_capitulos = request.form.get('capitulos')
        duracion = request.form.get('duracion')
        sinopsis = request.form.get('sinopsis')
        categoria = request.form.get('categoria')

        datos_serie = [nombre, puntuacion, genero, fecha, num_capitulos, duracion, sinopsis]
        series[user][categoria].append(datos_serie)
        return redirect(url_for('home'))
    return render_template('agregar.html')


if __name__ == '__main__':
    app.run()
