from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def homePage():
    session.clear()  
    return render_template("index_1.html")

@app.route('/next_1', methods=['POST', 'GET'])
@cross_origin()
def next_1_Page():
    if request.method == 'POST':
        try:
            session['mdvp_fo'] = float(request.form['mdvp_fo'])
            session['mdvp_fhi'] = float(request.form['mdvp_fhi'])
            session['mdvp_flo'] = float(request.form['mdvp_flo'])
            session['mdvp_jitper'] = float(request.form['mdvp_jitper'])
            session['mdvp_jitabs'] = float(request.form['mdvp_jitabs'])
            session['mdvp_rap'] = float(request.form['mdvp_rap'])
            session['mdvp_ppq'] = float(request.form['mdvp_ppq'])
            return render_template("index_2.html")

        except Exception as e:
            print('The Exception message is: ', e)
            return render_template('failure.html')
    

@app.route('/next_2', methods=['POST', 'GET'])
@cross_origin()
def next_2_Page():
    if request.method == 'POST':
        try:
            session['jitter_ddp'] = float(request.form['jitter_ddp'])
            session['mdvp_shim'] = float(request.form['mdvp_shim'])
            session['mdvp_shim_db'] = float(request.form['mdvp_shim_db'])
            session['shimm_apq3'] = float(request.form['shimm_apq3'])
            session['shimm_apq5'] = float(request.form['shimm_apq5'])
            session['mdvp_apq'] = float(request.form['mdvp_apq'])
            session['shimm_dda'] = float(request.form['shimm_dda'])
            return render_template("index_3.html")

        except Exception as e:
            print('The Exception message is: ', e)
            return render_template('failure.html')
    

@app.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            
            mdvp_fo = session.get('mdvp_fo', None)
            mdvp_fhi = session.get('mdvp_fhi', None)
            mdvp_flo = session.get('mdvp_flo', None)
            mdvp_jitper = session.get('mdvp_jitper', None)
            mdvp_jitabs = session.get('mdvp_jitabs', None)
            mdvp_rap = session.get('mdvp_rap', None)
            mdvp_ppq = session.get('mdvp_ppq', None)
            jitter_ddp = session.get('jitter_ddp', None)
            mdvp_shim = session.get('mdvp_shim', None)
            mdvp_shim_db = session.get('mdvp_shim_db', None)
            shimm_apq3 = session.get('shimm_apq3', None)
            shimm_apq5 = session.get('shimm_apq5', None)
            mdvp_apq = session.get('mdvp_apq', None)
            shimm_dda = session.get('shimm_dda', None)
            nhr = float(request.form['nhr'])
            hnr = float(request.form['hnr'])
            rpde = float(request.form['rpde'])
            dfa = float(request.form['dfa'])
            spread1 = float(request.form['spread1'])
            spread2 = float(request.form['spread2'])
            d2 = float(request.form['d2'])
            ppe = float(request.form['ppe'])

            
            filename = 'Model_Prediction.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            scaler = pickle.load(open('MinMaxScaler.sav', 'rb'))

            
            prediction = loaded_model.predict(scaler.transform([[mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitper, mdvp_jitabs,
                                                                  mdvp_rap, mdvp_ppq, jitter_ddp, mdvp_shim,
                                                                  mdvp_shim_db, shimm_apq3, shimm_apq5, mdvp_apq,
                                                                  shimm_dda, nhr, hnr, rpde, dfa, spread1, spread2,
                                                                  d2, ppe]]))
            print('prediction is', prediction)

            if prediction == 1:
                pred = "You have Parkinson's Disease. Please consult a doctor."
            else:
                pred = "You are a Healthy Person."

            
            return render_template('predict.html', prediction=pred)

        except Exception as e:
            print('The Exception message is: ', e)
            return render_template('failure.html')
    else:
        return render_template('index_1.html')

if __name__ == "__main__":
    app.run(debug=True)
