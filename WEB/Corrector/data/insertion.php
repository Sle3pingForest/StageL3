<?php

require_once('../connexion/connexion.php');

class Insertion
{
	private $pdo;
	function __construct()
	{
		$this->pdo = connect_bd();
	}

	//stocke les donnes du fichier de basedecas.csv  dans une array LAMDA	
	function importCaseBase($filename){
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
					    "idProvenance" => $col[6],
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

	//insert les donnees d'array LANDA dans la base de donnees du Corrector
	function insertCaseBase($filename){
		$array = $this->importCaseBase($filename);
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
		$this->pdo->exec('INSERT INTO CASES( idCase, problem, solution, status, error, correction, errorIndex, idProvenance, lang) values '.$valuesInfo );
	}

	//stocke les donnes du fichier de origine.csv dans une array DELTA
	function importOrigine($filename){
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
					    "idOrigin" => $col[0],
					    "originSource" =>	'\''.$col[1].'\'',
					    "note" => '\''.$col[2].'\'',
					);
		        	$array[] = $arrayLine;
		        }
		        $row++;
		    }
		    fclose($handle);
		}
		return $array;
	}

	//insert les donnees d'array LANDA dans la base de donnees du Corrector
	function insertOrigine($filename){
		$array = $this->importOrigine($filename);
		$num = 0;
		$data ="";
		$myliste;
		foreach ( $array as $value){
			$myliste[] = $value;
		}
		while($num < sizeof($myliste)){
			$data .= ',('.$myliste[$num]["idOrigin"].','.
			$myliste[$num]["originSource"].','.
			$myliste[$num]["note"].')';
			$num++;
		}
		$res = str_replace(',(1,', '(1,', $data);
		$values= str_replace('_', '\\\'', $res);
		$values.= ';';
		$this->pdo->exec('INSERT INTO ORIGIN(idOrigin,originSource,note) VALUES '.$values );
	}


	function insertProposition($string , $lang){
		if($lang == 'fr'){
				echo ("<script LANGUAGE='JavaScript'>
    				confirm('Voulez vous inserer votre phrase dans notre data?');
    				</script>");
				$this->pdo->exec('INSERT INTO CASES(problem, solution, status, idProvenance, lang) values '.$string);
		}
		if($lang == 'en'){
			echo ("<script LANGUAGE='JavaScript'>
    				confirm('Do you want to insert your request to us DB');
    				</script>");
				$this->pdo->exec('INSERT INTO CASES(problem, solution, status, idProvenance, lang) values '.$string);
		} 
		echo ("<script LANGUAGE='JavaScript'>
    		window.location.href='../index.php';
    		</script>");

	}
}
$insertion = new Insertion();
//insertion dans la base de donnees la phrase d'utilisateur et la correction d'utilisateur
if(isset($_GET['userProbleme'])){
	$solution= $_GET['userSentence'];
	$problem=$_GET['userProbleme'];
	$lang= $_GET['langSol2'];
	$string = '(\''.$problem.'\',\''.$solution.'\',\''.'en attente'.'\','.'2'.',\''.$lang.'\');';
	$insertion->insertProposition($string, $lang);
}
//insertion dans la base de donnees la phrase d'utilisateur et la solution donnee par le moteur
if(isset($_GET['solution'])){
	$solution= $_GET['solution'];
	$problem=$_GET['initProblem'];
	$lang= $_GET['langSol'];
	$string = '(\''.$problem.'\',\''.$solution.'\',\''.'en attente'.'\','.'2'.',\''.$lang.'\');';
	$insertion->insertProposition($string, $lang);
}
?>
