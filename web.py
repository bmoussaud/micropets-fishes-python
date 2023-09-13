from flask import Flask
from flask import json
from flask import jsonify
from markupsafe import escape
from pyservicebinding import binding

import platform
 
hostname = platform.node()

app = Flask(__name__)

def fromValue():

    try:
        sb = binding.ServiceBinding()
        bindings_list = sb.bindings("config","acs")
        print("bindings_list")
        print(bindings_list)
        return bindings_list[0]['micropets.from']
    except binding.ServiceBindingRootMissingError as msg:
        # log the error message and retry/exit
        print("SERVICE_BINDING_ROOT env var not set")
        return "NotFound"


def fishes():
    data = dict()
    data['Total']=5
    data['Hostname']=hostname
    data['Pets']=[
           {"Index":0,"Name":"Nemoo","Kind":"Fish Clown","Age":14,"URL":"https://www.sciencesetavenir.fr/assets/img/2019/07/10/cover-r4x3w1000-5d258790dd324-f96f05d4901fc6ce0ab038a685e4d5c99f6cdfe2-jpg.jpg","From":fromValue(),"URI":"/fishes/v1/data/0"},
           {"Index":1,"Name":"Glumpy","Kind":"Neon Tetra","Age":11,"URL":"https://www.fishkeepingworld.com/wp-content/uploads/2018/02/Neon-Tetra-New.jpg","From":fromValue(),"URI":"/fishes/v1/data/1"},
           {"Index":2,"Name":"Dory","Kind":"Pacific regal blue tang","Age":12,"URL":"http://www.oceanlight.com/stock-photo/palette-surgeonfish-image-07922-671143.jpg","From":fromValue(),"URI":"/fishes/v1/data/2"},
           {"Index":3,"Name":"Argo","Kind":"French Fighter","Age":27,"URL":"https://www.aquaportail.com/pictures1003/anemone-clown_1267799900_poisson-combattant.jpg","From":fromValue(),"URI":"/fishes/v1/data/3"}]

    return data

@app.route('/')
@app.route('/fishes/v1/data')
def pets():
    print("get pets")   
    return jsonify(fishes())

@app.route('/fishes/v1/data/<index>')
def pet(index):    
    print("get pet "+index)
    pets = fishes()['Pets']
    for pet in pets:        
        if pet['Index']==int(index):
            return jsonify(pet)    
    return jsonify([])

@app.route('/fishes/v1/config')
def config():    
    config ={}
    config['kind']='fish'
    config["datasource.driver"]="Memory"
    config["datasource.url"]="Memory"
    return jsonify(config)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
