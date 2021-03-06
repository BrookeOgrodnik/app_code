# this is an app whose purpose is to reccomend a show based on some input by
# the user.


import streamlit as st
import pandas as pd
import numpy as np

dataset=pd.read_csv('for_app_hardcode.csv')

@st.cache
def bestLocation(loc):
	listof=np.unique(-np.sort(-dataset[loc].values)[0:5])
	return list(dataset.loc[(dataset[loc].values>=min(listof)) & (dataset[loc].values<=max( listof))].index)[0:5]


def bestKeyword(keys):
	counter=0
	epi=[]
	while counter<len(dataset) and len(epi)<5:
		text_search=dataset.iloc[counter].summary.lower().find(keys)
		if text_search>-1:
			epi.append(counter)
		counter=counter+1
	return list(dataset.iloc[epi].index)

def bestCharacter(cha):
        listof=np.unique(-np.sort(-dataset[cha].values)[0:5])
        return list(dataset.loc[(dataset[cha].values>=min(listof)) & (dataset[cha].values<=max( listof))].index)[0:5]


#the min number for all the pre inputed side characters is 5 so we are good here
def bestSide(side):
	return list(dataset.loc[dataset[side]==1].index)[0:5]



st.title('The One with the Recommendations')

st.write('Tell us about what you are looking for in an episode and we will reccomend the 5 highest rated episodes that match your preferences.')

ready=True

st.header('Choose a character')
loc_win, char_win, side_win,key_win=['']*4
#start with none of them chosen
rachel, monica, phoebe, ross, joey, chandler, pref_char =[0]*7

if st.checkbox('Rachel'):
	rachel=1
	char_win='rachel'

if st.checkbox('Monica'):
	monica=1
	char_win='monica'

if st.checkbox('Ross'):
	ross=1
	char_win='ross'

if st.checkbox('Joey'):
	joey=1
	char_win='joey'

if st.checkbox('Chandler'):
	chandler=1
	char_win='chandler'

if st.checkbox('Phoebe'):
	phoebe=1
	char_win='phoebe'

if st.checkbox('No preference for main character') :
	pref_char=1
	char_win=''

if phoebe+rachel+monica+chandler+ross+pref_char+joey!=1:
	st.warning('Please choose exactly 1')
	ready=False

st.header('Choose a side character')
gunther, janice, richard, heckles, carol, frank, estelle, ursula, pref_side=[0]*9

if st.checkbox('Gunther'):
	gunther=1
	side_win='gunther'

if st.checkbox('Janice'):
	janice=1
	side_win='janice'

if st.checkbox('Richard'):
	richard=1
	side_win='richard'

if st.checkbox('Mr Heckles'):
	heckles=1
	side_win='heckles'

if st.checkbox('Carol'):
	carol=1
	side_win='carol'

if st.checkbox('Frank'):
	frank=1
	side_win='frank'

if st.checkbox('Estelle'):
	estelle=1
	side_win='estelle'

if st.checkbox('Ursula'):
	ursula=1
	side_win='ursula'

if st.checkbox('No preference for side character'):
	pref_side=1
	side_win=''

if gunther+janice+richard+heckles+carol+frank+estelle+ursula+pref_side!=1:
	st.warning('Please choose exactly 1')
	ready=False

st.header('Choose a location')
central_perk, monicas, joeys, rosses, pref_loc=[0]*5

if st.checkbox('Central Perk'):
	central_perk=1
	loc_win='central'

if st.checkbox('Monica\'s Apartment'):
	monicas=1
	loc_win='monica_loc'

if st.checkbox('Joey\'s Apartment'):
	joeys=1
	loc_win='joey_loc'

if st.checkbox('Ross\' Apartment'):
	rosses=1
	loc_win='ross_loc'

if st.checkbox('No preference for location'):
	pref_loc=1
	loc_win=''

if central_perk+monicas+joeys+rosses+pref_loc!=1:
	st.warning('Please choose exactly 1')
	ready=False

#if the keyword is not blank, take the first word and lowercase it, that is the keyword
st.header('Keyword')
keyword= st.text_input('search for')
if len(keyword)>0:
	key_win=keyword.split(' ')[0].replace(",",'').lower()

spoil=st.checkbox('No spoilers! Hide the summaries of the recommendations.')

submit=st.button('Recommend')


if submit and ready:
	#do things
	setwinners=[] 
	others=[]
	if loc_win!='':
		df=bestLocation(loc_win)
		others=others+df[0:len(df)]
	if char_win!='':
		df=bestCharacter(char_win)
		others=others+df[0:len(df)]
	if side_win!='':
		df=bestSide(side_win)
		others=others+df[0:len(df)]	
	if key_win!='':	
		df=bestKeyword(key_win)
		others=others+df[0:len(df)]

	#silly goose didn't choose anything so we are just going to give you the best matches 
	if key_win=='' and side_win=='' and char_win=='' and loc_win=='':
		st.write("No preference? Well, here are the overall best rated episodes")
		st.write(dataset[['season','episode','title']][0:5])
		if not spoil:
			for i in range(5):
				st.write(dataset.iloc[i].title+': '+dataset.iloc[i].summary)
		
	else:
		final_index=[]
		for i in others:
			if [i,0] not in final_index:
				final_index.append([i,0])
		#find the multiplicities
		for i in range(len(final_index)):
			final_index[i]=[final_index[i][0],-others.count(final_index[i][0])]
		
		#need it to be decreasing not increases
		setwinners=[t[0] for t in sorted(final_index, key=lambda x:x[1])]
		
		#add on some just really good episodes if their match didnt return enough
		counts=0
		final_index=[]
		while len(setwinners)+len(final_index)<5:
			if counts not in setwinners:
				final_index.append(counts)
			counts=counts+1
		
		setwinners=setwinners[0:min(len(setwinners),5)]
		
		st.write(dataset.iloc[setwinners][['season','episode','title']])

		if len(final_index)>0:
			st.write('It looks like we didn\'t find enough matches to what you were looking for so please also enjoy these really good episodes')
			st.write(dataset.iloc[final_index][['season', 'episode', 'title']])
		final_index=setwinners+final_index
		if not spoil:
			for i in final_index:
				st.write(dataset.iloc[i].title+': '+ dataset.iloc[i].summary)
			




elif submit and not ready:
	st.error('Please fix the warnings and then resubmit')

