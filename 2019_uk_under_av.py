import requests
import operator
import pandas as pd
from bs4 import BeautifulSoup
from RunoffElection import Runoff

url = 'https://en.wikipedia.org/wiki/Results_of_the_2019_United_Kingdom_general_election'
req = requests.get(url)

soup = BeautifulSoup(req.content, 'html.parser')
tables = soup.find_all('table', class_='sortable')

# ENGLAND
for table in tables:
    ths = table.find_all('th')
    headings = [th.text.strip() for th in ths]
    if headings[:3] == ['Constituency', 'County', 'Region']:
        break

eng_cols = ['constituency', 'county', 'region', 'A', 'result_2017', 'B', 'result_2019', 'winner_votes_2019', 'winner_share_2019', 'winner_maj_2019', 
							    'turnout_2019', 'con_2019', 'lab_2019', 'ld_2019', 'grn_2019', 'brx_2019', 'other_2019', 'total_2019']
england = pd.DataFrame(columns=eng_cols)
england['pc_2019'] = 0
# Extract the columns we want and write to a semicolon-delimited text file.
for tr in table.find_all('tr'):
    tds = tr.find_all('td')
    if not tds:
        continue
    try:
    	england = england.append(pd.DataFrame([[td.text.strip().replace(',','') for td in tds[:18]]], columns=eng_cols), ignore_index=True)
    except:
    	break

wales = pd.read_csv('wales.csv', thousands=r',', sep=',')
wales['county'] = ''
wales['region'] = ''
wales['A'] = ''
wales['B'] = ''
wales['winner_maj_2019'] = wales['majority_2019']

england = pd.concat([england, wales],ignore_index=True)
england.sample(5).to_csv('sample.csv')
print (england['winner_maj_2019'] > 50.0).sum()
con_seats_df = pd.DataFrame(columns=['ld_to_lab', 'brx_to_lab', 'con_seats'])    	
lds_to_lab = []
brxs_to_lab = []
con_seats = []
for ld_to_lab in range(0, 100, 10):
	for brx_to_lab in range(0, 100, 10):
		lds_to_lab.append(ld_to_lab)
		brxs_to_lab.append(brx_to_lab)
		pref_flows = {'CON': {            'LAB': 10, 'LD': 20, 'BRX': 70, 'GRN': 0, 'PC': 0},
					  'LAB': {'CON': 10,             'LD': 50, 'BRX': 10, 'GRN': 30, 'PC': 0},
					  'LD':  {'CON': 100-ld_to_lab,  'LAB': ld_to_lab,           'BRX': 0,  'GRN': 0, 'PC': 0},
					  'BRX': {'CON': 100-brx_to_lab,  'LAB': brx_to_lab,  'LD': 0,            'GRN': 0, 'PC': 0},
					  'GRN': {'CON': 10,  'LAB': 20, 'LD': 65, 'BRX': 5, 'PC': 0},
					  'OTH': {'CON': 50,  'LAB': 50, 'LD': 0,  'BRX': 0,  'GRN': 0, 'PC': 0},
					  'PC': {'CON':0, 'LAB': 80, 'LD': 20, 'BRX': 0, 'GRN': 0}}
					  
		england = england.replace(r'^\s*$', 0, regex=True)
		england['result_2019_runoff'] = ''
		england = england.fillna(0)

		for i in range(0, len(england)):
			candidate_dict = {'CON': int(england['con_2019'].iloc[i]),
							  'LAB': int(england['lab_2019'].iloc[i]),
							  'LD': int(england['ld_2019'].iloc[i]),
							  'GRN': int(england['grn_2019'].iloc[i]),
							  'BRX': int(england['brx_2019'].iloc[i]),
							  'PC': int(england['pc_2019'].iloc[i]),
							  'OTH': int(england['other_2019'].iloc[i])}
		# england['constituency'].iloc[i],
			england['result_2019_runoff'].iloc[i] = max(Runoff(candidate_dict, pref_flows).iteritems(), key=operator.itemgetter(1))[0]

		results_2017 = england[['constituency', 'result_2017']].groupby('result_2017').agg('count')
		results_2019 = england[['constituency', 'result_2019']].groupby('result_2019').agg('count')
		print(results_2019)
		results_2019_runoff = england[['constituency', 'result_2019_runoff']].groupby('result_2019_runoff').agg('count').reset_index()
		con = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'CON']['constituency'].iloc[0]
		con_seats.append(con)
		print 'ld_to_lab {}, brx_to_lab {}, con_seats {}'.format(ld_to_lab, brx_to_lab, con)

con_seats_df['ld_to_lab'] = lds_to_lab
con_seats_df['brx_to_lab'] = brxs_to_lab
con_seats_df['con_seats'] = con_seats

print con_seats_df
con_seats_df.to_csv('/Users/clinton/Desktop/england_and_wales.csv')

# NI
ni = pd.read_csv('ni.csv', thousands=r',', sep=',')
print ni.columns

ni = ni.replace(r'^\s*$', 0, regex=True)
ni = ni.replace(',','')
ni = ni.fillna(0)			  
ni['result_2019_runoff'] = ''

dup_seats_df = pd.DataFrame(columns=['sf_to_sdlp', 'apni_to_sdlp', 'dup_seats', 'sf_seats', 'sdlp_seats', 'apni_seats'])    	
sfs_to_sdlp = []
apnis_to_sdlp = []
dup_seats = []
sf_seats = []
apni_seats = []
sdlp_seats = []
for sf_to_sdlp in range(0, 100, 10):
	for apni_to_sdlp in range(0, 100, 10):
		sfs_to_sdlp.append(sf_to_sdlp)
		apnis_to_sdlp.append(apni_to_sdlp)
		ni_pref_flows = {'DUP':  {            'SF': 16, 'APNI': 16, 'SDLP': 16, 'UUP': 17,  'CON': 17,  'GRN': 17},
					     'SF':   {'DUP': 100-sf_to_sdlp, 'APNI': 0, 'SDLP': sf_to_sdlp, 'UUP': 0,  'CON': 0,  'GRN': 0},
					     'APNI': {'DUP': 100-apni_to_sdlp, 'SF': 0, 'SDLP': apni_to_sdlp, 'UUP': 0,  'CON': 0,  'GRN': 0},
					     'SDLP': {'DUP': 16,  'SF': 16, 'APNI': 16,   		'UUP': 0,  'CON': 17,  'GRN': 17},
					     'UUP':  {'DUP': 16,  'SF': 16, 'APNI': 16, 'SDLP': 17, 		   'CON': 17,  'GRN': 17},
					     'CON':  {'DUP': 16,  'SF': 16, 'APNI': 16, 'SDLP': 17, 'UUP': 17,  		  'GRN': 17},
					     'GRN':  {'DUP': 16,  'SF': 16, 'APNI': 16, 'SDLP': 17, 'UUP': 17,  'CON': 17},
					     'OTH':  {'DUP': 16,  'SF': 16, 'APNI': 16, 'SDLP': 17, 'UUP': 17,  'CON': 17,  'GRN': 17}}

		for i in range(len(ni)):
			candidate_dict = {'DUP': int(ni['dup_2019'].iloc[i]),
							  'SF': int(ni['sf_2019'].iloc[i]),
							  'APNI': int(ni['apni_2019'].iloc[i]),
							  'SDLP': int(ni['sdlp_2019'].iloc[i]),
							  'UUP': int(ni['uup_2019'].iloc[i]),
							  'CON': int(ni['con_2019'].iloc[i]),
							  'GRN': int(ni['grn_2019'].iloc[i]),
							  'OTH': int(ni['other_2019'].iloc[i])}
			ni['result_2019_runoff'].iloc[i] = max(Runoff(candidate_dict, ni_pref_flows).iteritems(), key=operator.itemgetter(1))[0]

		results_2017 = ni[['constituency', 'result_2017']].groupby('result_2017').agg('count')
		results_2019 = ni[['constituency', 'result_2019']].groupby('result_2019').agg('count')
		print(results_2019)
		results_2019_runoff = ni[['constituency', 'result_2019_runoff']].groupby('result_2019_runoff').agg('count').reset_index()
		dup = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'DUP']['constituency'].iloc[0]
		sdlp = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'SDLP']['constituency'].iloc[0]
		sf = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'SF']['constituency'].iloc[0]
		apni = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'APNI']['constituency'].iloc[0]
		dup_seats.append(dup)
		sdlp_seats.append(sdlp)
		sf_seats.append(sf)
		apni_seats.append(apni)
		print 'sf_to_sdlp {}, apni_to_sdlp {}, dup_seats {}'.format(sf_to_sdlp, apni_to_sdlp, dup)

dup_seats_df['sf_to_sdlp'] = sfs_to_sdlp
dup_seats_df['apni_to_sdlp'] = apnis_to_sdlp
dup_seats_df['dup_seats'] = dup_seats
dup_seats_df['apni_seats'] = apni_seats
dup_seats_df['sf_seats'] = sf_seats
dup_seats_df['sdlp_seats'] = sdlp_seats

print dup_seats_df
dup_seats_df.to_csv('/Users/clinton/Desktop/ni.csv')


# SCOTLAND
scotland = pd.read_csv('scot.csv', thousands=r',', sep=',')
print scotland.columns

scotland = scotland.replace(r'^\s*$', 0, regex=True)
scotland = scotland.replace(',','')
scotland = scotland.fillna(0)			  
scotland['result_2019_runoff'] = ''

con_seats_df = pd.DataFrame(columns=['ld_to_snp', 'lab_to_snp', 'con_seats', 'lab_seats', 'snp_seats', 'ld_seats'])    	
lds_to_snp = []
labs_to_snp = []
con_seats = []
lab_seats = []
snp_seats = []
ld_seats = []
for ld_to_snp in range(0, 100, 10):
	for lab_to_snp in range(0, 100, 10):
		lds_to_snp.append(ld_to_snp)
		labs_to_snp.append(lab_to_snp)
		scotland_pref_flows = {'SNP': {'SNP': 0, 'CON': 20, 'LAB': 20, 'LD': 20, 'GRN': 20, 'BRX': 20},
					           'CON': {'SNP': 20, 'CON': 0, 'LAB': 20, 'LD': 20, 'GRN': 20, 'BRX': 20},
					           'LAB': {'SNP': lab_to_snp, 'CON': 100-lab_to_snp, 'LAB': 0, 'LD': 0, 'GRN': 0, 'BRX': 0},
					           'LD':  {'SNP': ld_to_snp, 'CON': 100-ld_to_snp, 'LAB': 0, 'LD': 0, 'GRN': 0, 'BRX': 0},
					           'GRN': {'SNP': 20, 'CON': 20, 'LAB': 20, 'LD': 20, 'GRN': 0, 'BRX': 20},
					           'BRX': {'SNP': 20, 'CON': 20, 'LAB': 20, 'LD': 20, 'GRN': 20, 'BRX': 0},
					           'OTH': {'SNP': 16, 'CON': 16, 'LAB': 16, 'LD': 17, 'GRN': 17, 'BRX': 17}}

		for i in range(len(scotland)):
			candidate_dict = {'SNP': int(scotland['snp_2019'].iloc[i]),
							  'CON': int(scotland['con_2019'].iloc[i]),
							  'LAB': int(scotland['lab_2019'].iloc[i]),
							  'LD':  int(scotland['ld_2019'].iloc[i]),
							  'GRN': int(scotland['grn_2019'].iloc[i]),
							  'BRX': int(scotland['brx_2019'].iloc[i]),
							  'OTH': int(scotland['other_2019'].iloc[i])}
			scotland['result_2019_runoff'].iloc[i] = max(Runoff(candidate_dict, scotland_pref_flows).iteritems(), key=operator.itemgetter(1))[0]

		results_2017 = scotland[['constituency', 'result_2017']].groupby('result_2017').agg('count')
		results_2019 = scotland[['constituency', 'result_2019']].groupby('result_2019').agg('count')
		print(results_2019)
		results_2019_runoff = scotland[['constituency', 'result_2019_runoff']].groupby('result_2019_runoff').agg('count').reset_index()
		snp = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'SNP']['constituency'].iloc[0]
		con = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'CON']['constituency'].iloc[0]
		lab = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'LAB']['constituency'].iloc[0]
		ld = results_2019_runoff[results_2019_runoff['result_2019_runoff'] == 'LD']['constituency'].iloc[0]
		snp_seats.append(snp)
		con_seats.append(con)
		lab_seats.append(lab)
		ld_seats.append(ld)
		print 'ld_to_snp {}, lab_to_snp {}, con_seats {}'.format(ld_to_snp, lab_to_snp, con)

con_seats_df['ld_to_snp'] = lds_to_snp
con_seats_df['lab_to_snp'] = labs_to_snp
con_seats_df['con_seats'] = con_seats
con_seats_df['snp_seats'] = snp_seats
con_seats_df['lab_seats'] = lab_seats
con_seats_df['ld_seats'] = ld_seats

print con_seats_df
con_seats_df.to_csv('/Users/clinton/Desktop/scotland.csv')
