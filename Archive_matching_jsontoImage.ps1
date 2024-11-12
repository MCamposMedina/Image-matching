###################
## this code was desig to match .json archives to the image files to which the .json correspond
## 
##  The strings below ought to be changed accordingly 
##  
## "Folder where the .json files are" ->
## "Base directory" ->
## "Target directory" ->
## "Folder where the image files are" ->
cd "Base directory"
cd "Folder where the .json files are"


[array] $ListOutput = ls -Filter "*.json*" ## get names of the folders
$string1 = $ListOutput[1].Name


For ($i=0; $i -lt $ListOutput.Length; $i++) {
	$string1 = $ListOutput[$i].Name
	echo $string1
	$string2 = $string1 -replace 'json','.CutHere'
	$string2 = $string2 -replace '(.*).CutHere(.*)','$1' ## The number after the command indicates which part of the senteste is to be kept
	cd "Folder where the image files are"
	
	[array] $ListOutput2 = ls -Filter $string2* ## get names of the folders
	$string3 = $ListOutput2.Length

	##### look for the type of archive
	Get-ChildItem -Filter $string2* -Recurse | Copy-Item -Destination "Target directory"     #### Copying item to said destiation
	
}



Get-Host
Read-Host -Prompt "Press Enter to exit"
