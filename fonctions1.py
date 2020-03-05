#!/usr/bin/env python
# -*- coding: utf8 -*-
import json
import os.path
def estvide(Monfichier):
	if(os.path.getsize(Monfichier)==0):
		return 0
	else:
		return 1

def tableexiste(Monfichier,nametable):
        dic=dict()
        g=open(Monfichier,'r')
        dic=json.load(g)
        for n in dic.keys():
                if(n==nametable):
                        return 1
        return 0

def userexiste(Monfichier,nameuser):
        dic=dict()
        g=open(Monfichier,'r')
        dic=json.load(g)
        for n in dic.keys():
                if(n==nameuser):
                        return 1
        return 0

def cle(Monfichier,nametable):
        dic=dict()
        g=open(Monfichier,'r') 
        dic=json.load(g)
        t=[]
        d={}
        p=[]
        for nametable in dic.keys():
                t=dic[nametable]
                for i in range(len(t)):
                        p=t[i].keys()
        f=list(p)
        return f;

def esttype(typ):
	tabtyp=["int","string","varchar","float","double","bool","str","integer","varchar(30)","varchar(100)"]
	for i in range(len(tabtyp)):
		if(tabtyp[i]==typ):
			return 1
	return 0


def estcontrainte(cont):
	tabcont=["not null","primary key","foreign key",""]
	for i in range(len(tabcont)):
		if(tabcont[i]==cont):
			return 1
	return 0



def gestion_des_champs(champs,liste_colonnes,liste_types,liste_contraintes):
 print 'mes champs'
 print champs
 splited_liste_champs=champs.split()
 contrainte1=""
 i=0
 while i<len(splited_liste_champs):
  if (splited_liste_champs[i].upper()!='PRIMARY' and splited_liste_champs[i].upper()!='FOREIGN' 
  and splited_liste_champs[i].upper()!='NOT'):
   liste_colonnes.append(splited_liste_champs[i])
   i+=2
  else:
   contrainte1+=splited_liste_champs[i]+" "
   i+=2
 splited_contrainte1=contrainte1.split()
 i=1
 contrainte2=''
 while i<len(splited_liste_champs):
  if (splited_liste_champs[i].upper()!='KEY' and splited_liste_champs[i].upper()!='NULL'):
   liste_types.append(splited_liste_champs[i])
   i+=2
  else:
   contrainte2+=splited_liste_champs[i]+" "
   i+=2
 splited_contrainte2=contrainte2.split()
 i=0
 while i<len(splited_contrainte1):
  liste_contraintes.append(splited_contrainte1[i]+' '+splited_contrainte2[i])
  i+=1
 if(len(liste_contraintes)!=len(liste_colonnes)):
  i=0
  while i<((len(liste_colonnes)-len(liste_contraintes))+1):
   liste_contraintes.append('')
   i+=1


def creerdico(tabAttr,tabcont,tabtype):
        print 'tabAttr'
        print tabAttr
        print 'tabcont'
        print tabcont
        print 'tabtype'
        print tabtype
	dicti=dict()
	tab=[]
	for i in range(0,len(tabcont)):
		nomAttr=tabAttr[i]
		typeAttr=tabtype[i]
		contAttr=tabcont[i]
		if(estcontrainte(contAttr.lower())==0 or esttype(typeAttr.lower())==0):
                        print estcontrainte(contAttr.lower())==0
                        print esttype(typeAttr.lower())==0
			return 0
		else:
			tab.append(typeAttr.lower())
			tab.append(contAttr.lower())
			dicti[nomAttr.lower()]=tab
			tab=[]
	return dicti


def createTable(nom_table,champs,base_courante,nom_user,mdp):
       res=auth(nom_user,mdp)
       if res==0:
        return "Authenticcation failed"
       else:
        liste_colonnes=[]
        liste_types=[]
        liste_contraintes=[]
        gestion_des_champs(champs,liste_colonnes,liste_types,liste_contraintes)
        dico=creerdico(liste_colonnes,liste_contraintes,liste_types)
        if dico==0:
         return "Incorrect type or constraint."
        else:
	 tmp=0;
	 tab=[]
         Monfichier=nom_user+'_'+base_courante+'.json'
	 if(estvide(Monfichier)!=0 and tableexiste(Monfichier,nom_table)==0 ):
		f = open(Monfichier,'r')
		dictionnaire = json.load(f)
		tab.append(dico)
		dictionnaire[nom_table]=tab
		with open(Monfichier,"w") as write_file:
		  write_file.write(json.dumps(dictionnaire,indent=4))
                return "Create table Ok."
	 elif(estvide(Monfichier)==0):
		dictionnaire=dict()
		tab.append(dico)
		f = open(Monfichier,'a')
		dictionnaire[nom_table]=tab
		json.dump(dictionnaire, f, indent=4)
		f.close ()
		return "Create table Ok."
	 else:
		return "Table already exits."

#print createTable("test1_2"," v varchar(30) primary key i integer not null","test1","root")
def auth(login,mdp):
 dico=dict()
 with open("Users.json",'r') as f:
      dico = json.load(f)
      if login in dico:
       if dico[login][0]["login"]==login and dico[login][0]["mdp"]==mdp: 
        return "1"
       else:
        return "0"

def createUser(nomUser,mdp):
 user_exists=userexiste("Users.json",nomUser)
 users_vide=estvide("Users.json")
 if (users_vide==1):
  if user_exists==1:
   return "Username already exists"
  else:
   dico=dict()
   f=open("Users.json",'r')  
   dico=json.load(f)
   f.close()
   dico[nomUser]=[]   
   dico[nomUser].append({"login":"{0}".format(nomUser),"mdp": "{0}".format(mdp)})
   with open("Users.json","w") as write_file:
    write_file.write(json.dumps(dico,indent=4))
   return "Create user OK."
 else:
   dico=dict()
   f = open("Users.json",'a')
   dico=json.load(f)
   json.dump(dico, f, indent=4)
   f.close()
   return "Create user OK."


def exist_fichier(nom_database,nom_user):
 dico=dict()
 trouv=False
 with open("Users.json","r") as write_file:
   dico=json.load(write_file)
   i=1
   while( i<len(dico[nom_user])):
    k=dico[nom_user][i]
    for j in k.keys():
     print k[j]
     if k[j]==nom_database:
      trouv=True
      return trouv
     else:
      trouv=False
     i+=1
   return trouv


def createDatabase(nom_database,nom_user):
 if exist_fichier(str(nom_database),str(nom_user))==False:
  f = open(nom_user+'_'+nom_database+".json",'w')
  f.write("{}")
  f.close()
  dico=dict()
  f = open("Users.json",'r')
  dico=json.load(f)
  i=len(dico[nom_user])
  dico[nom_user].append({"{0}".format(i) : "{0}".format(nom_database)})
  with open("Users.json","w") as write_file:
    write_file.write(json.dumps(dico,indent=4))
  return "Create database OK."
 else:
  return "Database already exists."

def useDatabase(nomDatabase,nom_user):
 if exist_fichier(nomDatabase,nom_user)==False:
  return "0"
 else:
  return "1"

def dropTable(nomTable,baseC):
 return "Drop table OK."

def dropDatabase(nomDatabase):
 return "Drop database OK."

def dropUser(nomUser):
 return "Drop user OK."



def alterTableDropColumn(table,nomattribut,baseC,nom_user):
        Monfichier=nom_user+'_'+baseC+".json"
	if(estvide(Monfichier)==0):
		return "Table {0} doesn't exist in the database.".format(table)
	else:
		f=open(Monfichier,'r')
		dico=json.load(f)
                print 'dico'
                print dico
	t=[]
	p=[]
	l=[]
	d=dict()
	r=[]
	cl=cle(Monfichier,table)
        print 'cl'
        print cl
	if(tableexiste(Monfichier,table)==0):
		return "Inexisting table {0}".format(table)
	else:
		d=dico[table]
                print 'd'
                print d
		#for i in range(len(d)):
		for n in cl:
                                       print n
                                       if(n==nomattribut):
					print 'd[0][n]'
                                        print d[0][n]
					del d[0][n]
					print("aprés")
					print(dico)
					with open(Monfichier,"w") as write_file:
						write_file.write(json.dumps(dico,indent=4))
                                        return "Column {0} dropped from {1}.".format(nomattribut,table)
                                       else:
                                        print "NIce"

#print alterTableDropColumn("test1_4","c","test1","root")

def alterTableRename(nomtable,nouveaunom,baseC,nom_user):
        Monfichier=nom_user+'_'+baseC+".json"
	dico=dict()
	d=[]
	s=""
        if nomtable==nouveaunom:
                return "The old and the new name are the same." 
	if(estvide(Monfichier)==0):
		return "Table doesn't exist in the database."
	else:
		f=open(Monfichier,'r')
		dico=json.load(f)
                if(tableexiste(Monfichier,nouveaunom)==1):
                 return "There is already a table named {0} in the database.".format(nouveaunom)
		if (tableexiste(Monfichier,nomtable)==1):
			for n in dico.keys():
				d.append(str(n))
			for i in range(len(d)):
				if(d[i]==nomtable):
					c=d[i]
					d[i]=nouveaunom
					dico[d[i]]=dico[c]
					del dico[c] 
			with open(Monfichier,"w") as write_file:
				write_file.write(json.dumps(dico,indent=4))
			return "Table {0} renamed to {1}.".format(nomtable,nouveaunom)
                else:
                        return "Table to rename doesn't exist in the selected database."

#print alterrename("root_test1.json","test1_1","test1_2")



def alterTableAddConstraint(nomTable,columnConcerne,baseC):
 return "Add constraint OK."


def ajout_traits():
 list_db=''
 i=0
 while i<20:
  list_db+='-'
  i+=1
 return list_db

def showDatabases(nomUser):
 dico=dict()
 with open("Users.json","r") as write_file:
   dico=json.load(write_file)
   list_db=""
   list_db+=ajout_traits()
   list_db+='\nDatabases\n'
   list_db+=ajout_traits()
   list_db+='\n'
   i=1
   while( i<len(dico[nomUser])):
    k=dico[nomUser][i]
    for j in k.keys():
     list_db+=str(k[j])+"\n"
    i+=1
   list_db+=ajout_traits()
   return list_db 

def showTables(nomUser,baseC):
 if baseC=='':
  return "0"
 else:
  dico=dict()
  list_tables=""
  list_tables+=ajout_traits()
  list_tables+='\n'
  list_tables+='Tables\n'
  list_tables+=ajout_traits()
  list_tables+='\n'
  with open(nomUser+'_'+baseC+".json","r") as write_file:
   dico=json.load(write_file)
   for j in dico.keys():
    list_tables+=str(j)+"\n"
  list_tables+=ajout_traits()
  return list_tables

def tuple_exit(dicotable,dicouser,nom_table):
	for s in dicotable[nom_table]:
		#print(s)
		if(s==dicouser):
			return 1
	return 0


def insertIntoTable(nametable,valeurs,nomdb,nomuser):
        Monfichier=nomuser+'_'+nomdb+".json"
        dic=dict()
	t=[]
	d={}
	f=dict()
	tabl=[]
	if(estvide(Monfichier)==1 and tableexiste(Monfichier,nametable)==1):
		g=open(Monfichier,'r')
		dic=json.load(g)
		print(dic)
		f=dic[nametable]
                print 'CLES'
                print dic[nametable][0].keys()
		t=cle(Monfichier,nametable)
		for j in range(len(t)):
			l=t[j]
			d[l]=tab[j]
			tabl=d
			#print("je teste ma fonction")
			#print(dic)
			print(utilisateurexiste(dic,d))
			if(utilisateurexiste(dic,d)==1):
				print("l'utilisateur existe")
			else:
				f.append(d)
				dic[nametable]=f
				k=open(Monfichier,'w')
				json.dump(dic, k, indent=4)
				print("utilisateur ajouté")

		#print(t)
	else:
		print("base vide ou table innexistante")
#print insertIntoTable("test1_4",valeurs,nomdb,nomuser)

def cle(Monfichier,nametable):
	dic=dict()
	g=open(Monfichier,'r') 
	dic=json.load(g)
	t=[]
	d={}
	p=[]
	for nametable in dic.keys():
		t=dic[nametable]
		for i in range(len(t)):
                        p=t[i].keys()
	f=list(p)
	return f 
