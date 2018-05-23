<?php

require_once('../connexion/connexion.php');

echo $_GET['userSentence'];
echo $_GET['userProbleme'];
echo "<script language=\"javascript\">";
echo "alert('bonjour')";
echo "</script>";

header("Location: ../index.php");

?>
