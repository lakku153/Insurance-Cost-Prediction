from flask import Flask,request,render_template
import pickle
from src.pipeline.predict_pipeline import customdata,predictpipeline

application=Flask(__name__)
app=application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=customdata(
            age=int(request.form.get('age')),
            sex=request.form.get('gender'),
            bmi=float(request.form.get('bmi')),
            children=int(request.form.get('children')),
            smoker=request.form.get('smoker'),
            region=request.form.get('region')
        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)

        predict_pipe=predictpipeline()
        results=predict_pipe.predict_(pred_df)
        return render_template('home.html',results=round(results[0],2))

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)