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
<body class="p-3 mb-2 bg-info text-white">	
	<a href="#" data-toggle="modal" data-target="#login-modal">Login</a>
		<div class="modal fade" id="login-modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="display: none;">
    	  	<div class="modal-dialog loginmodal-container">
				<h1>Login to Your Account</h1><br>
				<form method="POST" action="models/AdminSection.php">
					<input type="text" id='user' name="user" placeholder="Username">
					<input type="password" id='pass' name="pass" placeholder="Password">
					<input type="submit" id='login' name="login" class="login loginmodal-submit" value="Login">
				</form>
			</div>
		 </div>
	<h1 style="text-align:center;">
		Bienvenue ! - Welcome !
	</h1>		
	<br>
	<h3 id = "lang" style="text-align:center;">
		<label class="radio-inline">
			<input class ="invisible" type="radio"  id="fr" onclick = "refresh('fr')"  checked="checked" name="optradio">
			<img height="32" width="60" src="img/fr.png">
		</label>
		<label class="radio-inline">
			<input class ="invisible" type="radio"  id="en" onclick = "refresh('en')" name="optradio">
			<img height="30" width="60" src="img/RU.jpeg">
		</label>
	</h3>
	<br>

	<form class="row">
		<div class="col-sm-8">
			<div class="input-group">
				<span  class="input-group-addon" id="erreurSentence">Entrez la phrase à corriger</span>
				<input  id="probleme" type="text" class="form-control" name="probleme" placeholder="Je nage pas.">
			</div>
		</div>
		<div class ="col-sm-4">	
			<button type="button" style ="width: 100px" id="runButton" class="btn p-3 mb-2 bg-primary text-white" >Vérifier</button>
		</div>	
	</form>
	<br>
	<form class="row" method ="GET" action="data/insertion.php">
		<div class="col-sm-8" id ="solutionDiv">
			<div class="input-group">
				<span  class="input-group-addon" id ="correctSentence">Voici la correction</span>
				<input  id="solution" type="text" class="form-control" name="solution" placeholder="Je ne nage pas.">
			</div>
		</div>
		<div class ="col-sm-4" id ="reponseButton">	
		</div>
		<input class="invisible" id="initProblem" type="text" class="form-control" name="initProblem">
			<input class="invisible" id="langSol" type="text" class="form-control" name="langSol">
	</form>

	<form method ="GET"  action="data/insertion.php" class="row invisible" id ="userCorrection" style=float:none; >
		<div class="col-sm-8">
			<div class="input-group" >
				<span  class="input-group-addon" id ="correction">Entrez votre correction</span>
				<input  id="usersolution" type="text" class="form-control" name="userSentence" placeholder="Entrer votre correction ici">
			</div>
		</div>
		<div class ="col-sm-4" id ="okUser">	
				<button  type="submit" id="userValidated" style="width: 100px" class="btn p-3 mb-2 bg-primary text-white" >OK</button>
		</div>
		<div class="col-sm-0" >
			<input class="invisible" id="userProbleme" type="text" class="form-control" name="userProbleme">
			<input class="invisible" id="langSol2" type="text" class="form-control" name="langSol2">
		</div>
	</form>

</body>
<footer class="page-footer font-small blue navbar" >
    <div class="container-fluid text-center text-md-left" style="margin-bottom: 5% ";>
        <div class="row">
            <div class="col-md-12">
                <h5 class="text-uppercase">linguistiCASE</h5>
                <p id="linguistiCASEInfo">linguistiCASE est une site permet de corriger les phrases a partir de RAPC (raisonnement a partir de case)</p>
            </div>
        </div>
    </div>
    <div class="footer-copyright text-center row" style="margin-bottom: auto ;">
        <div class="col-md-4">
         	<img class="col-md-4" height="32" width="60" src="img/logoCorrector.png">
     	</div>
        <p class="glyphicon glyphicon-copyright-mark col-md-4">2018Copyright: </p>
        <a class="glyphicon glyphicon-envelope col-md-4">cont@ct </a>
    </div>
</footer>
</html>



<script type="text/javascript">

	//this function print the interface with the langage selected
	var langselect = 'fr';
	function refresh(lang){
		var n = lang.toString().localeCompare('fr');
		if(n === 0){
			document.getElementById("erreurSentence").innerHTML= "Entrer la phrase a corriger";
			document.getElementById("correctSentence").innerHTML = "Voici la correction";
			document.getElementById("runButton").innerHTML = "Vérifier";
			document.getElementsByName('probleme')[0].placeholder='je nage pas';
			document.getElementsByName('solution')[0].placeholder='je ne nage pas';
			document.getElementById('linguistiCASEInfo').innerHTML='linguistiCASE est une site permet de corriger les phrases erreurs a partir de RAPC (raisonnement a partir de case)';
			langselect = 'fr';
			if(document.getElementById("OK") != null){
				document.getElementById("OK").innerHTML = "Correct";
				document.getElementById("notOK").innerHTML = "Incorrect";
			}
			document.getElementById("userValidated").innerHTML ="OK";
			document.getElementById("correction").innerHTML ='Correction d\'utilisateur';
			document.getElementsByName('userSentence')[0].placeholder='Entrer votre correction ici';
		}
		else{
			document.getElementById("erreurSentence").innerHTML="Enter the sentence to corrige";
			document.getElementById("correctSentence").innerHTML = "Here the correct sentence";
			document.getElementById("runButton").innerHTML = "Verify";
			document.getElementsByName('probleme')[0].placeholder='i cannott swin';
			document.getElementsByName('solution')[0].placeholder='i can\'t swin';
			document.getElementById('linguistiCASEInfo').innerHTML='linguistiCASE is a website that corrects bad sentences ';
			
			if(document.getElementById("OK") != null){
				document.getElementById("OK").innerHTML = "Correct";
				document.getElementById("notOK").innerHTML = "Incorrect";
			}
			langselect ='en';

			document.getElementById("userValidated").innerHTML ="OK";
			document.getElementById("correction").innerHTML	='User Sentence';
			document.getElementsByName('userSentence')[0].placeholder='Enter your correction here.';
		}
	}

	  $(function() {
        $('#runButton').click(function() {			
        	if(document.getElementById("notOK") === null && document.getElementById("OK") === null  && langselect.toString().localeCompare('fr') == 0){
				$("#reponseButton").append('<button  style="margin-right:5px; width: 100px" type="submit" id="OK"  class="btn btn-success">Correct</button>');
				$("#reponseButton").append('<button type="button" style="margin-right:5px; width: 100px" type="submit" id="notOK" onclick="userCorrectionForm()" class="btn btn-danger">Incorrect</button>');
				langselect ='fr';
			}
			if(document.getElementById("notOK") === null && document.getElementById("OK") === null  && langselect.toString().localeCompare('en') == 0){
				$("#reponseButton").append('<button style="margin-right:5px; width: 100px" type="submit" id="OK" class="btn btn-success">Correct</button>');
				$("#reponseButton").append('<button type="button" style="margin-right:5px; width: 100px" type="submit" id="notOK" onclick="userCorrectionForm()" class="btn btn-danger">Incorrect</button>');
				langselect ='en';
			}
			//envoyer le probleme de la form 1 au initProbleme de la form2
			document.getElementById("initProblem").value= document.getElementById("probleme").value;
			document.getElementById("langSol").value= langselect;

	 		$.get('models/moteur.php?probleme=test', function(data) {
	            document.getElementById("solution").value= data;
	          });

        });   

      });

	function userCorrectionForm()
	{
		document.getElementById("OK").disabled = true;
		document.getElementById("userCorrection").style.visibility = "visible";

		//envoyer le probleme de la form 1 au initProbleme de la form 3
		document.getElementById("userProbleme").value= document.getElementById("probleme").value;
		document.getElementById("langSol2").value= langselect;
	}

</script>
