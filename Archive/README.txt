This explains how to run the spark code in a resolvejumbledword.py file
1- Requirments
   a- Pandas needs to be installed and preferanbly. Here is how :
      pip install --upgrade pandas

   b- spark needs to be installed (instalation of spark is our of scope for this exercise)
 

1- How to run this 
 spark-submit resolvejumbledword.py -i <frequency dictionary inputfile > -o <frequency dictionary outputfile> -j <jumbled words list file>
 example: spark-submit resolvejumbledword.py -i freq_dict.json -o freq_dict2.json -j jumbledwords.txt

 As in you can see the frequency dictionary file ( freq_dict.json) is already included in  the same directory (it does not have to be in the same directory) as resolvejumbledword.py and a user needs to provide the "frequency dictionary outputfile".This is a json formatted file  consumable by spak that is dynamically generated , a user needs to tell the application where to print this file. The jumbled word list file is a list of jumbled words that the application needs to solve, a sample jumbledwords.txt is provided and it is in the same directory as the resolvejumbledword.py


2- Spark version:
 This code is written using spark 1.6.3.2 but should run with later versions 


3- Algorithm used by the resolvejumbledword.py

This code load the frequency dictionary outputfile which is formatted version of the frequency dictionary inputfile, as a spark dataframe. The initial dataframe looks like below:
+----+--------------+
|rank|          word|
+----+--------------+
|   0|     biennials|
|   0|    tripolitan|
|   0|     oblocutor|
|   0|  leucosyenite|
|   0|      chilitis|
|   0|     fabianist|
|   0|     diazeutic|
|   0|        alible|
|4601|         woods|
|   0|preadjournment|
|   0|       spiders|
|   0|     fabianism|
|   0|   outscolding|
|   0|    sperrylite|
|   0|      trawling|
|   0| cardiospermum|
|   0|    lighttight|
|   0|       spidery|
|   0|    regularize|
|   0|      beadsmen|
+----+--------------+

 

Then the spark peforms some transformation on the dataframe adding 2 more colums the purpose of which is to help solve the jumble. At this stage the dataframe will look like below:

+----+--------------+---------------+------------+
|rank|          word|sortedChartWORD|modifiedRank|
+----+--------------+---------------+------------+
|   0|     biennials|      abeiilnns|       10000|
|   0|    tripolitan|     aiilnoprtt|       10000|
|   0|     oblocutor|      bclooortu|       10000|
|   0|  leucosyenite|   ceeeilnostuy|       10000|
|   0|      chilitis|       chiiilst|       10000|
|   0|     fabianist|      aabfiinst|       10000|
|   0|     diazeutic|      acdeiituz|       10000|
|   0|        alible|         abeill|       10000|
|4601|         woods|          doosw|        4601|
|   0|preadjournment| adeejmnnoprrtu|       10000|
|   0|       spiders|        deiprss|       10000|
|   0|     fabianism|      aabfiimns|       10000|
|   0|   outscolding|    cdgilnoostu|       10000|
|   0|    sperrylite|     eeilprrsty|       10000|
|   0|      trawling|       agilnrtw|       10000|
|   0| cardiospermum|  acdeimmoprrsu|       10000|
|   0|    lighttight|     gghhiilttt|       10000|
|   0|       spidery|        deiprsy|       10000|
|   0|    regularize|     aeegilrruz|       10000|
|   0|      beadsmen|       abdeemns|       10000|
+----+--------------+---------------+------------+


 as one can see the sortedChartWORD column and the modifiedRank columns were add. The first one is the word column rewritten in a way it is the same word sorted by character , this is used to  search the possible matching words for a jumble one . The second column is the modifiedRank column . This is the same column as the rank colum except the value of 0 has been replaced by 10000. Because the higher is the rank , the less frequent is the word and 0 based on the game means the word is too frequent to be ranked. this transformation allow to reach a logic that the higher is the ramk the less frequent is the word without any exception 

Then for the jumbled list passed as input a select is perfrom to get all the matching words for each word on the list. This will give a subset small enough to be sent to the driver as a pandas dataframe. A filter is perform based on the modifiedRank column for each jumlbed word   . The results for this could look similar to the below :

********** Printing the results **********

Printing the best matched word for ramoj:
major

Printing the best matched word for camble:
becalm

Printing the best matched word for wraley:
lawyer

Printing the best matched word for reyane:
No match

Printing the best matched word for nagld:
gland
********** End of the results **********
