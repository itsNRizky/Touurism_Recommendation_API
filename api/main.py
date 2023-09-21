from flask import Flask, jsonify, request
from bson import ObjectId
import json
from db import get_penginapan, get_transportasi, get_wisata
from flask_cors import CORS
from saw import SAW

#Middleware untuk menerima semua respond agar dapat di baca pada server Flask
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
    
#Preference yang dibutuhkan untuk destinasi wisata
destination_preference = {
    'pm': {
        'ticket': 0.6,
        'rating': 0.3,
        'station_to_destination' : 0.1
    },
    'dn': {
        'ticket': 0.4,
        'rating': 0.3,
        'station_to_destination': 0.3
    },
    'pn': {
        'ticket': 0.2,
        'rating': 0.4,
        'station_to_destination': 0.4
    }
}

#Menjalankan server beserta middleware
app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
# CORS(app, resources={r"/api/*": {"origins": "https://touurism-recommendation.vercel.app"}})
CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)
app.json_encoder = JSONEncoder

@app.route('/', methods=['GET'])

def index():
    '''Halaman cek kondisi server'''
    response = jsonify({'status': 200})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/bestplaces', methods=['POST'])
def get_best_places():
    '''
    Mendapatkan semua data destinasi wisata

    request-param:
        id = id destinasi wisata

    return:
        json dari daftar destinasi wisata
    '''
    print(request.args['id'])
    res = get_wisata(request.args['id'])
    response = jsonify(res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route('/api/recommend_transportasi', methods=['POST'])
def recommend_transportasi():
    '''
    Merekomendasikan transportasi berdasarkan dari respond yang diterima melalui method POST

    request-body:
        origin = hasil form keberangkatan user
        arrival = hasil form waktu kedatangan user
        budget = hasil form budget yang dimiliki user
        transport_preference = hasil form preferensi user terhadap transportasi
        stay_preference = hasil form preferensi user terhadap penginapan

    return:
        json dari daftar transportasi
    '''
    json_from_reqs = request.get_json()
    print(json_from_reqs)
    transportasi = get_transportasi(json_from_reqs['origin'], json_from_reqs['departure'], json_from_reqs['budget'])
    print(transportasi)
    df_transportasi = SAW(transportasi)
    df_transportasi.choose_column_for_saw(['id', 'train_class', 'price'])
    df_transportasi.normalize_data_frame(['train_class', 'price'], [False, True])
    df_transportasi.scoring({
        'train_class' : json_from_reqs['transport_preference']/100,
        'price' : (100 - json_from_reqs['stay_preference'])/100
        })
    return jsonify(df_transportasi.show_data_frame())


@app.route('/api/recommend_wisata', methods=['GET', 'POST'])
def recommend_wisata():
    '''
    Merekomendasikan wisata berdasarkan dari respond yang diterima melalui method POST dan GET

    request-body:
        budget = hasil form budget yang dimiliki user
        destination_preference = hasil form preferensi user terhadap destinasi wisata
    
    return:
        json dari daftar wisata
    '''
    json_from_reqs = request.get_json()
    wisata = get_wisata(budget=json_from_reqs['budget'])
    df_wisata = SAW(wisata)
    df_wisata.choose_column_for_saw(['id','ticket', 'rating', 'station_to_destination'])
    df_wisata.normalize_data_frame(['ticket', 'rating', 'station_to_destination'], [True, False, True])
    df_wisata.scoring(destination_preference[json_from_reqs['destination_preference']])
    return df_wisata.show_data_frame()


@app.route('/api/recommend_penginapan', methods=['POST'])
def recommend_penginapan():
    '''
    Merekomendasikan penginapan berdasarkan dari respond yang diterima melalui method POST

    request-body:
        budget = hasil form budget yang dimiliki user
        stay_preference = hasil form preferensi user terhadap penginapan

    return:
        json dari daftar penginapan
    '''
    json_from_reqs = request.get_json()
    penginapan = get_penginapan(json_from_reqs['budget'])
    df_penginapan = SAW(penginapan)
    df_penginapan.choose_column_for_saw(['id', 'type', 'price'])
    df_penginapan.normalize_data_frame(['type', 'price'], [False, True])
    df_penginapan.scoring({
        'type': json_from_reqs['stay_preference']/100,
        'price': (100 - json_from_reqs['stay_preference'])/100
        })
    return df_penginapan.show_data_frame()
