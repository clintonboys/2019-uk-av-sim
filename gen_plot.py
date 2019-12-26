import matplotlib.pyplot as plt
import pandas as pd 

# df = pd.read_csv('~/Desktop/england_and_wales.csv')
# fig, ax = plt.subplots()
# ax.scatter(df['ld_to_lab'], df['brx_to_lab'], c=df['con_seats'], marker='s', s=650, cmap='RdBu', label='Conservative seats')
# #plt.colorbar(label='Conservative seats in England and Wales (actual: 359/573)')
# plt.xlabel('Percentage of Liberal Democrat preferences flowing to Labour')
# plt.ylabel('Percentage of Brexit Party preferences flowing to Labour')
# plt.title('UK 2019 election under AV: England and Wales\n 326 needed for a majority', fontsize=14)
# for i, txt in enumerate(df['con_seats']):
#     ax.annotate(txt, (df['ld_to_lab'].iloc[i], df['brx_to_lab'].iloc[i]), xytext=(int(df['ld_to_lab'].iloc[i])-3,int(df['brx_to_lab'].iloc[i])))
# plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25))
# plt.tight_layout()
# plt.show()
# plt.clf()

df = pd.read_csv('~/Desktop/ni.csv')
fig, ax = plt.subplots()
ax.scatter(df['sf_to_sdlp'], df['apni_to_sdlp'], c=df['dup_seats'], marker='s', s=650, cmap='PRGn', label='DUP Seats')
#plt.colorbar(label='DUP seats in Northern Ireland (actual: 8/18)')
plt.xlabel('Percentage of Sinn Fein preferences flowing to SDLP')
plt.ylabel('Percentage of APNI preferences flowing to SDLP')
plt.title('UK 2019 election under AV: Northern Ireland', fontsize=14)
for i, txt in enumerate(df['dup_seats']):
    ax.annotate(txt, (df['sf_to_sdlp'].iloc[i], df['apni_to_sdlp'].iloc[i]), xytext=(int(df['sf_to_sdlp'].iloc[i])-3,int(df['apni_to_sdlp'].iloc[i])))
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25))
plt.tight_layout()    
plt.show()
plt.clf()

# df = pd.read_csv('~/Desktop/scotland.csv')
# fig, ax = plt.subplots()
# ax.scatter(df['ld_to_snp'], df['lab_to_snp'], c=df['con_seats'], marker='s', s=650, cmap='YlGnBu', label='Conservative seats')
# #plt.colorbar(label='DUP seats in Northern Ireland (actual: 8/18)')
# plt.xlabel('Percentage of Liberal Democrat preferences flowing to SNP')
# plt.ylabel('Percentage of Labour preferences flowing to SNP')
# plt.title('UK 2019 election under AV: Scotland', fontsize=14)
# for i, txt in enumerate(df['con_seats']):
#     ax.annotate(txt, (df['ld_to_snp'].iloc[i], df['lab_to_snp'].iloc[i]), xytext=(int(df['ld_to_snp'].iloc[i])-3,int(df['lab_to_snp'].iloc[i])))
# plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25))
# plt.tight_layout()    
# plt.show()
# plt.clf()