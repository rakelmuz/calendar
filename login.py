#app.py
from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
import re 
 
app = Flask(__name__)
 
#  proteção extra
app.secret_key = 'testesecretkey'
 
mysql = MySQL()
   
# conexao MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'calendar'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
# http://localhost:5000/login/ - esta será a página de login
@app.route('/login/', methods=['GET', 'POST'])
def login():
 # conexao
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Mensagem de saída se algo der errado ...
    msg = ''
    # Verifica se existe solicitações POST "email" e "senha"
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        # variáveis para facilitar o acesso
        email = request.form['email']
        senha = request.form['senha']
        # Verifica se existe uma conta usando o MySQL
        cursor.execute('SELECT * FROM login WHERE email = %s AND senha = %s', (email, senha))
        # Busca um registro e retornar resultado
        login = cursor.fetchone()
   
    # Se a conta existir na tabela de login no banco de dados
        if login:
            # Cria dados da sessão, pode acessar esses dados em outras rotas
            session['loggedin'] = True
            session['idlogin'] = login['idlogin']
            session['email'] = login['email']
            # Redirecionar para a página inicial
            #return 'Conectado com sucesso!'
            return redirect(url_for('home'))
        else:
            # A conta não existe ou o e-mail / senha incorretos
            msg = ' e-mail/senha incorretos!'
    
    return render_template('login.html', msg=msg)
 
# http://localhost:5000/register - esta será a página de registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    #Mensagem de saída se algo der errado ...
    msg = ''
    # Verifica se existem solicitações POST "email" AND "senha" (formulário enviado pelo usuário)
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        # Create variables for easy access
        senha = request.form['senha']
        email = request.form['email']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM login WHERE email = %s', (email))
        login = cursor.fetchone()
        # Se houver uma conta, mostre verificações de erro e validação
        if login:
            msg = 'Conta já existente!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Endereço de e-mail invalido!'
        
        else:
            # A conta não existe e os dados do formulário são válidos, agora insira nova conta na tabela de contas
            cursor.execute('INSERT INTO login VALUES (NULL, %s, %s)', (email, senha)) 
            conn.commit()
   
            msg = 'Você se registrou com sucesso!'
    elif request.method == 'POST':
        # o formulário está vazio ... (sem dados POST)
        msg = 'Por favor, preencha o formulário!'
    # Mostrar formulário de registro com mensagem (se houver)
    return render_template('register.html', msg=msg)
  
# http://localhost:5000/home - essa será a página inicial, acessível apenas para usuários logados
@app.route('/')
def home():
    # Verifique se o usuário está logado
    if 'loggedin' in session:
   
        # Usuário conectado mostra a página inicial
        return render_template('layout.html', email=session['email'])
    # O usuário não está conectado, redirecionado para a página de login
    return redirect(url_for('login'))
  
# http://localhost:5000/logout - esta será a página de logout
@app.route('/logout')
def logout():
    # Remover dados da sessão, isso fará o logout do usuário
   session.pop('loggedin', None)
   session.pop('idlogin', None)
   session.pop('email', None)
   # redireciona para a pagina de login
   return redirect(url_for('login'))
 
# http://localhost:5000/profile -essa será a página de perfil, acessível apenas para usuários logados
@app.route('/profile')
def profile(): 
 # Verifica se existe uma conta usando o MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Verifique se o usuário está logado
    if 'loggedin' in session:
        # Precisamos de todas as informações da conta para o usuário, para que possamos exibi-las na página de perfil
        cursor.execute('SELECT * FROM login WHERE id = %s', [session['idlogin']])
        login = cursor.fetchone()
        # Mostrar a página de perfil com informações da conta
        return render_template('profile.html', login=login)
    # O usuário não está conectado, redirecionado para a página de login
    return redirect(url_for('login'))
  
  
  
if __name__ == '__main__':
    app.run(debug=True)