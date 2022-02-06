from flask import Flask, flash, render_template, request
# from umodbus.exceptions import IllegalDataAddressError
# from modbus_client import read_from_server, write_to_server
from modbus_client import modbus_actions
app = Flask(__name__)
app.secret_key = b'_this_is_not_used_in_prod_xD'

@app.route("/", methods=['GET', 'POST'])
def index():
    context = {
    'read_from_server': 'Read',
    'write_to_server': 'Write',
    'data': None
    }
    
    if request.method == 'POST':
            input_data = request.form.get('InputData')
            try:
                data = modbus_actions(input_data)
                context['data'] = data
                flash('You were successfully able to read', 'success')
            except Exception as e:
                flash(e, 'danger')
    elif request.method == 'GET':
        return render_template('base.html', **context)
    return render_template('base.html', **context)


if __name__ == "__main__":
    app.run(debug=True)