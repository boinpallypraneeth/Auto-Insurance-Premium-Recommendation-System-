import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale

from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import classification_report, confusion_matrix  

from sklearn import metrics

###############Importing data frame and data cleanising¶###############


df1=pd.read_csv('train_kddcup.csv',header=None)
df2=pd.read_csv('test_kddcup.csv',header=None)
df=pd.concat([df1,df2])
df
df.head()
df.columns = ['duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent','hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root','num_file_creations','num_shells','num_access_files','dummy','num_outbound_cmds','is_host_login','is_guest_login','count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate','dst_host_srv_diff_host_rate','dst_host_serror_rate','dst_host_srv_serror_rate','dst_host_rerror_rate','dst_bushost_srv_rerror_rate']
df.head()
df.shape
df=df.drop(['wrong_fragment','urgent','num_failed_logins','num_file_creations','num_shells','dummy','num_outbound_cmds'],axis=1)
df.shape
df.head()
df.info()
df.describe()
df.columns.values
df.isnull().sum()
df.duplicated(keep='first').sum()
df=df.drop_duplicates()
df.duplicated(keep='first').sum()
corr_map=df.corr()
sns.set_style('darkgrid') 
# sns.set_style help to set color of the axes, whether a grid is enabled by default, and other aesthetic elements.
plt.figure(figsize=(15,15))
sns.heatmap(data=corr_map, annot=True)
df['protocol_type'].value_counts()
df['service'].value_counts()
df['flag'].value_counts()
df['dst_host_rerror_rate'].value_counts()


###########DATA TRASFORMATION ##################

protocol_type = {'tcp' : 0,'udp' : 1,'icmp' : 2}
protocol_type.items()
df.protocol_type = [protocol_type[item] for item in df.protocol_type]
df.head(20)
duration =df['duration']

for i in duration:
    if i <= 2:
        print('good condition', i)
    else:        
        print('bad condition', i)
df['duration'] = np.where((df.duration <= 2), 0, 1)
df.head(20)
replace_map = {'normal' : "normal" , 'DOS' : ['back', 'land', 'pod', 'neptune', 'smurf', 'teardrop'], 'R2L' : ['ftp_write', 'guess_passwd', 'imap', 'multihop', 'spy', 'phf', 'warezclient', 'warezmaster'], 'U2R' : ['buffer_overflow', 'loadmodule', 'perl', 'rootkit'], 'PROBE' : ['ipsweep', 'nmap', 'portsweep', 'satan'], 'extra new attacks' : ['apache2', 'httptunnel', 'mailbomb', 'mscan', 'named', 'processtable', 'ps', 'saint', 'sendmail', 'snmpgetattack', 'snmpguess', 'sqlattack', 'udpstorm', 'worm', 'xlock', 'xsnoop', 'xterm']}
df= df.assign(dst_host_rerror_rate = df['dst_host_rerror_rate'].apply(lambda x: [key for key, value in replace_map.items() if x in value][0]))
df.head(20)
df['dst_host_rerror_rate'].values
dst_host_rerror_rate = {'normal' : 0, 'DOS' : 1, 'R2L' : 2, 'U2R' : 3, 'PROBE' : 4, 'extra new attacks' : 5}
dst_host_rerror_rate.items()
df.dst_host_rerror_rate = [dst_host_rerror_rate[item] for item in df.dst_host_rerror_rate]
df.head(20)
service = {'aol' : 1,'auth' : 2,'bgp' : 3, 'courier' : 4, 'csnet_ns' : 5, 'ctf' : 6, 'daytime' : 7, 'discard' : 8, 'domain' : 9, 'domain_u' : 10, 'echo' : 11, 'eco_i' : 12, 'ecr_i' : 13, 'efs' : 14, 'exec' : 15, 'finger' : 16, 'ftp' : 17, 'ftp_data' : 18, 'gopher' : 19, 'harvest' : 20, 'hostnames' : 21, 'http' : 22, 'http_2784' : 23, 'http_443' : 24, 'http_8001' : 25, 'imap4' : 26, 'IRC' : 27, 'iso_tsap' : 28, 'klogin' : 29, 'kshell' : 30, 'ldap' : 31, 'link' : 32, 'login' : 33, 'mtp' : 34, 'name' : 35, 'netbios_dgm' : 36, 'netbios_ns' : 37, 'netbios_ssn' : 38, 'netstat' : 39, 'nnsp' : 40, 'nntp' : 41, 'ntp_u' : 42, 'other' : 43, 'pm_dump' : 44, 'pop_2' : 45, 'pop_3' : 46, 'printer' : 47, 'private' : 48, 'red_i' : 49, 'remote_job' : 50, 'rje' : 51, 'shell' : 52, 'smtp' : 53, 'sql_net' : 54, 'ssh' : 55, 'sunrpc' : 56, 'supdup' : 57, 'systat' : 58, 'telnet' : 59, 'tftp_u' : 60, 'tim_i' : 61, 'time' : 62, 'urh_i' : 63, 'urp_i' : 64, 'uucp' : 65, 'uucp_path' : 66, 'vmnet' : 67, 'whois' : 68, 'X11' : 69, 'Z39_50' : 70}
service.items()
df.service = [service[item] for item in df.service]
df.head(20)
flag = {'SF' : 0,'S0' : 1,'REJ' : 2,'RSTR' : 3, 'RSTO' : 4, 'S1' : 5, 'SH' : 6, 'S2' : 7, 'RSTOS0' : 8, 'S3' : 9, 'OTH' : 10}
flag.items()
df.flag = [flag[item] for item in df.flag]
df.head(20)
print(df.iloc[2])
# Creating plot
plt.boxplot(df)
X=df.drop(labels=['dst_host_rerror_rate'], axis=1)
y=df['dst_host_rerror_rate'].values
X,y= scale(X),y
X.shape
y
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
results=[]




################# SUPPORT VCTOR MACHINE ###################
svm = SVC(kernel = 'linear', C = 1, gamma = 1)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)
#normal' : 0, 'DOS' : 1, 'R2L' : 2, 'U2R' : 3, 'PROBE' : 4, 'extra new attacks' : 5
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))



############# RANDOM FOREST ################

from sklearn.ensemble import RandomForestClassifier
rclf = RandomForestClassifier(n_estimators=100)  
rclf.fit(X_train, y_train)
y_pred = rclf.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)

########## DECISION TREE CLASSIFIER########
dt = DecisionTreeClassifier()  
dt.fit(X_train, y_train)
y_pred = dt.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)

##########KNEIGHBORSCLASSIFIER ##############
knn = KNeighborsClassifier()  
knn .fit(X_train, y_train)
y_pred = knn.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)



############# Gaussian Naive Bayes classifier################
from sklearn.naive_bayes import GaussianNB
# training the model on training set
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)


############################XGBClassifier ########################


from xgboost import XGBClassifier
xgb = XGBClassifier()
xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)


##############LogisticRegression##############



from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)



#############MLPClassifier#############

from sklearn.neural_network import MLPClassifier
nn = MLPClassifier()
nn.fit(X_train, y_train)
y_pred = nn.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
accuracy=metrics.accuracy_score(y_test, y_pred)
results.append(accuracy)
print("Accuracy:",accuracy)




############# ALGO COMARASSION ################

algorithms =['SVM','RF','DT','KNN','GNB','XGB','LR','Neural Network']
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(algorithms,results, color ='maroon', width = 0.4)
 
plt.xlabel("Algorithms")
plt.ylabel("Accuracy")
plt.show()


############ FEATURES #############

features_list = ['train_duration', 'train_protocol_type', 'train_service',
       'train_flag', 'src_bytes', 'dst_bytes', 'land', 'hot', 'logged_in',
       'num_compromised', 'root_shell', 'su_attempted', 'num_root',
       'num_access_files', 'is_host_login', 'is_guest_login', 'count',
       'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
       'srv_rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
       'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
       'dst_host_srv_count', 'dst_host_same_srv_rate',
       'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
       'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
       'dst_host_srv_serror_rate','dst_bushost_srv_rerror_rate']

features_dict=dict()

i=0
for feature in features_list:
    features_dict.update({'f'+str(i):feature})
    i=i+1
#====================================================================
feature_important = xgb.get_booster().get_score(importance_type='weight')
important_keys = list(feature_important.keys())
keys=[]
values = list(feature_important.values())

for key in important_keys:
    keys.append(features_dict[key])

data = pd.DataFrame(data=values, index=keys, columns=["score"]).sort_values(by = "score", ascending=False)
data.nlargest(35, columns="score").plot(kind='barh', figsize = (20,10)) ## plot top 12 important features





































