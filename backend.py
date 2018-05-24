# -*- coding: utf-8 -*-
"""
Created on Thu May 15 22:08:52 2018

@author: Amauri
"""
import os
import stat
import time
import re
import numpy as np
import pandas as pd
import sqlite3 as lite
import sys

class back(object):
    
    """"""
    #----------------------------------------------------------------------
        
    def getSize(self, rowObj):
        count = 0
        for row in rowObj:
            f = open((row.path).replace('\\','/'), 'r')
            for line in f:
                try:
                    file_name = re.sub('_', ' ', line)
                except:
                    file_name = "not_desired_row"
                no_mult_space = re.sub(' +', ' ', line)
                if "procs" in no_mult_space or "swpd" in no_mult_space:
                    continue;
                if file_name in no_mult_space:
                    continue;
                count += 1
            f.close()
        return count
        
    #----------------------------------------------------------------------
    def getFiles(self, rowObj):
        """"""
        colums_name = ['r','b','swpd', 'livre', 'buffer','cache','si','so', 
        'bi', 'bo', 'in', 'cs', 'us', 'sy', 'id', 'wa', 'st','name', 'date', 'time'
        ]
        count = self.getSize(rowObj)
        df = pd.DataFrame(index=np.arange(count), columns=colums_name)
        i = 0
        for row in rowObj:
            f = open((row.path).replace('\\','/'), 'r')
            for line in f:
                try:
                    file_name = re.sub('_', ' ', line)
                except:
                    file_name = "not_desired_row"
                no_mult_space = re.sub(' +', ' ', line)
                
                if "procs" in no_mult_space or "swpd" in no_mult_space:
                    continue;
                if file_name in no_mult_space:
                    wordList = no_mult_space.split()
                    print(wordList) #print ServerName, day and time 
                    server_name = wordList[0]
                    server_date = wordList[1]
                    server_time = wordList[2]   
                
                list_param = no_mult_space.split()
                if len(list_param) < len(colums_name) - 3:
                    list_param.append(-1)
                list_param.append(server_name)
                list_param.append(server_date)
                list_param.append(server_time)
                
                if len(list_param) == len(colums_name) or len(list_param) == len(colums_name) - 1: 
                    for param, colum in zip(list_param,colums_name):
                        df[colum][i] = param
                    i += 1
            
            
            f.close()
        df.to_csv("teste.csv", sep=',')
        return df
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    def addToDatabase(self, rowObj):
        """"""
        data_files = self.getFiles(rowObj)
        
        print("--------------------------------------DATAFRAME DESTE ARQUIVO--------------------------------")
        #print (data_files['name'].values)
        
        con = None
 
        try:
            con = lite.connect('servidores.db')
            cur = con.cursor()    
            cur.execute("create table if not exists Servidor(r INT, b INT, swpd INT, livre INT, buffer INT, cache INT, si INT, so INT, bi INT, bo INT, in_ INT, cs INT, us INT, sy INT, id INT, wa INT, st INT, name TEXT, date TEXT, time TEXT)")
            data_files.to_sql("Servidor", con, if_exists="append")
            con.commit()
            data = cur.fetchone()
            cur.execute("Select * from Servidor")
            con.commit()
            data = cur.fetchone()
        except lite.Error as er:
            print ("Database error: %s" % er)
            sys.exit(1)
        finally:    
            if con:
                cur = con.cursor()
                cur.execute("SELECT * from Servidor")
                results = cur.fetchall()
                print(results)
                con.close()
        
    #----------------------------------------------------------------------
    def dropDatabase(self, rowObj):
        """"""
        con = None
 
        try:
            con = lite.connect('servidores.db')
            cur = con.cursor()    
            cur.execute('DELETE FROM Servidor')
            con.commit()
            data = cur.fetchone()
            print (data)               
        except lite.Error as er:   
            print ("Error %s:" % er)
            sys.exit(1)
        finally:    
            if con:
                con.close()