getShellText = lambda text: "=" * 10 + text + "=" * 10
print(getShellText('[ π μ§νμ²  νΌμ‘λ μμΈ‘ π ]'), '\nLoading...')


import matplotlib.pyplot as plt
import tensorflow.compat.v1 as tf
from rich.console import Console
from rich.table import Table
from rich.progress import track
from datetime import datetime
from utils import loadDataPandas

tf.disable_v2_behavior()
plt.rc('font', family='Malgun Gothic')


print(getShellText('[ λͺ¨λ λ‘λ© μλ£ β ]'))

column_names = [
  'μ¬μ©μ',
  'νΈμ λͺ',
  'μ§νμ² μ­',
  '00μ-01μ μΉμ°¨μΈμ',
  '00μ-01μ νμ°¨μΈμ',
  '01μ-02μ μΉμ°¨μΈμ',
  '01μ-02μ νμ°¨μΈμ',
  '02μ-03μ μΉμ°¨μΈμ',
  '02μ-03μ νμ°¨μΈμ',
  '03μ-04μ μΉμ°¨μΈμ',
  '03μ-04μ νμ°¨μΈμ',
  '04μ-05μ μΉμ°¨μΈμ',
  '04μ-05μ νμ°¨μΈμ',
  '05μ-06μ μΉμ°¨μΈμ',
  '05μ-06μ νμ°¨μΈμ',
  '06μ-07μ μΉμ°¨μΈμ',
  '06μ-07μ νμ°¨μΈμ',
  '07μ-08μ μΉμ°¨μΈμ',
  '07μ-08μ νμ°¨μΈμ',
  '08μ-09μ μΉμ°¨μΈμ',
  '08μ-09μ νμ°¨μΈμ',
  '09μ-10μ μΉμ°¨μΈμ',
  '09μ-10μ νμ°¨μΈμ',
  '10μ-11μ μΉμ°¨μΈμ',
  '10μ-11μ νμ°¨μΈμ',
  '11μ-12μ μΉμ°¨μΈμ',
  '11μ-12μ νμ°¨μΈμ',
  '12μ-13μ μΉμ°¨μΈμ',
  '12μ-13μ νμ°¨μΈμ',
  '13μ-14μ μΉμ°¨μΈμ',
  '13μ-14μ νμ°¨μΈμ',
  '14μ-15μ μΉμ°¨μΈμ',
  '14μ-15μ νμ°¨μΈμ',
  '15μ-16μ μΉμ°¨μΈμ',
  '15μ-16μ νμ°¨μΈμ',
  '16μ-17μ μΉμ°¨μΈμ',
  '16μ-17μ νμ°¨μΈμ',
  '17μ-18μ μΉμ°¨μΈμ',
  '17μ-18μ νμ°¨μΈμ',
  '18μ-19μ μΉμ°¨μΈμ',
  '18μ-19μ νμ°¨μΈμ',
  '19μ-20μ μΉμ°¨μΈμ',
  '19μ-20μ νμ°¨μΈμ',
  '20μ-21μ μΉμ°¨μΈμ',
  '20μ-21μ νμ°¨μΈμ',
  '21μ-22μ μΉμ°¨μΈμ',
  '21μ-22μ νμ°¨μΈμ',
  '22μ-23μ μΉμ°¨μΈμ',
  '22μ-23μ νμ°¨μΈμ',
  '23μ-24μ μΉμ°¨μΈμ',
  '23μ-24μ νμ°¨μΈμ',
]
slot_names = column_names[3:]

dataset = loadDataPandas.read('./dataset/subway.csv', column_names)
stations = list(set(dataset['μ§νμ² μ­'].to_numpy()))


class App:
  def __init__(self, station):
    self.__station = station
    self.select_dataset = dataset[dataset['μ§νμ² μ­'] == station][slot_names].to_numpy()
    # placeholderλ, μ²μμ λ³μλ₯Ό μ μΈν  λ κ°μ λ°λ‘ μ£Όλ κ²μ΄ μλλΌ, λμ€μ κ°μ λμ Έμ£Όλ κ³΅κ°μ λ§λ€μ΄μ£Όλ κ²
    # νλΌλ―Έν°λ₯Ό shape none μΌλ‘ ν¬κΈ°λ₯Ό μ ν΄μ§μ§μμμΌλ‘ μ€μ , μ΄λ κ² νλ©΄, shapeμ΄ μ ν΄μ§μ§ μμμ 1μ°¨μλΆν° λ€ λμ¬ μ μλ€λ κ²μ μλ―Έ
    # μλ£λ₯Ό μλ ₯λ°μ νλ μ΄μ€ νλλ₯Ό μ€μ 
    self.X = tf.placeholder(tf.float32, shape=None)
    self.Y = tf.placeholder(tf.float32, shape=None)
    #tf.random.uniformμ μνλ ννμ λλ€ κ°μ κ°μ§ λ°°μ΄μ λ§λ¬
    # xμ yμ μκ΄κ΄κ³λ₯Ό μ€λͺνκΈ°μν λ³μλ₯Ό -100λΆν° 100κΉμ§ κ· λ±λΆν¬ uniform distribution(μ°μκ· λ±λΆν¬)μ κ°μ§ λ¬΄μμ κ°μΌλ‘ μ΄κΈ°νν¨
    self.W = tf.Variable(tf.random_uniform([1], -100, 100), 'weight')
    self.b = tf.Variable(tf.random_uniform([1], -100, 100), 'bias')
    self.H = self.X * self.W + self.b
    # xκ° μ£Όμ΄ μ‘μλ, yλ₯Ό λ§λ€μ΄ λΌμ μλ wμ bλ₯Ό μ°Ύλκ², wλ weight, bλ bias.
    # νμ (x,y)μ λ°μ΄ν°μ λν μμ€κ°μ κ³μ°νλ ν¨μ. μ€μ κ°κ³Ό λͺ¨λΈλ‘ μμΈ‘ν κ°μ΄ μΌλ§λμ°¨μ΄κ° λλκ°λ₯Ό λνλ΄λκ°. Cost function μ΄λΌκ³ λν¨ 
    # μ¦, loss functionμ΄ μμμλ‘ κ·Έλͺ¨λΈμ΄ μ£Όμ΄μ§ xκ°μ λν΄ yκ°μ μ ννκ² μμΈ‘νκ².
    self.cost = tf.reduce_mean(tf.square(self.H - self.Y))
    # Gradient descent Optimizer ν¨μλ₯Ό μ¬μ©ν΄μ μμ€κ°μ μ΅μν νλ μ°μ° κ·Έλνλ₯Ό μμ±ν΄μΌνλ€.
    # Wμ Bμ κ°μ λ³κ²½ν΄κ°λ©΄μ μμ€κ°μ μ΅μν μν€λλ‘ νλλ°, ν¨μμ κΈ°κ΅΄κΈ°λ₯Ό μνκ³ , κΈ°μΈκΈ°κ° λ?μ μͺ½μΌλ‘ κ³μ μ΄λμν€λ μκ³ λ¦¬μ¦μ΄λ€.
    # learning_rate(νμ΅λ₯ )μ λ§€κ°λ³μλ‘ νλλ° μ΄κ²μ μ¦, νμ΅μ μΌλ§λ 'κΈνκ²' ν κ²μΈκ°μ λν λ³μμ΄λ€.
    # νμ΅λ₯ μ΄ ν¬λ©΄ μ΅μ μ μμ€κ°μ λͺ»μ°Ύκ³  μ§λμΉκ²λκ³ , λλ¬΄ μμΌλ©΄ νμ΅ μλκ° λλ €μ§λ€.
    # μ΄κ²μ hyperparameterλΌκ³  νλλ°, κ³μ λ³κ²½ν΄κ°λ©° μ΅μ μ κ°μ μ°Ύλ κ²λ μ€μνλ€.
    optimizer = tf.train.GradientDescentOptimizer(tf.Variable(0.001))
    self.train = optimizer.minimize(self.cost)
    self.congestion_session = 0
    self.x_data = list(range(24))
    self.y_data = []
    self.slots  = []
    self.getString = lambda x: '0' + str(x) if x < 10 else str(x)
    self.now = 0
  
  '''
  def findRideAndQuitData(self):
    new_data = [[], []]  
    for data in self.select_dataset:
      ride = []
      quit = []
      for i in range(48):
        if i % 2 == 0:
          quit.append(data[i])
          continue
        ride.append(data[i])
      new_data[0].append(ride)
      new_data[1].append(quit)
    return new_data

  def drawRideAndQuitGraph(self):
    _data = self.findRideAndQuitData()
    for i in range(len(_data[0])):
      plt.plot(_data[0][i], _data[1][i], 'ro')
      plt.title(f'{self.__station}μ μΉΒ·νμ°¨ μΈμ μ κ΄κ³')
      plt.xlabel('μΉμ°¨ μΈμ')
      plt.ylabel('νμ°¨ μΈμ')
      plt.show()


  def trainingRideAndQuitModel(self):
    _data = self.findRideAndQuitData()
    x_data = np.ravel(_data[0], order='C')
    y_data = np.ravel(_data[1], order='C')
    X = tf.placeholder(tf.float32, shape=None)
    Y = tf.placeholder(tf.float32, shape=None)
    W = tf.Variable(tf.random_uniform([1], -100, 100), 'weight')
    b = tf.Variable(tf.random_uniform([1], -100, 100), 'bias')
    H = X * W + b
    cost = tf.reduce_mean(tf.square(H - Y))
    optimizer = tf.train.GradientDescentOptimizer(tf.Variable(0.00000000001))
    train = optimizer.minimize(cost)
    session = tf.Session()
    session.run(tf.global_variables_initializer())
    for step in range(100001):
      session.run(train, feed_dict = { X: x_data, Y: y_data })
      if step % 10000 == 0:
        print(step, session.run(cost, feed_dict = { X: x_data, Y: y_data }), session.run(W), session.run(b))
    return session
  '''
  #μΉνμ°¨ ν© κ³μ° λμΆ = new_data
  def findCongestionData(self):
    new_data = []
    for data in self.select_dataset:
      layer = []
      for i in range(0, 48, 2):
        ride = data[i]
        quit = data[i + 1]
        layer.append(ride + quit)
      new_data.append(layer)
    return new_data
  #νΌμ‘λ κ·Έλν (plt λ³κ²½κ°λ₯ μ€μ  μμ )
  def drawCongestionGraph(self):
    _data = self.findCongestionData()
    for arr in _data:    plt.plot(arr, 'ro')
    plt.title(f'{self.__station}μ μκ°λλ³ νΌμ‘λ')
    plt.xlabel('μκ°λ')
    plt.ylabel('νΌμ‘λ')
    plt.show()

  # νΌμ‘λ νλ ¨ λͺ¨λΈ
  # tf.session (νμνλ‘ μ€νμ°½μΌλ‘ μ°μκ²°κ³Ό νμΈνκΈ°)
  def trainingCongestionModel(self):
    select_dataset = dataset[dataset['μ§νμ² μ­'] == self.__station][slot_names]
    new_data = {}
    session = tf.Session()  # μΈμ μ λ¬Έ
    session.run(tf.global_variables_initializer()) # λ³μ μ΄κΈ°ν -> μ΅κ³Όννλ κ²μ΄ μ’μμ
    for i in range(0, 48, 2):
      new_data[slot_names[i][:7]] = sum(
        select_dataset[
          [
            slot_names[i],
            slot_names[i + 1]
          ]
        ].sum().to_numpy()
      ) // len(select_dataset)
    new_data = sorted(new_data.items(), key=lambda x:x[1])
    for i in range(len(new_data)):
      self.y_data.append(new_data[i][1])
      self.slots.append(new_data[i][0])
    print()
    for _ in track(range(10000), description="νμ΅ μ€...", style="white"):
      session.run(
        self.train,
        feed_dict = {
          self.X: self.x_data,
          self.Y: self.y_data
        },
      )
    self.congestion_session = session

  def getNowSlotIndex(self):
    self.now = datetime.now()
    hour = self.now.hour
    return self.slots.index(
      f'{self.getString(hour)}μ-{self.getString(hour + 1)}μ'
    )

  #νΌμ‘λ μμΈ‘ νμ΄λΈ λ‘μ§
  
  def predictionCongestion(self):
    if self.congestion_session == 0:  return 0
    i = self.getNowSlotIndex()
    result = self.congestion_session.run(self.H, feed_dict={ self.X: [i] })[0]
    average = sum(self.y_data) // 24
    max_result = max(self.y_data)
    console = Console()
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("νμ¬ μκ° ", style="dim", width=12)
    table.add_column("μ­ ")
    table.add_column("νΌμ‘λ ")
    table.add_column("μΉΒ·νμ°¨ μΈμ ")
    table.add_column("μν ")
    table.add_row(
      self.getString(self.now.hour) + ':' + self.getString(self.now.minute),
      self.__station,
      str(round(result / max_result * 100, 5)) + '%',
      str(result if result > 0 else 0),
      "νΌμ‘ν¨" if result > average else "μ¬μ λ‘μ",
    )
    console.print(table)

    


while 1:
  station = input('\n\nπ κΆκ΅Όνμ  μ­μ μλ ₯ν΄μ£ΌμΈμ?? (μ’λ£: 0)\n')
  if station == '0':  break
  if stations.count(station) != 0:
    app = App(station)
    print()
    app.trainingCongestionModel()
    print(f'\n{getShellText("[ νμ΅ μλ£ ]")}\n\n')
    app.predictionCongestion()
    app.drawCongestionGraph()
    continue
  print('=> ν΄λΉ μ­μ λ°μ΄ν°λ₯Ό μ‘°νν  μ μμ΅λλ€.')
