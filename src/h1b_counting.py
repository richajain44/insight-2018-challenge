"""
This program takes in input file h1b_ipnput.csv and outputs top_10_occupation.txt and top_10_state.txt.
It calculates for each certified applicant, the top 10 occupation for which H1B is certified and 
top 10 state for where the workers work

run.sh provides the necessary input and output paths
"""
#Importing necessary libraries
#sys is used for input and output reading

import sys
import os

#Function to count the top 10 occupations
#Input: input file i.e. h1b_input.csv, status='certified',job_title
#Returns : One list of top 10 occupations

def count_occupations(filepath,status_no,job_title):
	occupation={}
	with open(filepath,'r',encoding='utf8') as fp:
		next(fp)
		for i in fp:
			i=i.split(';')
			i[job_title]=i[job_title].replace("'",'')
			i[job_title]=i[job_title].replace('"','')
			if i[status_no]=='CERTIFIED':
				if i[job_title] not in occupation:
					occupation.update({i[job_title]:1})
				else:
					occupation[i[job_title]]=occupation[i[job_title]]+1

	return sorted(occupation.items(), key = lambda x: (-x[1],x[0]))

#Function to count the top 10 states
#Input: input file i.e. h1b_input.csv, status='certified',state
#Returns : One list of top 10 states	
def count_state(filepath,status_no,state):
	state_count={}
	with open(filepath,'r',encoding='utf8') as fp:
		next(fp)
		for i in fp:
			i=i.split(';')
			if i[status_no]=='CERTIFIED':
				if i[state] not in state_count:
					state_count.update({i[state]:1})
				else:
					state_count[i[state]]=state_count[i[state]]+1
					
	return sorted(state_count.items(), key = lambda x: (-x[1],x[0]))
	
#main function 	
if __name__ == '__main__':
	input_file = sys.argv[1]
	output_occupation=sys.argv[2]
	output_state = sys.argv[3]
	status_no=0
	job_title=0
	state=0
	#reading the input file
	with open(input_file,'r',encoding='utf8') as fp:
		i = fp.readline()
		i = i.split(';')
		for k,j in enumerate(i):
			if ('LCA_CASE_WORKLOC1_STATE' in j) or ('WORKSITE_STATE' in j):
				state=k
			if ('STATUS' in j) or ('CASE_STATUS' in j):
				status_no = k
			if ('LCA_CASE_SOC_NAME' in j) or ('SOC_NAME' in j):
				job_title=k

	result_occupation = count_occupations(input_file,status_no,job_title)#call to count the occupations
	result_state=count_state(input_file,status_no,state)#call to count the states
	
	#writing the header to output file
	with open(output_occupation,'a') as f:
		f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
		f.write('\n')
	#writing the header to output file
	with open(output_state,'a') as f:
		f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
		f.write('\n')
	
	#writing the top 10 occupations to output file
	l_occupation=0
	for i in result_occupation:
		l_occupation=l_occupation+i[1]
	for i in result_occupation[0:10]:
		#print(i[0]+';'+str(i[1])+';'+str(round((i[1]/l_occupation)*100,2))+'%')
		with open(output_occupation,'a') as f:
			f.write(i[0]+';'+str(i[1])+';'+str(round((i[1]/l_occupation)*100,1))+'%')
			f.write('\n')
	
	#writing the top 10 states to output file
	l_state=0
	for i in result_state:
		l_state=l_state+i[1]
	for i in result_state[0:9]:
		#print(i[0]+';'+str(i[1])+';'+str(round((i[1]/l_state)*100,1))+'%')
		with open(output_state,'a') as f:
			f.write(i[0]+';'+str(i[1])+';'+str(round((i[1]/l_state)*100,1))+'%')
			f.write('\n')