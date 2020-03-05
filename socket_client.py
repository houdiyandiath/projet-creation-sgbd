# coding: utf-8
from getpass import getpass
import sqlparse
import socket
import sys

def recuperation_des_arguments(args):
 if (len(args)!=7 and len(args)!=5 and len(args)!=3):
  print 'Erreur syntaxe connexion'
 elif len(args)==5:
  if (args[1]=='-h' and args[3]=='-u'):
   hote=args[2] 
   login=args[4]
   mdp=getpass("User Password: ")
   return [hote,login,mdp]
  else:
   print 'Erreur syntaxe connexion'
 elif len(args)==7:
  if (args[1]=='-h' and args[3]=='-u' and args[5]=='--password'):
   hote=args[2] 
   login=args[4]
   mdp=args[6]
   return [hote,login,mdp]
  else:
   print 'Erreur syntaxe connexion'
 elif len(args)==3:
  if (args[1]=='-h'):
   hote=args[2]
   login=raw_input("User login: ")
   mdp=getpass("User Password: ")
   return [hote,login,mdp]
  else:
   print 'Erreur syntaxe connexion'
 else:
   print 'Erreur syntaxe connexion'

[hote,login,mdp]=recuperation_des_arguments(sys.argv)

port = 8888
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
socket.send(login)
socket.recv(255)
socket.send(mdp)
socket.recv(255)
msg_recu=socket.recv(255)
if msg_recu=='0':
 print "Could not connect to the server."
elif msg_recu=='-1':
 print "Login or password incorrect"
else:
 while True:
  msg=raw_input("hmDB> ")
  while msg[len(msg)-1]!=';':
   msg+=" "+raw_input("hmDB> ")
  socket.send(msg.encode("Utf8"))
  result=socket.recv(1024)
  if result=='00':
   print 'Bye.'
   sys.exit()
  else:
   print result
