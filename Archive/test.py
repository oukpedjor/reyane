# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
#!/usr/bin/python
import getopt
import json
import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import pyspark.sql.functions as F
import pyspark.sql.types as T
import sys

def main(argv):
   inputfile = False
   outputfile = False
   jumbledwordsfile= False
   try:
      opts, args = getopt.getopt(argv,"i:o:j:",["ifile=","ofile=","jumbletestfile="])
   except getopt.GetoptError:
      print('vec2bin.py -i <dictionary inputfile> -o <dictionary outputfile> -j <jumbled words list file>')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-j", "--jumbletestfile"):
         jumbledwordsfile = arg

   if not inputfile or not outputfile or not jumbledwordsfile:
       print('vec2bin.py -i <dictionary inputfile> -o <dictionary outputfile> -j <jumbled words list file>')
       sys.exit(2)

   print inputfile
   print outputfile
   print jumbledwordsfile



if __name__ == "__main__":
   main(sys.argv[1:])
