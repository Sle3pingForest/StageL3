<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<title> linguistiCASE </title>
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


		function valideData(){
			echo "<h2 style='text-align:center'>";
			echo "Valider les cas d'utilisateur ";
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
								echo "";
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
									echo "<button type='button' type='submit' class='btn btn-info text-white''>OK</button>";
								echo "</td>";
						
							$num++;
							echo "</tr>";
					}
					echo "</table>";
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
	echo "Restaurer la base de données ";
	echo "<button type='button' type='submit' class='btn btn-danger text-white' onclick='insertData()'>Reset</button>";
	echo "<script language=\"javascript\">";
		echo "function insertData(){";
			$insert = new Insertion();
			$insert->insertData('../data/base_de_cas_minimal.csv');
			echo "alert('Insertion Fait')";
		echo "}";
	echo "</script>";
	echo "</h2>";
	$admin = new ADMIN();
	$admin->valideData();
	
	
?>
</body>
</html>