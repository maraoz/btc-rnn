
from shove import Shove
import csv

mem_store = Shove()
root = Shove('file://shovestore')


def parse(filename):
  print 'Parsing', filename
  n, e = filename.split('.')
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      date = row[0]
      if date == 'Date':
        names = row
        continue

      o = root[date] = root.get(date) or {}
      for index, name in enumerate(names):
        key = name if index is 0 else (n+'.'+name)
        o[key] = row[index]
      print date,len(o.keys())


parse('BAVERAGE-USD.csv')
parse('BCHAIN-ATRCT.csv')
parse('BCHAIN-AVBLS.csv')
parse('BCHAIN-BCDDE.csv')
parse('BCHAIN-CPTRA.csv')
parse('BCHAIN-ETRAV.csv')
parse('BCHAIN-HRATE.csv')
parse('BCHAIN-NADDU.csv')
parse('BCHAIN-NTRAN.csv')
parse('BCHAIN-NTREP.csv')
parse('BCHAIN-TOUTV.csv')
parse('BCHAIN-TRFEE.csv')
parse('BCHAIN-TVTVR.csv')


root.sync()


  

