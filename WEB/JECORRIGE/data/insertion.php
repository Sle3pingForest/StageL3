<?php

require_once('../connexion/connexion.php');

class Insertion
{
	private $pdo;
	function __construct()
	{
		$this->pdo = connect_bd();
	}

	function importCSV($filename){
		$row = 1;
		$array;
		if (($handle = fopen($filename, "r")) !== FALSE) {
		    while (($data = fgetcsv($handle, 1000, "\n")) !== FALSE) {
		        $num = count($data);
		        for ($c=0; $c < $num; $c++) {
		        	$line  = $data[$c];
					$col1 = explode("\t", $line);				
					$col = str_replace('\'', '_', $col1);
					$arrayLine = array(
					    "problem" => '\''.$col[0].'\'',
					    "solution" =>	'\''.$col[1].'\'',
					    "status" => '\''.$col[2].'\'',
					    "error" => '\''.$col[3].'\'',
					    "correction" => '\''.$col[4].'\'',
					    "errorIndex" => '\''.$col[5].'\'',
					    "idProvenance" => 1,
					    "lang" => '\''.$col[7].'\'',
					);
		        	$array[] = $arrayLine;
		        }
		        $row++;
		    }
		    fclose($handle);
		}
		return $array;
	}

	function insertData($filename){
		$array = $this->importCSV($filename);
		$num = 0;
		$data ="";
		$myliste;
		foreach ( $array as $value){
			$myliste[] = $value;
		}
		while($num < sizeof($myliste)){
			$data .= ',('.$num.','.$myliste[$num]["problem"].','.
			$myliste[$num]["solution"].','.
			$myliste[$num]["status"].','.
			$myliste[$num]["error"].','.
			$myliste[$num]["correction"].','.
			$myliste[$num]["errorIndex"].','.
			$myliste[$num]["idProvenance"].','.
			$myliste[$num]["lang"].')';
			$num++;
		}
		$res = str_replace(',(0,', '(0,', $data);
		$valuesInfo = str_replace('_', '\\\'', $res);
		$valuesInfo .= ';';
		//$this->pdo->exec('INSERT INTO ORIGIN(idOrigin,originSource,note) VALUES(1,"testSource","testNOtes")');
		$this->pdo->exec('INSERT INTO CASES( idCase, problem, solution, status, error, correction, errorIndex, idProvenance, lang) values '.$valuesInfo );		
	}

	function insertProposition($problem,$solution,$lang){
		$string = $problem.','.$solution.','.'en attente'.','.1.','.$lang;
		echo $string;
		//$this->pdo->exec('INSERT INTO CASES(problem, solution, status, idProvenance, lang) values '.$string);
	}
}
?>