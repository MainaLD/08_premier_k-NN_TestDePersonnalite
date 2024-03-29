from json import load
import numpy as np
import pandas as pd
import os
import joblib

class Question:
     def __init__(self, prompt):
          self.prompt = prompt
          #self.answer = answer

question_prompts = [
    
    "Question 1 :\nQuelle importance accordez-vous au succès ?\n\n(a)Une importance moyenne.\n(b)Une très grande importance.\n(c)Le succès ne me préoccupe pas beaucoup.\n",
    
    "\nQuestion 2 :\nVous est-il déjà arrivé de prendre des jours de congé parce que vous étiez stressé(e) ?\n\n(a)Une ou deux fois.\n(b)Plus de deux fois.\n(c)Jamais.\n",

    "\nQuestion 3 :\nVous considère-t-on comme une personne sachant conserver son sang froid en période de crise ?\n\n(a)Parfois, mais ceux qui arrivent à garder la tête froide en période de crise n’ont généralement pas saisi la gravité de la situation.\n(b)Pas vraiment.\n(c)Oui, je pense être à juste titre perçu(e) ainsi.\n",

    '\nQuestion 4 :\nParmi les propositions suivantes, laquelle est la plus à même de vous détendre et de réduire votre stress après une journée particulièrement éprouvante ?\n\n(a)Quelques heures de sommeil dans ma chaise longue préférée.\n(b)Une bonne rasade de whiskey ou d’un autre alcool.\n(c)Une barre chocolatée.\n',

    '\nQuestion 5 :\nLes délais vous stimulent-ils ?\n\n(a)Non, mais les délais sont un mal nécessaire avec lequel il faut apprendre à vivre.\n(b)Non, les délais ont tendance à me stresser et je préfère travailler à mon rythme.Oui, je pense que je travaille mieux quand je suis sous pression.\n',

    '\nQuestion 6 :\nPensez-vous que la vie actuelle génère plus de stress qu’il y a 40 ans ?\n\n(1)Peut-être.\n(2)Oui.\n(3)Non.\n',

    '\nQuestion 7 :\nVotre neveu vous demande de garder ses trois enfants un peu turbulents pendant le week-end en raison d’une crise familiale. Comment envisagez-vous cette situation ?\n\n(1)Cela m’inquiète terriblement.\n(2)L’idée de garder ces trois enfants me terrifie à un point tel que je chercherai probablement un moyen d’y échapper.\n(3)C’est un nouveau défi que je relèverai avec plaisir.\n',

    '\nQuestion 8 :\nLe stress vous a-t-il déjà conduit(e) à endommager des choses ?\n\n(1)Non, je n’ai jamais rien fait de tel mais il m’est déjà arrivé de raccrocher brutalement le téléphone.\n(2)Oui.\n(3)Non.\n',

    '\nQuestion 9 :\nVous arrive-t-il d’être ennuyé(e) par des petits riens ?\n\n(1)Oui, parfois.\n(2)Assez souvent.\n(3)Rarement voire jamais.\n',

    '\nQuestion 10 :\nQue ressentiriez-vous si vous deviez vous familiariser avec une nouvelle technologie ?\n\n(1)Rien de particulier. Si je devais me familiariser avec un nouvel outil de travail pour des raisons professionnelles, je m’adapterais sans difficulté.\n(2)Cela m’inquièterait un peu.\n(3)J’aime apprendre des choses nouvelles, je trouve cela très intéressant.\n',


]

Interpretation = [
    'Score entre 15 et 30 (A) : \n\nVous savez très bien gérer votre stress. \nVous êtes très probablement perçu(e) comme quelqu’un de très détendu presque toujours capable de garder le sens des proportions.',
    'Score entre 10 et 14 (B) : \n\nMême s’il vous arrive d’être tendu(e) et stressé(e) en certaines occasions, vous semblez donc capable de prendre soin de vous-même et de dire non aux requêtes déraisonnables.',
    'Score moins de 10 (C) : \n\nVotre score indique que le stress vous affecte de façon négative.',
    ]


questions = [
      Question(question_prompts[0]),
      Question(question_prompts[1]),
      Question(question_prompts[2]),
      Question(question_prompts[3]),
      Question(question_prompts[4]),
      Question(question_prompts[5]),
      Question(question_prompts[6]),
      Question(question_prompts[7]),
      Question(question_prompts[8]),
      Question(question_prompts[9]),
]

def run_quiz(questions, Interpretation):
     score = 0
     Data = []
     for question in questions:
          answer = input(question.prompt)
          Data.append(answer)
          if answer == 'a' or answer == '1':
               score += 1
          elif answer == 'b' or answer == '2':
              score += 0
          elif answer == 'c' or answer == '3':
              score += 2
     
     print("\nVotre Score est : ", score,'\n')
     
     print('--------------------------------------------------------')
     print('\n--------- Interprétation final avec score  ---------\n')
     print('--------------------------------------------------------')
     
     if score < 30 and score >=15:
         Label = 'A'
         print(Interpretation[0])
     elif score < 15 and score >=10:
         Label = 'B'
         print(Interpretation[1])
     elif score < 10:
         Label = 'C'
         print(Interpretation[2])
     print('-----------------------------------------\n')
      
     Data.append(score)
     Data.append(Label)
     Data = np.array(Data)
     # chr = character
    #  Plus besoin de name_generator  car pas de stockage à effectuer
     #name_generator = chr(np.random.randint(500))+chr(np.random.randint(500))+chr(np.random.randint(500))
     
     d = {'Q1' : Data[0],
             'Q2' : Data[1],
             'Q3' : Data[2],
             'Q4' : Data[3],
             'Q5' : Data[4],
             'Q6' : Data[5],
             'Q7' : Data[6],
             'Q8' : Data[7],
             'Q9' : Data[8],
             'Q10' : Data[9],
             'Score' : Data[10],
             'Interpretation' : Data[11],}
     
     print('--------------------------------------------------')
     print('\n--------- Interprétation final avec KNN  ---------\n')
     print('---------------------------------------------------')

    #  je transforme en DataFrame
     Data = pd.DataFrame(d, index=[1])
     
    #  je récupère mes 10 premier itérations
     for_test=Data.replace(["a","1","1.0"],1).replace(["b","2","2.0"],0).replace(["c","3","3.0"],2)
    #  je découpe ma dataframe
     for_test = for_test.iloc[0,0:10]
    #  transpose le
     for_test = np.expand_dims(for_test, axis = 0)
     load_model = joblib.load('KNN_Final')
     pred = load_model.predict(for_test)
    
    # je récupère la valeur dans ma 'liste'
     print('Prédiction KNN : ', pred[0])

     



    #  Plus besoin de name_generator  car pas de stockage à effectuer
    #  if any(File.endswith(".csv") for File in os.listdir('./Dataset/')):
    #     df = pd.read_csv('./DataSet/'+os.listdir('./DataSet/')[0])
    #     df = df.append(d, ignore_index=True)
    #     df.to_csv('./DataSet/'+os.listdir('./DataSet/')[0], index=False)
    #  else:
    #     df = pd.DataFrame(d, index = ['1'])
    #     df.to_csv('./DataSet/DataSet__'+name_generator+'__.csv', index=False) 
    #  return print(df)
        
run_quiz(questions, Interpretation)



