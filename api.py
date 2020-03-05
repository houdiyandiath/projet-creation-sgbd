#!/usr/bin/env python
# coding: utf-8
#import sqlparse as psr
from flask import Flask,request
from flask_restplus import Resource, Api, fields
from datetime import datetime
import fonctions
import fonctions1
import enum
import subprocess
import sys
app = Flask(__name__)
api = Api(app, version='1.0', title="API BDD", description="API base de donnees ")
parser = api.parser()
ns_tables=api.namespace('api/tables',description='gestion tables')
ns_users=api.namespace('api/users',description='gestion utilisateurs')
ns_databases=api.namespace('api/databases',description='gestion des bases de donnees')

@ns_tables.route('/createtable/<string:nomtable>/<string:colonnes>/<string:baseC>/<string:nomuser>/<string:mdp>')
class CreateTable(Resource):
 @api.doc(parser=parser)
 def get(self,nomtable,colonnes,baseC,nomuser,mdp):
  '''Ajouter table'''
  colonnes.replace('%20',' ')
  print colonnes
  return fonctions1.createTable(nomtable,colonnes,baseC,nomuser,mdp)

@ns_users.route('/createuser/<string:nomuser>/<string:mdp>/')
class CreateUser(Resource):
 @api.doc(parser=parser)
 def get(self,nomuser,mdp):
  '''Ajouter user'''
  return fonctions.createUser(nomuser,mdp)

@ns_databases.route('/createdatabase/<string:nomdatabase>/<string:nomuser>/')
class CreateDatabase(Resource):
 @api.doc(parser=parser)
 def get(self,nomdatabase,nomuser):
  '''Ajouter base de donnees'''
  return fonctions.createDatabase(nomdatabase,nomuser)

@ns_tables.route('/droptable/<string:nomtable>/<string:baseC>/')
class DropTable(Resource):
 @api.doc(parser=parser)
 def get(self,nomtable,baseC):
  '''Supprimer table'''
  return fonctions.dropTable(nomtable,baseC)

@ns_databases.route('/dropdatabase/<string:nomdatabase>/')
class DropDatabase(Resource):
 def get(self,nomdatabase):
  '''Supprimer database'''
  return fonctions.dropDatabase(nomdatabase)

@ns_users.route('/dropuser/<string:nomuser>/')
class DropUser(Resource):
 def get(self,nomuser):
  '''Supprimer user'''
  return fonctions.dropUser(nomuser)

@ns_tables.route('/altertable/dropcolumn/<string:nomtable>/<string:nomcolumn>/<string:baseC>/')
class AlterTableDropColumn(Resource):
 def get(self,nomtable,nomcolumn,baseC):
  '''Supprimer colonne d'une table'''
  return fonctions.alterTableDropColumn(nomtable,nomcolumn,baseC)


@ns_tables.route('/altertable/rename/<string:nomtable>/<string:nouveaunomtable>/<string:baseC>/')
class AlterTableRename(Resource):
 def get(self,nomtable,nouveaunomtable,baseC):
  '''Changer le nom de la table'''
  return fonctions.alterTableRename(nomtable,nouveaunomtable,baseC)

@ns_tables.route('/altertable/addconstraint/<string:nomtable>/<string:columnconcerne>/<string:baseC>/')
class AlterTableAddConstraint(Resource):
 def get(self,nomtable,columnconcerne,baseC):
  '''Changer contrainte sur une colonne'''
  return fonctions.alterTableAddConstraint(nomtable,columnconcerne,baseC)

@ns_tables.route('/insert/<string:nomtable>/<string:valeurs>/<string:baseC>/<string:nomuser>/')
class InsertIntoTable(Resource):
 def get(self,nomtable,valeurs,baseC,nomuser):
  '''Inserer dans une table'''
  return fonctions.insertIntoTable(nomtable,valeurs,baseC,nomuser)

@ns_users.route('/authenticate/<string:login>/<string:mdp>/')
class AuthentificationUser(Resource): 
 def get(self,login,mdp):
  '''Authentification user'''
  return fonctions.auth(login,mdp)

@ns_databases.route('/usedatabase/<string:login>/<string:nomdb>/')
class UseDatabase(Resource):
 def get(self,nomdb,login):
  '''Use database'''
  return fonctions.useDatabase(nomdb,login)

@ns_databases.route('/showdatabases/<string:login>/')
class ShowDatabases(Resource):
 def get(self,login):
  '''Show databases'''
  return fonctions.showDatabases(login) 

@ns_tables.route('/showtables/<string:login>/<string:nomdb>/')
class ShowTables(Resource):
 def get(self,login,nomdb):
  '''Show tables'''
  return fonctions.showTables(login,nomdb) 


if __name__ == '__main__':
 app.debug=True
 app.run("localhost",8889)
