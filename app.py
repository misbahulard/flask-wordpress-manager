from flask import Flask
from flask import render_template, request

from forms import CreateForm

import subprocess

app = Flask(__name__)
app.secret_key = 'development'

@app.route("/")
def index():
    # inisialisasi
    form = CreateForm()
    output = []
    vhost = []
    USER = "root"
    HOST = "pcxma.com"

    # Ports are handled in ~/.ssh/config since we use OpenSSH
    COMMAND = "ls /etc/nginx/vhost"

    ssh = subprocess.Popen(["ssh", "%s@%s" % (USER, HOST), COMMAND],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.communicate()

    if result[0] != "":
        output.append(result[0])

        # get all vhost
        vhost = result[0].split('.conf\n')
        vhost.pop()
        vhost.insert(0, 'wpuser')
    else:
        output.append("ERROR: " + result[1])
        vhost.append('wpuser')


    return render_template("index.html", form = form, output = output, vhost = vhost)

@app.route("/create", methods = ["POST"])
def create():
    username = request.form['username']
    password = request.form['password']

    output = []

    USER = "root"
    HOST = "monitoring.pcxma.com"

    COMMAND = "sh /opt/extras/create_wordpress.sh " + username + " " + password

    cmd = subprocess.Popen(["ssh", "%s@%s" % (USER, HOST), COMMAND],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = cmd.communicate()

    if result[0] != "":
        output.append(result[0])
    else:
        output.append("ERROR: " + result[1])

    return render_template("console.html", username = username, output = output, method = "create")

@app.route("/delete")
def delete():
    vhost = request.args.get('vhost')

    output = []

    USER = "root"
    HOST = "monitoring.pcxma.com"

    COMMAND = "sh /opt/extras/delete_wordpress.sh " + vhost

    cmd = subprocess.Popen(["ssh", "%s@%s" % (USER, HOST), COMMAND],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = cmd.communicate()

    if result[0] != "":
        output.append(result[0])
    else:
        output.append("ERROR: " + result[1])

    return render_template("console.html", username = vhost, output = output, method = "delete")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)
