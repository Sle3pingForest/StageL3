<?php 

echo "hello";
$command = escapeshellcmd('php -v');
$output = shell_exec($command);
echo $output;

echo "out";
?>