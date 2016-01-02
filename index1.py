from bottle import route, run, template,get,post,request,response,static_file
import os

@route('/hello/<name>')
def index(name):
	return template('<b>Hello {{name}}</b>!', name=name)
@route('/mmd')
def hello():
	return '<del>hello world!!</del>'


@get('/login') # or @route('/login')
def login():
	username = request.get_cookie("account", secret='some-secret-key')
	if request.get_cookie("login") == "true" and username:
		return '''
Welcome Back!!<button onclick='document.cookie="login="' style="margin-right=10px">Logout</button>
''' + template("Hello {{name}}", name=username)
	else:
		return '''
<form action="/login" method="post">
Username: <input name="username" type="text" />
Password: <input name="password" type="password" />
<input value="Login" type="submit" />
</form>
'''

@post('/login') # or @route('/login', method='POST')
def do_login():
	username = request.forms.get('username')
	password = request.forms.get('password')
	if check_login(username, password):
		response.set_header('Set-Cookie', 'login=true')
		response.set_cookie("account", username, secret='some-secret-key')
		return "<p>Your login information was correct.</p>"
	else:
		return "<p>Login failed.</p>"
def check_login(username, password):
	if username == "admin" and password == "admin":
		return True
	else:
		return False
@route('/static/<filename>')
def server_static_file(filename):
	return static_file(filename, root='/it')
@route('/static/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='/it')

@route('/upload', method='POST')
def do_upload():
    #category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg', '.java'):
        return 'File extension not allowed.'

    save_path  = get_save_path(upload.filename);
#get_save_path_for_category(category)
    upload.save(save_path) # appends upload.filename automatically
    return 'OK'
def get_save_path(filename):
	return "/it/upload/" + filename;

@route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    # or ip = request.get('REMOTE_ADDR')
    # or ip = request['REMOTE_ADDR']
    return template("Your IP is: {{ip}}", ip=ip)

from bottle import error
@error(404)
def error404(error):
	return 'Nothing here, sorry'

run(host='0.0.0.0', port=1010, debug=True, reloader=True)
