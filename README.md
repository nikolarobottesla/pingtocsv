# pingtocsv
ping to csv

## features
* runs ping once then waits 5 seconds
* captures the date time for each ping
* saves the output to a .csv file

## arguments
* input arg for ip ```--ip```
* input arg for wait time in seconds ```--wait```
* input arg for csv file name ```-n```
* example: ```pingtocsv.exe --ip 192.168.1.1 --wait 10 -n "ping results"```  

## windows executable
download exe from releases and double click

## build
* clone
* pip install .[test]
* `pyinstaller --onefile pingtocsv/pingtocsv.py` 

## to do
* multi-platform builds