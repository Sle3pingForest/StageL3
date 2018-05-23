<script type="text/javascript">
	//this function print the interface with the langage selected
		var langselect = 'fr';
		function refresh(lang){
			var n = lang.toString().localeCompare('fr');
			if(n === 0){
				document.getElementById("erreurSentence").innerHTML= "Entrer la phrase a corriger";
				document.getElementById("correctSentence").innerHTML = "Voici la correction";
				document.getElementById("runButton").innerHTML = "Valider";
				document.getElementsByName('probleme')[0].placeholder='je nage pas';
				document.getElementsByName('solution')[0].placeholder='je ne nage pas';
				langselect = 'fr';
				if(document.getElementById("OK") != null){
					document.getElementById("OK").innerHTML = "Bon";
					document.getElementById("notOK").innerHTML = "Mauvais";
				}
				document.getElementById("userValidated").innerHTML ="Valider";
				document.getElementById("correction").innerHTML ='Correction d\'utilisateur';
				document.getElementsByName('userSentence')[0].placeholder='Entrer votre correction ici';
			}
			else{
				document.getElementById("erreurSentence").innerHTML="Enter the sentence to corrige";
				document.getElementById("correctSentence").innerHTML = "Here the correct sentence";
				document.getElementById("runButton").innerHTML = "Run";
				document.getElementsByName('probleme')[0].placeholder='i cannott swin';
				document.getElementsByName('solution')[0].placeholder='i can\'t swin';
				if(document.getElementById("OK") != null){
					document.getElementById("OK").innerHTML = "Correct";
					document.getElementById("notOK").innerHTML = "Bad";
				}
				langselect ='en';

				document.getElementById("userValidated").innerHTML ="Validate";
				document.getElementById("correction").innerHTML	='User Sentence';
				document.getElementsByName('userSentence')[0].placeholder='Enter your correction here.';
			}
		}


		function selectPhrase(){
			var msg='<?PHP 
			?>';
 			if(document.getElementById("notOK") === null && document.getElementById("OK") === null  && langselect.toString().localeCompare('fr') == 0){
 				$("#reponseButton").append('<button type="button" type="submit" id="OK" onclick="insertPhrase()" class="btn btn-success">Bon</button>');
 				$("#reponseButton").append('<button type="button" type="submit" id="notOK" onclick="userCorrectionForm()" class="btn btn-danger">Inccorect</button>');
 			}
 			if(document.getElementById("notOK") === null && document.getElementById("OK") === null  && langselect.toString().localeCompare('en') == 0){
 				$("#reponseButton").append('<button type="button" type="submit" id="OK" onclick="insertPhrase()" class="btn btn-success">Correct</button>');
 				$("#reponseButton").append('<button type="button" type="submit" id="notOK" onclick="userCorrectionForm()" class="btn btn-danger">Bad</button>');
 			}
		}


		function userCorrectionForm()
		{
			document.getElementById("userCorrection").style.visibility = "visible";
		}

		function insertPhrase(){
			window.location.reload(false);
		}

</script>