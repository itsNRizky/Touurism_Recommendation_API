from pymongo.mongo_client import MongoClient

uri = 'mongodb+srv://its_nrizky:wFWE3yQdh3BIXnbn@tourism-recommendation.xxivixw.mongodb.net/?retryWrites=true&w=majority'
client  = MongoClient(uri)
db = client.recommendation_app_db

def get_wisata(id = '', budget=''):
  '''
  Mengambil Data Destinasi Wisata Dari Database.

  Tanpa ID: menampilkan semua destinasi wisata
  
  Tanpa Budget: menampilkan tanpa batas maksimum harga

  parameters:
    id(string) = id destinasi wisata

    budget(string) = budget yang dimiliki oleh user saat ini

  return:
    list destinasi wisata
  '''
  if id == '':
    try:
      wisata = db.wisata
      res = list(wisata.find({} if budget == '' else {'ticket' : {'$lte' : float(budget)}}, {'_id' : 0}))
      return res
    except Exception as e:
      print(e)
  else:
    try:
      wisata = db.wisata
      res = wisata.find_one({'id' : id}, {'_id': 0})
      return res
    except Exception as e:
      print(e)

def get_penginapan(budget):
  '''
  Mengambil Data Penginapan Dari Database.

  parameters:
    budget = budget yang dimiliki oleh user saat ini

  return:
    list penginapan
  '''
  try:
    penginapan = db.penginapan
    res = penginapan.find({'price' : {'$lt' : float(budget)}}, {'_id': 0, 'description': 0, })
    return res
  except Exception as e:
    print(e)

def get_transportasi(origin, departure, budget):
  '''
  Mengambil Data Transportasi Kereta Dari Database.

  parameters:
    origin = asal keberangkatan user

    departure =  preferensi waktu keberangkatan user

    budget = budget yang dimiliki oleh user saat ini

  return:
    list transportasi kereta
  '''
  try:
    transportasi = db.transportasi_kereta
    res = transportasi.find(
      {'departure_station' : origin, 
       'price' : {'$lt' : float(budget)}
       } if departure == 'Bebas' else 
       {'departure_station' : origin,
        'time_start_category' : departure,
        'price' : {'$lt' : int(budget)}
      }
      , {'_id' : 0}
      )
    return res
  except Exception as e:
    print(e)

