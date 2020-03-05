# coding: utf-8

import socket
import httplib
import sqlparse
import fonctions
import sys
from sqlparse.sql import IdentifierList, Identifier,Function,Parenthesis,Token
from sqlparse.tokens import Keyword, DML,DDL,Whitespace,Punctuation,Literal,String,Token,Wildcard
import urllib
socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind(('', 8888))

def reception_inf_auth(client):
 login=client.recv(1024)
 mdp=client.recv(1024)
 return [login,mdp]

def demandeClient():
 demande_client=""
 chaine_saisie=client.recv(1024)
 while chaine_saisie!='' and chaine_saisie[len(chaine_saisie)-1]!=";":
  demande_client+=chaine_saisie+" "
  chaine_saisie=client.recv(1024)
 if chaine_saisie[len(chaine_saisie)-1]==";":
  demande_client+=chaine_saisie
 if demande_client=='quit;':
  client.send("00")
 else:
  return demande_client

def transformation_request(demande_client):
 parsed = sqlparse.parse(demande_client)[0]
 request= parsed.tokens
 global request_whitespaceless
 request_whitespaceless=[]
 parsed_request_without_whitespaces(request,request_whitespaceless)
 '''print request
 print request_whitespaceless
 print request_whitespaceless[1]
 print type(request_whitespaceless[1])'''

'''def envoi_request_to_httpserver_et_envoi_reponse_to_client(url_api,i):
  httpServ.request('GET',url_api)
  response=httpServ.getresponse()
  result=response.read()
  print 'resultat'
  print result  
  return result
'''
'''def verification_DATABASE(url_api):
 httpServ.request('GET',url_api)
 response=httpServ.getresponse()
 result=response.read()
 if result=="0":
  return "0"
 else:
  return result
'''

def analyseur_type_syntaxe_request(req_parsed_tokens):
 if req_parsed_tokens[0].value.upper()=='CREATE':
  if req_parsed_tokens[1].value.upper()=='TABLE':
   return analyseur_CREATE_TABLE(req_parsed_tokens)
  elif req_parsed_tokens[1].value.upper()=='USER':
   return analyseur_CREATE_USER(req_parsed_tokens)
  else:
   return analyseur_CREATE_DATABASE(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='DROP':
  if req_parsed_tokens[1].value.upper()=='TABLE':
   return analyseur_DROP_TABLE(req_parsed_tokens)
  elif req_parsed_tokens[1].value.upper()=='USER':
   return analyseur_DROP_USER(req_parsed_tokens)
  else:
   return analyseur_DROP_DATABASE(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='ALTER':
  if req_parsed_tokens[3].value.upper()=='DROP':
   return analyseur_ALTER_TABLE_DROP_COLUMN(req_parsed_tokens)
  elif req_parsed_tokens[3].value.upper()=='ADD':
   return analyseur_ALTER_TABLE_ADD_CONSTRAINT(req_parsed_tokens)
  else:
   return analyseur_ALTER_TABLE_RENAME(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='INSERT':
  return analyseur_INSERT(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='UPDATE':
  return analyseur_UPDATE(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='DELETE':
  return analyseur_DELETE(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='SELECT':
  if type(req_parsed_tokens[1]) is not sqlparse.sql.Token and type(req_parsed_tokens[1]) is not sqlparse.sql.IdentifierList:
   if req_parsed_tokens[1][0].value.upper()=='DATABASE':
    return analyseur_SELECT_DATABASE(req_parsed_tokens)
   elif req_parsed_tokens[1][0].value.upper()=='USER':
    return analyseur_SELECT_USER(req_parsed_tokens)
  elif len(req_parsed_tokens)>=5 and type(req_parsed_tokens[4]) is sqlparse.sql.Where:
   return analyseur_SELECT_WHERE(req_parsed_tokens)
  else:
   return analyseur_SELECT(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='USE':
  return analyseur_USE_DATABASE(req_parsed_tokens)
 elif req_parsed_tokens[0].value.upper()=='SHOW':
  if req_parsed_tokens[1].value.upper()=='DATABASES':
   return analyseur_SHOW_DATABASES(req_parsed_tokens)
  else:
   return analyseur_SHOW_TABLES(req_parsed_tokens)
 else:
  return 0




def parsed_request_without_whitespaces(req_parsed_tokens,req_parsed_tokens_whitespaceless):
 i=0
 while(i<len(req_parsed_tokens)):
  if req_parsed_tokens[i].ttype is not  Whitespace:
   req_parsed_tokens_whitespaceless.append(req_parsed_tokens[i])
  i+=1

def analyseur_CREATE_TABLE(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='CREATE' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='TABLE' 
 and type(req_parsed_tokens[2]) is sqlparse.sql.Function and req_parsed_tokens[3].ttype is Punctuation): 
  return 1
 else:
  return 0

def analyseur_CREATE_USER(req_parsed_tokens):
 if (
 req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='CREATE' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='USER'  
 and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is Keyword and req_parsed_tokens[3].value.upper()=='IDENTIFIED'
 and req_parsed_tokens[4].ttype is Keyword and req_parsed_tokens[4].value.upper()=='BY' 
 and req_parsed_tokens[5].ttype is None and req_parsed_tokens[6].ttype is Punctuation):
  return 2
 else:
  return 0


def analyseur_CREATE_DATABASE(req_parsed_tokens):
 if(req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='CREATE'
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='DATABASE' and req_parsed_tokens[2].ttype is None
 and req_parsed_tokens[3].ttype is Punctuation):
  return 3
 else:
  return 0

def analyseur_USE_DATABASE(req_parsed_tokens):
 if(req_parsed_tokens[0].ttype is Keyword and req_parsed_tokens[0].value.upper()=='USE'
 and req_parsed_tokens[1].ttype is None and req_parsed_tokens[2].ttype is Punctuation):
  return 15
 else:
  return 0

def analyseur_DROP_TABLE(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='DROP' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='TABLE' 
 and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is Punctuation):
  return 4
 else:
  return 0

def analyseur_DROP_DATABASE(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='DROP' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='DATABASE' 
 and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is Punctuation):
  return 5
 else:
  return 0

def analyseur_DROP_USER(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='DROP' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='USER' 
 and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is Punctuation):
  return 6
 else:
  return 0

def analyseur_ALTER_TABLE_DROP_COLUMN(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='ALTER' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='TABLE' 
 and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is DDL and req_parsed_tokens[3].value.upper()=='DROP'
 and req_parsed_tokens[4].ttype is Keyword and req_parsed_tokens[4].value.upper()=='COLUMN' and req_parsed_tokens[5].ttype is None
 and req_parsed_tokens[6].ttype is Punctuation):
  return 7
 else:
  return 0

def analyseur_ALTER_TABLE_RENAME(req_parsed_tokens):
  if (req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='ALTER' 
  and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='TABLE' 
  and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is Keyword  and req_parsed_tokens[3].value.upper()=='RENAME'
  and req_parsed_tokens[4].ttype is Keyword and req_parsed_tokens[4].value.upper()=='TO' and req_parsed_tokens[5].ttype is None
  and req_parsed_tokens[6].ttype is Punctuation):
   return 8
  else:
   return 0

def analyseur_ALTER_TABLE_ADD_CONSTRAINT(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DDL and req_parsed_tokens[0].value.upper()=='ALTER' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='TABLE' 
 and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is Keyword and req_parsed_tokens[3].value.upper()=='ADD'
 and req_parsed_tokens[4].ttype is Keyword and req_parsed_tokens[4].value.upper()=='CONSTRAINT' and req_parsed_tokens[5].ttype is None
 and req_parsed_tokens[6].ttype is Keyword and req_parsed_tokens[6].value.upper()=='PRIMARY' 
 and req_parsed_tokens[7].ttype is Keyword and req_parsed_tokens[7].value.upper()=='KEY' and req_parsed_tokens[8].ttype is None
 and req_parsed_tokens[9].ttype is Punctuation):
  return 9
 else:
  return 0

def analyseur_INSERT(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DML and req_parsed_tokens[0].value.upper()=='INSERT' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='INTO' 
 and type(req_parsed_tokens[2]) is sqlparse.sql.Identifier and type(req_parsed_tokens[3]) is sqlparse.sql.Values and req_parsed_tokens[4].ttype is Punctuation):
  return 10
 else:
  return 0

def analyseur_UPDATE(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DML and req_parsed_tokens[0].value.upper()=='UPDATE'
 and req_parsed_tokens[1].ttype is None  
 and req_parsed_tokens[2].ttype is Keyword and req_parsed_tokens[2].value.upper()=='SET' 
 and req_parsed_tokens[3].ttype is None and req_parsed_tokens[4].ttype is None):
  return 11
 else:
  return 0

def analyseur_DELETE(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DML and req_parsed_tokens[0].value.upper()=='DELETE'
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='FROM'
 and req_parsed_tokens[2].ttype is None and req_parsed_tokens[3].ttype is None):
  return 12
 else:
  return 0

def analyseur_SELECT(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DML and req_parsed_tokens[0].value.upper()=='SELECT'
 and (req_parsed_tokens[1].ttype is None or req_parsed_tokens[1].ttype is None
 or req_parsed_tokens[1].ttype is Token.Wildcard)
 and req_parsed_tokens[2].ttype is Keyword and req_parsed_tokens[2].value.upper()=='FROM' 
 and req_parsed_tokens[3].ttype is None and req_parsed_tokens[4].ttype is Punctuation):
  return 13
 else:
  return 0  

def analyseur_SELECT_WHERE(req_parsed_tokens):
 if (req_parsed_tokens[0].ttype is DML and req_parsed_tokens[0].value.upper()=='SELECT'
 and (req_parsed_tokens[1].ttype is None or req_parsed_tokens[1].ttype is None
 or req_parsed_tokens[1].ttype is Token.Wildcard)
 and req_parsed_tokens[2].ttype is Keyword and req_parsed_tokens[2].value.upper()=='FROM' 
 and req_parsed_tokens[3].ttype is None and req_parsed_tokens[4].ttype is None):
  return 14
 else:
  return 0

def analyseur_SHOW_DATABASES(req_parsed_tokens):
 if(req_parsed_tokens[0].ttype is Keyword and req_parsed_tokens[0].value.upper()=='SHOW' 
 and type(req_parsed_tokens[1]) is sqlparse.sql.Identifier and req_parsed_tokens[1].value.upper()=='DATABASES'
 and req_parsed_tokens[2].ttype is Punctuation):
  return 16
 else:
  return 0

def analyseur_SHOW_TABLES(req_parsed_tokens):
 if(req_parsed_tokens[0].ttype is Keyword and req_parsed_tokens[0].value.upper()=='SHOW' 
 and req_parsed_tokens[1].ttype is Keyword and req_parsed_tokens[1].value.upper()=='TABLES'
 and req_parsed_tokens[2].ttype is Punctuation): 
  return 17
 else:
  return 0

def analyseur_SELECT_DATABASE(req_parsed_tokens):
 if(req_parsed_tokens[0].ttype is DML and req_parsed_tokens[0].value.upper()=='SELECT'
 and type(req_parsed_tokens[1]) is sqlparse.sql.Function and req_parsed_tokens[1][0].value.upper()=='DATABASE' 
 and req_parsed_tokens[2].ttype is Punctuation):
  return 18
 else:
  return 0

def analyseur_SELECT_USER(req_parsed_tokens):
 if(req_parsed_tokens[0].ttype is DML and req_parsed_tokens[0].value.upper()=='SELECT'
 and type(req_parsed_tokens[1]) is sqlparse.sql.Function and req_parsed_tokens[1][0].value.upper()=='USER'
 and req_parsed_tokens[2].ttype is Punctuation):
  return 19
 else:
  return 0



def splited_string_whitespaceless(s,s_without_spaces):
 i=0
 while i<len(s):
  if s[i]!=' ':
   s_without_spaces.append(s[i])
  i+=1


def traitement_CREATE_TABLE(request_whitespaceless,nom_user,base_courante):
 fonction_create_table=request_whitespaceless[2]
 F=fonction_create_table.tokens
 fonction_create_table_without_spaces=[]
 parsed_request_without_whitespaces(F,fonction_create_table_without_spaces)
 print fonction_create_table_without_spaces
 p=sqlparse.sql.Parenthesis(fonction_create_table_without_spaces[1])
 p_tokens=p.tokens
 p_tokens_en_string=str(p_tokens)
 p_tokens_en_string= p_tokens_en_string[1 : len(p_tokens_en_string)-1] 
 p_tokens_en_string_tableau=' '.join(p_tokens_en_string.split())
 liste_colonnes=p_tokens_en_string_tableau.split(',')
 nom_table=str(fonction_create_table[0])
 liste_colonnes_en_string=''
 for n in liste_colonnes:
  liste_colonnes_en_string+=n+' '
 #liste_colonnes_en_string=liste_colonnes_en_string.replace(' ','%20')
 #print liste_colonnes_en_string
 return [nom_table,liste_colonnes_en_string]


def traitement_CREATE_USER(request_whitespaceless):
 nom_user=str(request_whitespaceless[2])
 mdp=str(request_whitespaceless[5])
 return [nom_user,mdp]

def traitement_CREATE_DATABASE(request_whitespaceless,nom_user):
 nom_database=str(request_whitespaceless[2])
 return nom_database

def traitement_DROP_TABLE(request_whitespaceless,base_courante):
 nom_table=str(request_whitespaceless[2])
 return nom_table

def traitement_DROP_DATABASE(request_whitespaceless):
 nom_database=str(request_whitespaceless[2])
 return nom_database

def traitement_DROP_USER(request_whitespaceless):
 nom_user=str(request_whitespaceless[2])
 return  nom_user

def traitement_ALTER_TABLE_DROP_COLUMN(request_whitespaceless,base_courante):
 nom_table=str(request_whitespaceless[2])
 nom_column=str(request_whitespaceless[5])
 return [nom_table,nom_column]


def traitement_ALTER_TABLE_RENAME(request_whitespaceless,base_courante):
 nom_table=str(request_whitespaceless[2])
 nouveau_nom_table=str(request_whitespaceless[5])
 return [nom_table,nouveau_nom_table]

def traitement_ALTER_TABLE_ADD_CONSTRAINT(request_whitespaceless,base_courante):
 nom_table=str(request_whitespaceless[2])
 colonne_concerne_tab=request_whitespaceless[8]
 colonne_concerne_tokens=colonne_concerne_tab.tokens
 colonne_concerne=str(colonne_concerne_tokens[1])
 return [nom_table,colonne_concerne]



def traitement_INSERT(request_whitespaceless,base_courante,nom_user):
 nom_table=str(request_whitespaceless[2])
 values=request_whitespaceless[3]
 values_token=values.tokens
 valeurs=values_token[1]
 valeurs_en_string=str(valeurs)
 valeurs_en_string=valeurs_en_string[valeurs_en_string.find('(')+1 : valeurs_en_string.find(')')]
 splited_valeurs_en_string=valeurs_en_string.split(',')
 #print nom_table
 return [nom_table,valeurs_en_string]
 

'''
def traitement_UPDATE(request_whitespaceless,base_courante):
 nom_table=str(request_whitespaceless[1])
 modif=str(request_whitespaceless[3])
'''  
def traitement_USE_DATABASE(request_whitespaceless,nom_user):
 nom_database=str(request_whitespaceless[1])
 return nom_database

def traitement_SHOW_DATABASES(nom_user):
 return nom_user
 

def traitement_SHOW_TABLES(nom_user,base_courante):
 return [nom_user,base_courante]

def traitement_SELECT_DATABASE(base_courante):
 if base_courante=='':
  return 'No database used.'
 else:
  return base_courante

def traitement_SELECT_USER(nom_user):
 return nom_user

def formation_url(request_whitespaceless,nom_user,base_courante):
 value_request=analyseur_type_syntaxe_request(request_whitespaceless)
 if value_request==0:
  result="Invalid syntax."
 elif value_request==1:
  [nom_table,liste_colonnes_en_string]=traitement_CREATE_TABLE(request_whitespaceless,nom_user,base_courante)
  result=fonctions.createTable(nom_table,liste_colonnes_en_string,base_courante,nom_user)
 elif value_request==2:
  [nom_user,mdp]=traitement_CREATE_USER(request_whitespaceless)
  result=fonctions.createUser(nom_user,mdp)
 elif value_request==3:
  nom_database=traitement_CREATE_DATABASE(request_whitespaceless,nom_user)
  result=fonctions.createDatabase(nom_database,nom_user)
 elif value_request==4:
  nom_table=traitement_DROP_TABLE(request_whitespaceless,base_courante)
  result=fonctions.dropTable(nom_table)
 elif value_request==5:
  nom_database=traitement_DROP_DATABASE(request_whitespaceless)
  result=fonctions.dropDatabase(nom_database)
 elif value_request==6:
  user=traitement_DROP_USER(request_whitespaceless)
  result=fonctions.dropUser(user)
 elif value_request==7:
  [nom_table,nom_column]=traitement_ALTER_TABLE_DROP_COLUMN(request_whitespaceless,base_courante)
  result=fonctions.alterTableDropColumn(nom_table,nom_column,base_courante,nom_user)
 elif value_request==8:
  [nom_table,nouveau_nom_table]=traitement_ALTER_TABLE_RENAME(request_whitespaceless,base_courante)
  result=fonctions.alterTableRename(nom_table,nouveau_nom_table,base_courante,nom_user)
 elif value_request==9:
  [nom_table,colonne_concerne]=traitement_ALTER_TABLE_ADD_CONSTRAINT(request_whitespaceless,base_courante)
  result=fonctions.alterTableAddConstraint(nom_table,colonne_concerne,base_courante)
 elif value_request==10:
  [nom_table,valeurs_en_string]=traitement_INSERT(request_whitespaceless,base_courante,nom_user)
  result=fonctions.insertIntoTable(base_courante,nom_user,nom_table,valeurs_en_string)
 elif value_request==16:
  result=fonctions.showDatabases(nom_user)
 elif value_request==17:
  result=fonctions.showTables(nom_user,base_courante)
 else:
  result=' '
 return result


while True:
       socket.listen(5)
       client, address = socket.accept()
       login=client.recv(1024)
       client.send("l")
       mdp=client.recv(1024)
       client.send("m")
       result=fonctions.auth(login,mdp)
       if(result=="1"):
        client.send("1")
       else:
        client.send("-1")
       select_db=False
       used_db=''
       while True:
        while select_db==False:
         demande_client=demandeClient()
         transformation_request(demande_client)
         i=analyseur_type_syntaxe_request(request_whitespaceless)
         if (i!=15 and i!=3 and i!=2 and i!=16 and i!=18 and i!=19):
          if i==0:
           client.send("Invalid syntax.")
          else:
           client.send("Create or use a database first.")
         elif i==3:
          used_db=traitement_CREATE_DATABASE(request_whitespaceless,login)
          result=fonctions.createDatabase(used_db,login)
          client.send(result)
         elif i==2:
          if login=='root':
           [nom_user,password]=traitement_CREATE_USER(request_whitespaceless)
           result=fonctions.createUser(nom_user,password)
           client.send(result)
          else:
           client.send("Permission denied.")
         elif i==16:
          result=fonctions.showDatabases(login)
          client.send(result)
         elif i==18:
          client.send(traitement_SELECT_DATABASE(used_db))
         elif i==19:
          client.send(traitement_SELECT_USER(login))
         else:
          nomDatabase=traitement_USE_DATABASE(request_whitespaceless,login) 
          result=fonctions.useDatabase(nomDatabase,login)
          if result=="0":
           client.send("Inexisting database.")
           used_db=''
          else:
           select_db=True
           client.send("Database selected.")
           used_db=nomDatabase
        demande_client=demandeClient()
        transformation_request(demande_client)
        i=analyseur_type_syntaxe_request(request_whitespaceless)
        bc=used_db
        if i==0:
         client.send("Invalid syntax.")
        elif i==15:
         nomDatabase=traitement_USE_DATABASE(request_whitespaceless,login)
         result=fonctions.useDatabase(nomDatabase,login)
         if result=="0":
          client.send("Inexisting database.")
          used_db=bc
         else:
          client.send("Database selected.")
          used_db=nomDatabase
        elif i==2:
         if login=='root':
          [nom_user,password]=traitement_CREATE_USER(request_whitespaceless)
          result=fonctions.createUser(nom_user,password)
          client.send(result)
         else:
          client.send('Permission denied.')
        elif i==18:
         client.send(traitement_SELECT_DATABASE(used_db))
        elif i==19:
         client.send(traitement_SELECT_USER(login))
        else:
         result=formation_url(request_whitespaceless,login,used_db)
         print 'result'
         print result
         client.send(result)
print "Close"
client.close()
socket.close()
