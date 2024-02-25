from flask import Flask, jsonify
import motor_control  # Your motor control file

app = Flask(__name__)

@app.route('/set_color/<color_name>/<diffusion>')
def api_set_color(color_name, diffusion):
    motor_control.set_color(color_name, int(diffusion))
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
