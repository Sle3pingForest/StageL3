For using this project you will need to install fast_distance module in the directory module.

The goal of this project is to correct sentence thanks to case base reasoning.
In this debut we only works with character without any linguistic analysis.


For testing you need to enter these following instruction:

	cat test_rememoration.txt | python moteur.py base_de_cas.txt -s 1 -t 2

	or

	printf "J'aime pas nager." | python moteur.py base_de_cas.txt -s 1 -t 2

	or 

	python moteur.py



If you want to test this with database you need to use Test.py and configure test_sql.py:


	python Test.py base_de_cas.txt -s 1 -t 2 -se "J'aime pas nager."
