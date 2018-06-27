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
      print('spark-submit resolvejumbledword.py -i <dictionary inputfile> -o <dictionary outputfile> -j <jumbled words list file>')
      sys.exit(2)
    for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-j", "--jumbletestfile"):
         jumbledwordsfile = arg

    if not inputfile or not outputfile or not jumbledwordsfile:
       print('spark-submit resolvejumbledword.py -i <dictionary inputfile> -o <dictionary outputfile> -j <jumbled words list file>')
       sys.exit(2)

    print inputfile
    print outputfile
    print jumbledwordsfile
   
    reformatjson(inputfile, outputfile)
    conf = SparkConf().setAppName("Spark jumble resolution")
    sc = SparkContext(conf=conf)
    #sc = pyspark.SparkContext('Reyane')
    sqlContext = SQLContext(sc)
    df = sqlContext.read.option('multinode', True).json(outputfile)
    # Displays the content of the DataFrame to stdout

    print('printing the dataframe as it is from the json file loaded ')
    df.show()

    word_udf = F.UserDefinedFunction(sort_string_chars, T.StringType())


    df = df.withColumn("sortedChartWORD", word_udf('word'))
   
    rank_udf = F.UserDefinedFunction(modify_rank_of_zero, T.IntegerType())
   
    df = df.withColumn("modifiedRank", rank_udf('rank'))

    print('printing the dataframe with a newly add column')

    df.show()
   
    sqlContext.registerDataFrameAsTable(df, "table1")
   
    lines = readjumbledwordfile(jumbledwordsfile)
    sqlstatment = "SELECT * FROM table1 WHERE sortedChartWORD='" + sort_string_chars(lines[0]) + "'"
    firstline=lines[0]
    lines.remove(lines[0])
    for x in lines: 
        sqlstatment = sqlstatment + " OR sortedChartWORD='" + sort_string_chars(x) + "'"
    
    print (sqlstatment)
   
    #lines2=lines.append(firstline)
    #length=len(lines)
    lines=lines+[firstline]
    df2 = sqlContext.sql(sqlstatment)
    #df2=sqlContext.sql("SELECT * FROM table1 WHERE sortedChartWORD='adgln' OR sortedChartWORD='ajmor' OR sortedChartWORD='abcelm' OR sortedChartWORD='aelrwy'")
   
    df2 = df2.toPandas()
    print("Printing the pandas dataframe")
    print (df2)
    print('')
    print("********** Printing the results **********")
    
    for x in lines:
        df3 = df2[df2['sortedChartWORD'] == sort_string_chars(x)]
        print('')
        print('Printing the best matched word for ' + x + ':')
        if df3['word'].count()==0:
            print("No match")
        else:
            print(df3.sort_values(by=['modifiedRank'], ascending=True).iloc[0]['word'])
    print("********** End of the results **********")
    
   




    #df=df.filter(df['sortedChartWORD']==sortedJumbledWord).sort("rank",ascending=False).first()

    #print (df)

    #print("printing the matching words")
    #row=df.filter(df['sortedChartWORD']==sortedJumbledWord).sort("modifiedRank",ascending=True).first()
    #print(row.word)
   

   
   
   
   
   
def reformatjson(inputfilename, outputfilename):
    "this reformat the json to make is consumable by spark api"
    if not os.path.exists(outputfilename):
        with open(inputfilename) as jsonfile:
            js = json.load(jsonfile)
        #now write a new file
        with open(outputfilename, 'w') as outfile:
            for d in js:
                json.dump({"word": d, "rank": js[d]}, outfile)
                outfile.write('\n')
                
def readjumbledwordfile(jumbledwordsfilename):
    with open(jumbledwordsfilename) as f:
        content = f.read().splitlines()
        return content
    

def sort_string_chars(col):
    newCol = ''.join(sorted(col))
    return newCol

def modify_rank_of_zero(col):
    if (col == 0):
        return 10000
    else:
        return col
                

if __name__ == "__main__":
   main(sys.argv[1:])


