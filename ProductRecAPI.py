from flask import Flask, request, jsonify, make_response
from flask_api import status 
from ProductRecModel import Recommender
app = Flask(__name__)
recommender = Recommender()



@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        needed_inputs=["ind_empleado","pais_residencia","sexo","age","ind_nuevo","antiguedad","indrel","indrel_1mes",
                    "tiprel_1mes","indresi","indext","conyuemp","canal_entrada","indfall","tipodom","ind_actividad_cliente",
                    "renta","segmento","prev_products"]
        messages =[]
        user = request.json.get('user', None)
        nums_of_products = request.json.get('products', 1)    
        if user:
            for input in needed_inputs:
                if user.get(input) is None :
                    messages.append(input+' is missing')
            if len(user['prev_products'])!=22:
                messages.append('prev_products size should be 22') 
        else:
            messages.append('User is not provided')    
        if messages:
            return make_response(jsonify({'message': messages}),status.HTTP_400_BAD_REQUEST)
        prods = recommender.recommendProducts(user, nums_of_products)
        return make_response(jsonify({"result": "success", "output":prods }),status.HTTP_200_OK)
    except:
        return make_response(jsonify({'message': "We need to do some maintenance ;)"}),status.HTTP_500_INTERNAL_SERVER_ERROR)
  
app.run(host='0.0.0.0',port=5000)



