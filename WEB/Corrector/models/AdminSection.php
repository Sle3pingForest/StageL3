<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<title> CORRECTOR </title>
  	<meta name="viewport" content="width=device-width, initial-scale=1">
  	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.css">
	<link rel="stylesheet" href="bootstrap/css/localCss.css" />
  	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.js"></script>
  	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.js"></script>
</head>

<body>
<h1 style="text-align:center;">
	Bonjour  
	<?php 
		echo $_POST['user'];
	?>
</h1>
<?php
require_once('../connexion/connexion.php');
include ('../data/insertion.php');

	
	class ADMIN
	{
		private $pdo;
		function __construct()
		{
			$this->pdo = connect_bd();
		}
		
		function infoAdmins($idAdmin)
		{
			$myliste = Array();
			$sql="select * from ADMINS where idAdmin = ".$idAdmin;
			foreach ($this->pdo->query($sql) as $row)
			{
				$myliste[] = $row;
			}
			return $myliste;
		}

		function selectEnAttente()
		{
			$myliste = Array();
			$sql="select * from CASES where status = 'en attente'";
			foreach ($this->pdo->query($sql) as $row)
			{
				$myliste[] = $row;
			}
			return $myliste;
		}


		// cette fonction permet de valider les case bon pour les admin , le changement de statut en attent en tru est en cours de developpement
		function valideData(){
			echo "<h2 style='text-align:center'>";
			echo "Valider les cas d'utilisateurs ";
			echo "<button type='button' type='submit' class='btn btn-info text-white' onclick='afficherCase()'>Afficher</button>";
			echo "</h2>";
			$num = 0;
			$liste = $this->selectEnAttente();
			echo "<div id='userProposition' class='row invisible'>";
				echo"<div class='col-sm-12'>";
					echo "<table align='center' class='table table-bordered'>";
						echo "<thead>";
						echo "<tr style='text-align:center'>";
							echo "<th>";
								echo "Probleme";
							echo "</th>";
							echo "<th>";
								echo "Solution";
							echo "</th>";
							echo "<th>";
								echo "Langue";
							echo "</th>";
							echo "<th>";
								echo "Correct?";
							echo "</th>";

						echo "</tr>";
						echo "</thead>";
						while($num < sizeof($liste)){
							echo "<tr style='text-align:center'>";
								echo "<td>";
									echo $liste[$num]["problem"];
								echo "</td>";
								echo "<td>";
									echo $liste[$num]["solution"];
								echo "</td>";
								echo "<td>";
									echo $liste[$num]["lang"];
								echo "</td>";
								echo "<td>";
								echo "<input id='checkBox' type='checkbox'>";
								echo "</td>";
							$num++;
							echo "</tr>";
					}
				echo "</table>";
				echo "<button style='float:right' type='button' type='submit' class='btn btn-info text-white''>Valider</button>";
				echo "</div>";	
			echo "</div>";
			echo "<script language=\"javascript\">";
				echo "function afficherCase(){";
					echo "document.getElementById('userProposition').style.visibility = 'visible';";
				echo "}";
			echo "</script>";

		}
	}

	echo "<h2 style='text-align:center'>";
	echo "Insertion base de cas initiale ";
	echo "<button type='button' type='submit' class='btn btn-danger text-white' onclick='insertMin()'>Insérer</button>";
	echo "<script language=\"javascript\">";
		echo "function insertMin(){";
			$insert = new Insertion();
			$insert->insertOrigine('../data/origine.csv');
			$insert->insertCaseBase('../data/base_de_cas_minimal.csv');
			echo "alert('Insertion Fait')";
		echo "}";
	echo "</script>";
	echo "</h2>";

	echo "<h2 style='text-align:center'>";
	echo "Insertion base de cas de WiCoPaCo ";
	echo "<button type='button' type='submit' class='btn btn-danger text-white' onclick='insertwiko()'>Insérer</button>";
	echo "<script language=\"javascript\">";
		echo "function insertMwiko(){";
			$insert = new Insertion();
			$insert->insertOrigine('../data/origine.csv');
			//$insert->insertCaseBase('../data/base_de_cas_WiKoPaCo.csv');
			echo "alert('Insertion Fait')";
		echo "}";
	echo "</script>";
	echo "</h2>";

	$admin = new ADMIN();
	$admin->valideData();
	
	
?>
</body>
</html>