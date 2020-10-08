# CSC533 Homework Readme

This readme file provides details on how to install the necessary dependencies to run the the scripts that generate the outputs for question 2, 3 and 4 of HW3. 

## Installation

Ensure that python3 is used as the programming language to execute these scripts. 
Clone the repository or place all the contents of the program submission into a directory. 

Use the python3 package manager in order to install the dependencies for these scripts.
```bash
sudo pip3 install -r requirements.txt
```

## Usage
Follow these instructions in order to run each of the scripts for the assignment. 

### Q2
The script is hardcoded to use the files www.cnn.com.har and www.macys.com.har. 
Run the following command in order to execute the script.

```python
python3 mmanika_HW3_Q2.py
```
A plot will be automatically generated, and the necessary tables containing the domain names that are third party for each of the two sites, and the common domains are printed out in the CLI. 

### Q3
The script is hardcoded to use the files www.cnn.com.har and www.macys.com.har. In addition, the file easylist.txt that is provided in this directory is used to initialize the adblocker functions rules. 
The first level domain that is used for the cnn site is cnn.com. The first level domain name that is used for www.macys.com is macys.com. 
Run the following command in order to execute the script.

```python
python3 mmanika_HW3_Q3.py
```
The script will run by printing out that each URL is being processed. At the end of execution, a table that is formatted to the requirements of the question is printed on the CLI. 

### Q4
The script is hardcoded to use the file Tor_query_EXPORT-1.csv for its processing. 
The script makes use of md5 hashing in order to uniquely identify the tor routers based on the combination of router name, bandwidth, ip and the hostname. 
Run the following command in order to execute the script. 

```python
python3 mmanika_HW3_Q4.py
```
A plot will be automatically generated that displays a Venn diagram for the distribution of the different types of relays that constitute the Tor network. 
The CLI will display information regarding the top 5 countries that are hosting Tor relays, the bandwidth contribution of the top 5 relays and the cumulative bandwidth distribution table of the groups that constitute the Venn diagram. 

## Author
```text
Mukul Manikandan
mmanika@ncsu.edu
```



