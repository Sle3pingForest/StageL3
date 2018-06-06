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
<body class="p-3 mb-2 bg-info text-white">	
	<div class ="row">

		<!-- logo  du site -->
		<div class="col-md-4 ">
	        <img class="col-md-4" height="32" width="60" style="margin: 5% 0;" src="img/logoCorrector.png">
	    </div>
	    <div class= "col-md-8" style="text-align:right;">
			<a href="#" data-toggle="modal" data-target="#login-modal">Login</a>
		</div>

		<!-- partie pop up pour login administrateur -->
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
	</div>		 
	<h1 style="text-align:center;">
		Bienvenue ! - Welcome!
	</h1>		
	<br>

	<!-- partie traitement de la langue -->
	<h3 id = "lang" style="text-align:center;">
		<label class="radio-inline">
			<input  type="radio"  id="fr" onclick = "refresh('fr')"  checked="checked" name="optradio">FR

		</label>
		<label class="radio-inline">
			<input  type="radio"  id="en" onclick = "refresh('en')" name="optradio">EN
		</label>
	</h3>
	<br>

	<!-- cette FORM est pour la partir entrer la phrase a corriger -->
	<form>
		<div class="row"> 
			<div class ="col-sm-2" style ="padding-right: 0px">	
				<span  class="form-control input-group-addon" id="erreurSentence" >Entrez la phrase à corriger</span>
			</div>	
			<div class="col-sm-6" style ="padding-left: 0px" >
				<input  id="probleme" type="text" class="form-control" name="probleme" placeholder="Je nage pas." onkeypress="refuserToucheEntree(event);">
			</div>
			<div class ="col-sm-4">	
				<button type="button" style ="width: 100px" id="runButton" class="btn p-3 mb-2 bg-primary text-white" >Corriger</button>
			</div>	
		</div>
	</form>
	<br>


	<!-- cette FORM est la partir d'affichage le solution retourner par le moteur -->
	<form  method ="GET" action="data/insertion.php">
		<div class="row">
			<div class="col-sm-2" style ="padding-right: 0px" id ="solutionDiv">
				<span  class="form-control input-group-addon" id ="correctSentence">Voici la correction</span>
			</div>
			<div class="col-sm-6" style ="padding-left: 0px">
				<input  id="solution" type="text" class="form-control" name="solution" placeholder="Je ne nage pas." onkeypress="refuserToucheEntree(event);">
			</div>
			<div class ="col-sm-4" id ="reponseButton">	
			</div>
			<input class="invisible" id="initProblem" type="text" class="form-control" name="initProblem">
				<input class="invisible" id="langSol" type="text" class="form-control" name="langSol">
		</div>
	</form>


	<!-- cette FORM est la partir pour rentrer la correction utilisateur -->
	<form method ="GET"  action="data/insertion.php" class="invisible" id ="userCorrection";>
		<div class="row">
			<div class="col-sm-2" style ="padding-right: 0px">
				<span  class="form-control input-group-addon" id ="correction">Entrez votre correction</span>
			</div>
			<div class="col-sm-6 " style ="padding-left: 0px">
				<input  id="usersolution" type="text" class="form-control" name="userSentence" placeholder="Entrer votre correction ici" onkeypress="refuserToucheEntree(event);">
			</div>
			<div class ="col-sm-4" id ="okUser">	
				<button  type="submit" id="userValidated" style="width: 100px" class="btn p-3 mb-2 bg-primary text-white" >OK</button>
			</div>
			<div class="col-sm-0" >
				<input class="invisible" id="userProbleme" type="text" class="form-control" name="userProbleme">
				<input class="invisible" id="langSol2" type="text" class="form-control" name="langSol2">
			</div>
		</div>
	</form>

</body>

<!-- footer de la page ou il presente les infos du site .... -->
<footer class="page-footer" >
    <div class="container-fluid text-center" style="margin-bottom: 5% ";>
           <p id="Corrector">
           		Corrector est une site permet de corriger les phrases à partir de RAPC (raisonnement a partir de case)
           </p>
    </div>
    <div class="footer-copyright text-center row" style="margin-bottom: auto;">
        <p class="glyphicon glyphicon-copyright-mark col-md-4">2018Copyright </p>
        <a class="glyphicon glyphicon-envelope col-md-4">cont@ct </a>
    </div>
</footer>
</html>



<script type="text/javascript">

	var langselect = 'fr';

	/*	fonction refresh actualise dynamiquement la langue du site en fonction du buton radio dans la partie traitement de la langue
	*/
	function refresh(lang){
		var n = lang.toString().localeCompare('fr');
		//francaise
		if(n === 0){
			document.getElementById("erreurSentence").innerHTML= "Entrer la phrase a corriger";
			document.getElementById("correctSentence").innerHTML = "Voici la correction";
			document.getElementById("runButton").innerHTML = "Corriger";
			document.getElementsByName('probleme')[0].placeholder='je nage pas';
			document.getElementsByName('solution')[0].placeholder='je ne nage pas';
			document.getElementById('Corrector').innerHTML='Corrector est une site permet de corriger les phrases à partir de RAPC (raisonnement a partir de case)';
			langselect = 'fr';
			if(document.getElementById("OK") != null){
				document.getElementById("OK").innerHTML = "Correct";
				document.getElementById("notOK").innerHTML = "Incorrect";
			}
			document.getElementById("userValidated").innerHTML ="OK";
			document.getElementById("correction").innerHTML ='Correction d\'utilisateur';
			document.getElementsByName('userSentence')[0].placeholder='Entrer votre correction ici';
		}
		//anglais
		else{
			document.getElementById("erreurSentence").innerHTML="Enter the sentence to corrige";
			document.getElementById("correctSentence").innerHTML = "Here the correct sentence";
			document.getElementById("runButton").innerHTML = "Revise";
			document.getElementsByName('probleme')[0].placeholder='i cannott swin';
			document.getElementsByName('solution')[0].placeholder='i can\'t swin';
			document.getElementById('Corrector').innerHTML='Corrector is a website that corrects bad sentences ';
			
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

	/*
	cette partie est du ajax pour recuper la valeur de retour par le moteur du fichier moteur.php  
	et l'afficher dans la zone de text de la partie le solution retourner par le moteur
	*/
	$(function() {
		$('#runButton').click(function() {			
			//cette function affiche deux boutons CORRECT ET INCORRECT si on click sur la corriger
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
			
			//ces 2 lignes sert a passer les values dans la zone de text de la form probleme d'utilisateur
			document.getElementById("initProblem").value= document.getElementById("probleme").value;
			document.getElementById("langSol").value= langselect;

			//ajax pour recuper la solution retourne par moteur.php
 			$.get('models/moteur.php?probleme='+document.getElementById("probleme").value, function(data) {
				document.getElementById("solution").value= data;
			});

    	});   

	});

	//cette fonction sert a desactiver le bouton CORRECT et afficher la formualire de correction d'utilisateur
	function userCorrectionForm()
	{
		document.getElementById("OK").disabled = true;
		document.getElementById("userCorrection").style.visibility = "visible";

		//envoyer le probleme de la form 1 au initProbleme de la form 3
		document.getElementById("userProbleme").value= document.getElementById("probleme").value;
		document.getElementById("langSol2").value= langselect;
	}

	//function pour desactive le enter dans les champ input des formulaire.
	function refuserToucheEntree(event)
	{
		// Compatibilité IE / Firefox
		if(!event && window.event) {
			event = window.event;
		}
		// IE
		if(event.keyCode == 13) {
			event.returnValue = false;
			event.cancelBubble = true;
		}
		// DOM
		if(event.which == 13) {
			event.preventDefault();
			event.stopPropagation();
		}
	}

</script>

