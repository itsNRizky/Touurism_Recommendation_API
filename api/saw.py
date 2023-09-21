import pandas as pd
from sklearn.preprocessing import minmax_scale

class SAW:
  """
    Class untuk implementasi SAW.

    ...

    Attributes
    ----------
    data : dict
        data awal implementasi SAW
    data_for_saw : dict
        dataframe untuk implementasi SAW
    weights : dict
        kumpulan bobot untuk implementasi SAW

    Methods
    -------
    choose_column_for_saw(self, columns):
        Memilih kolom yang akan diimplementasi SAW

    normalize_data_frame(self, columns, invert_value):
        Normalisasi kolom yang dipilih

    scroring(self, weights):
        Melakukan perhitungan final dengan bobot

    show_data_frame(self):
        Mengembalikan hasil dari implementasi SAW
    """
  def __init__(self, data):
    '''
    Menginisiasi atribute awal

    parameters:
      data = data dari database
    '''
    self.data = pd.DataFrame(data)
    self.data_for_saw = pd.DataFrame()
    self.weights = {}

  def choose_column_for_saw(self, columns):
    '''
    Memilih kolom pada data yang akan diimplementasi SAW

    parameters:
      columns = list kolom yang akan digunakan pada implementasi SAW

    return: (void)
      Memasukkan kolom kolom tertentu yang akan diimplementasi SAW pada atribute data_for_saw
    '''
    self.data_for_saw = self.data[columns].copy()

  def normalize_data_frame(self, columns, invert_value):
    '''
    Melakukan normalisasi pada kolom yang dipilih beserta inversinya

    parameters:
      columns = list kolom yang akan dilakukan normalisasi
      invert_value = list kolom yang hasil normalisasinya perlu diinversi

    return: (void)
      Melakukan modifikasi pada atribut data_for_saw agar memiliki nilai yang ternormalisasi
    '''
    for index in range(len(columns)):
      if invert_value[index]:
        self.data_for_saw[columns[index]] = 1 -  minmax_scale(self.data_for_saw[columns[index]])
      else:
        self.data_for_saw[columns[index]] = minmax_scale(self.data_for_saw[columns[index]])
  
  def scoring(self, weights):
    '''
    Memberikan bobot pada tiap cell dan menjadikan skor akhir implementasi SAW

    parameters:
      weights = bobot yang didapat dari preferensi user

    return: (void)
      Menambah satu kolom dan mengisi kolom tersebut dengan skor
    '''
    scores = []
    for row in self.data_for_saw.iterrows():
      score = sum(row[1][column] * weight for column, weight in weights.items())
      scores.append(score)
    
    self.data['score'] = scores

  def show_data_frame(self):
    '''
    Mengembalikan hasil skor yang sudah dibuat

    return: 
      dictionary daftar data
    '''
    return self.data.sort_values(by='score', ascending=False).to_dict('records')
  
