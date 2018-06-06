<?php 
$probleme = $_GET['probleme'];
$output = exec('python ../test/Test.py ../test/base_de_cas.txt -s 1 -t 2 -se "'. $probleme . '"');
echo $output;
?>		