import regex as re
import pandas as pd
from pythainlp.tokenize import word_tokenize
from asrtoolkit import cer
import numpy as np
import matplotlib.pyplot as plt

df_output = pd.read_excel('output.xlsx')
column = ["Kaldi", "Partii", "Google", "Gowajee"]
num = [["1","หนึ่ง"],["2","สอง"],["3","สาม"],["4","สี่"],["5","ห้า"],["6","หก"],["7","เจ็ด"],["8",'แปด'],["9","เก้า"],["0","ศูนย์"]]
index_to_rm = []
for k,i in df_output.iterrows():
  for c in column:
    try:
      i[c] = i[c].replace(" ","")
    except AttributeError:
      index_to_rm.append(k)
      continue
  
  truth = True
  for c in column:
    truth =  i[c] != ''
  if truth : index_to_rm.append(k)
  try:
    if re.search('[a-zA-Zๆ]', i["Kaldi"]) or re.search('[a-zA-Zๆ]', i["Partii"]) or re.search('[0-9]', i["Partii"]) or re.search('[0-9]', i["Gowajee"]) or re.search('[a-zA-Zๆ]', i["Gowajee"]):
        index_to_rm.append(k)
  except TypeError:
    index_to_rm.append(k)
    continue
  if 'ๆ' in i["Ground Truth"]:
    sep = word_tokenize(i["Ground Truth"])
    for index,value in enumerate(sep):
      if value == 'ๆ':
        sep[index] = sep[index-1]
      elif value[-1] == 'ๆ':
        sep[index] = value[:len(value) - 1] + value[:len(value) - 1]
    i['Ground Truth'] = ''.join(sep)

df_filtered = df_output.drop(index_to_rm)

cer_kaldi_partii = []

for k,v in df_output.iterrows():
  ground_truth = v["Ground Truth"]
  try:
    cer_kaldi_partii.append([cer(ground_truth,v["Kaldi"]),  cer(ground_truth,v["Partii"]) ,cer(ground_truth,v["Google"]), cer(ground_truth,v["Gowajee"])],)
  except:
    continue

cer_kaldi_partii = np.array(cer_kaldi_partii)  
print("Kaldi cer : ", cer_kaldi_partii[:,0].sum()/cer_kaldi_partii.shape[0])
print("Partii cer : ", cer_kaldi_partii[:,1].sum()/cer_kaldi_partii.shape[0])
print("Google cer : ", cer_kaldi_partii[:,2].sum()/cer_kaldi_partii.shape[0])
print("Gowajee cer : ", cer_kaldi_partii[:,3].sum()/cer_kaldi_partii.shape[0])

print("Kaldi Correct : ", (cer_kaldi_partii[:,0]==0.0).sum(),"=====", str(round((cer_kaldi_partii[:,0]==0.0).sum()/cer_kaldi_partii.shape[0]*100,2)),"%")
print("Partii Correct : ", (cer_kaldi_partii[:,1]==0.0).sum(),"=====", str(round((cer_kaldi_partii[:,1]==0.0).sum()/cer_kaldi_partii.shape[0]*100,2)),"%")
print("Google Correct : ", (cer_kaldi_partii[:,2]==0.0).sum(),"=====", str(round((cer_kaldi_partii[:,2]==0.0).sum()/cer_kaldi_partii.shape[0]*100,2)),"%")
print("Gowajee Correct : ", (cer_kaldi_partii[:,3]==0.0).sum(),"=====", str(round((cer_kaldi_partii[:,3]==0.0).sum()/cer_kaldi_partii.shape[0]*100,2)),"%")

print("From : ", cer_kaldi_partii.shape[0])