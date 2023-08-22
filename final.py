# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13czStHxya1KTO3-MaTUXm1_hJ3hNPGeK
"""

pip install python-doc
!python3 -m pip install docx2txt
!pip install textract
!sudo apt-get install antiword
!pip install python-docx
!pip install xgboost
!pip install wordcloud
!python -m spacy download en_core_web_sm
!pip install docx2txt

from google.colab import drive
drive.mount('/content/drive/')

import os,re
!pip install docx2txt
import docx2txt
!pip install textract
import textract
import pandas as pd
import numpy as np
!pip install python-docx

from docx import Document
import nltk
nltk.download('punkt')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score,precision_score
from pandas.plotting import scatter_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
nltk.download("stopwords")
import xgboost as xgb

os.listdir('/content/drive/MyDrive/Project_Resume')

os.listdir('/content/drive/MyDrive/Project_Resume/Resumes/Peoplesoft resumes')

os.listdir('/content/drive/MyDrive/Project_Resume/Resumes/SQL Developer Lightning insight')

os.listdir('/content/drive/MyDrive/Project_Resume/Resumes/workday resumes')

file_path = []
category = []


directory = '/content/drive/MyDrive/Project_Resume/Resumes'
for i in os.listdir(directory):
  if i.endswith('.docx') or i.endswith('.doc') or i.endswith('.pdf'):
    os.path.join(directory, i)
    file_path.append((textract.process(os.path.join(directory, i))).decode('utf-8'))
    category.append('React JS Developer')
file_path, category

file_path_1 = []
category_1 = []

directory_1 = '/content/drive/MyDrive/Project_Resume/Resumes/Peoplesoft resumes'
for i in os.listdir(directory_1):
  if i.endswith('.docx') or i.endswith('.doc') or i.endswith('.pdf'):
    os.path.join(directory_1, i)
    file_path_1.append((textract.process(os.path.join(directory_1, i))).decode('utf-8'))
    category_1.append('Peoplesoft resumes')


file_path_1, category_1

file_path_2 = []
category_2= []


directory_2 = '/content/drive/MyDrive/Project_Resume/Resumes/SQL Developer Lightning insight'
for i in os.listdir(directory_2):
  if i.endswith('.docx') or i.endswith('.doc') or i.endswith('.pdf'):
    os.path.join(directory_2, i)
    file_path_2.append((textract.process(os.path.join(directory_2, i))).decode('utf-8'))
    category_2.append('SQL Developer Lightning insight')


file_path_2, category_2


file_path_3 = []
category_3 = []


directory_3 = '/content/drive/MyDrive/Project_Resume/Resumes/workday resumes'
for i in os.listdir(directory_3):
  if i.endswith('.docx') or i.endswith('.doc') or i.endswith('.pdf'):
    os.path.join(directory_3, i)
    file_path_3.append((textract.process(os.path.join(directory_3, i))).decode('utf-8'))
    category_3.append('Workday Resume')


file_path_1, category_1

data = pd.DataFrame(data = file_path , columns = ['resumes'])
data['category'] = category
data

df1 = pd.DataFrame(data = file_path_1 , columns = ['resumes'])
df1['category_1'] = category_1
df1

df2 = pd.DataFrame(data = file_path_2, columns = ['resumes'])
df2['category_2'] = category_2
df2

df3 = pd.DataFrame(data = file_path_3 , columns = ['resumes'])
df3['category_3'] = category_3
df3

# Create a DataFrame
resume_data = data.append([df1, df2, df3], ignore_index = True)
resume_data

""" Merge all Unnecessary column in One Column

"""

resume_data['Category'] = category+category_1+ category_2 + category_3
resume_data

resume_data.drop(['category', 'category_1', 'category_2', 'category_3'], axis = 1, inplace = True)
resume_data

resume_data.head(15)

resume_data.info()

resume_data.to_csv('finalRaw_Resume.csv', index=False)

import pandas as pd
resume_data = pd.read_csv("/content/finalRaw_Resume.csv")
resume_data

df = pd.read_csv('/content/finalRaw_Resume.csv')

# Define a function to extract name using spaCy's named entity recognition (NER)
import re
import pandas as pd
import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern], on_match = None)

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text
df['Name'] = df['resumes'].apply(extract_name)
df['Name']

def education(resumes):
    education_pattern = r'Education:.*?((?:\n.+\n)+)'
    education_match = re.search(education_pattern, resumes, re.IGNORECASE)
    if education_match:
        return education_match.group(1).strip()
    else:
        return '-'

df['Education'] = df['resumes'].apply(education)

df.head()

def experience(resumes):
    experience_pattern = r'\b(?!2012|100)(?:(?:0?\.\d+|\d+\.\d+)|[1-9]\d?(?:\.\d+)?)(?:\s*(?:years?|yrs?)\s*)?(?:\s*\d+(?:\.\d+)?\s*(?:months?|mos?)\s*)?(?:\s*(?:of\s)?experience)?'
    experience = re.search(experience_pattern, resumes, re.IGNORECASE)
    if experience:
        experience_value = re.findall(r'\d+(?:\.\d+)?', experience.group())
        # Exclude numbers greater than 26
        if float(experience_value[0]) <= 26:
            return experience_value[0]
    return ''

df['Experience'] = df['resumes'].apply(experience)
df.head()

def work_experience(resumes):
    experience_pattern = r'(\d+(\.\d+)?\s*(?:years?|yrs?)\s*(?:of\s+experience)?)[\s-]*(.*)'

    match = re.search(experience_pattern, resumes, re.IGNORECASE)

    if match:
        return match.group(3).strip()
    else:
        return 'Not Found'

df['Work Experience'] = df['resumes'].apply(work_experience)
df.head()

def skillset(resumes, category):
    skills = []
    if category == 'SQLDeveloper':
        predefined_skills = ['SQL', 'Database Management', 'Data Analysis', 'Query Optimization', 'ETL', 'Performance Tuning', 'Stored Procedures', 'Data Modeling', 'Indexing', 'Data Warehousing']
    elif category == 'WorkDay':
        predefined_skills = ['Workday', 'HCM', 'Integration', 'Consultant', 'Business Processes', 'Configuration', 'Report Writing', 'Security Administration', 'Absence Management', 'Benefits Administration']
    elif category == 'Peoplesoft':
        predefined_skills = ['Peoplesoft', 'HRMS', 'Payroll Management', 'PeopleTools', 'Application Designer', 'PeopleCode', 'Component Interface', 'SQR', 'Integration Broker', 'Workflow']
    elif category == 'React JS Developer':
        predefined_skills = ['React JS', 'UI Development', 'JavaScript', 'HTML', 'CSS', 'RESTful APIs', 'React Router', 'Redux', 'Webpack', 'Testing (Jest/Enzyme)']
    else:
        predefined_skills = []

    for skill in predefined_skills:
        pattern = r'\b{}\b'.format(re.escape(skill))
        if re.search(pattern, resumes, re.IGNORECASE):
            skills.append(skill)

    return ', '.join(skills[:10])

# Apply the function to the DataFrame based on the Category column
df['Technical Skills'] = df.apply(lambda x: skillset(x['resumes'], x['Category']), axis=1)
df.head()

# Extract location using regular expressions
location_pattern = r'\b(Hyderabad|Pune|Mumbai|Bangalore|delhi|chennai|lucknow|nagpur|indore|Coimbatore|vizag|kolkata|suart|jaipur|ahemdabad|kochi)\b'
df['Location'] = df['resumes'].apply(lambda x: re.findall(location_pattern, str(x), re.IGNORECASE)[0].strip() if re.findall(location_pattern, str(x), re.IGNORECASE) else 'Not Found')
df['Location']

# Extract links from the 'resumes' column
link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
df['Link'] = df['resumes'].apply(lambda x: re.findall(link_pattern, str(x)) if re.findall(link_pattern, str(x)) else 'Not Found')
df['Link']

df.head()

df.to_csv('finalp247 skills.csv', index=False)

df=pd.read_csv("finalp247 skills.csv")
df

df['Category'].unique

df.isnull().sum()

"""Number of Words in each Resume"""

df['Word_Count'] = df['resumes'].apply(lambda x: len(str(x).split(" ")))
df[['resumes','Word_Count']]

"""Number of Characters"""

df['Char_Count'] = df['resumes'].str.len() ## this also includes spaces
df[['resumes','Char_Count']].head(20)

import nltk
nltk.download('stopwords')

"""Number of Stopwords"""

from nltk.corpus import stopwords as nltk_stopwords
stopwords_list = nltk_stopwords.words('english')
df['stopwords'] = df['resumes'].apply(lambda x: len([x for x in x.split() if x in stopwords_list]))
df[['resumes', 'stopwords']]

"""Number of Numerics"""

resume_data['Numerics'] = resume_data['resumes'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))
resume_data[['resumes','Numerics']]

df

"""Text Pre-Processing
Using Regular Expression
"""

def preprocess(sentence):
    sentence = str(sentence)
    sentence = sentence.lower()
    sentence = sentence.replace('{html}',"")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url = re.sub(r'http\S+', '',cleantext)
    rem_num = re.sub('[0-9]+', '', rem_url)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)
    filtered_words = [w for w in tokens if len(w) > 2 if not w in nltk_stopwords.words('english')]

    return " ".join(filtered_words)

from nltk.tokenize import RegexpTokenizer
df = pd.read_csv('/content/finalp247 skills.csv')
df['Resume_Details'] = resume_data.resumes.apply(lambda x: preprocess(x))

df['Resume_Details']

df.drop(['resumes'], axis = 1, inplace = True)
df

df.to_csv('finalCleaned_Resumesnlp.csv', index = False)

df = pd.read_csv('finalCleaned_Resumesnlp.csv')
df

# Plot a pie chart
df['Link'].value_counts().plot(kind='pie', autopct='%1.1f%%')

# Display the chart
plt.axis('equal')
plt.show()

# Plot a pie chart
df['Education'].value_counts().plot(kind='pie', autopct='%1.1f%%')

# Display the chart
plt.axis('equal')
plt.show()

# Plot a pie chart
df['Location'].value_counts().plot(kind='pie', autopct='%1.1f%%')

# Display the chart
plt.axis('equal')
plt.show()

df['Resume_Details'].head()

"""Named Entity Recognition (NER)"""

import string
oneSetOfStopWords = set(nltk_stopwords.words('english')+['``',"''"])
totalWords =[]
Sentences = df['Resume_Details'].values
cleanedSentences = ""
for records in Sentences:
    cleanedText = preprocess(records)
    cleanedSentences += cleanedText
    requiredWords = nltk.word_tokenize(cleanedText)
    for word in requiredWords:
        if word not in oneSetOfStopWords and word not in string.punctuation:
            totalWords.append(word)

wordfreqdist = nltk.FreqDist(totalWords)
mostcommon = wordfreqdist.most_common(50)
print(mostcommon)

"""Parts Of Speech (POS) Tagging"""

!python -m spacy download en_core_web_lg
import spacy
nlp = spacy.load('en_core_web_lg')

one_block = cleanedSentences[1300:5200]
doc_block = nlp(one_block)
spacy.displacy.render(doc_block, style= 'ent', jupyter= True)

for token in doc_block[:30]:
    print(token,token.pos_)

"""Filtering out only the Nouns and Verbs from the Text to Tokens

"""

one_block = cleanedSentences
doc_block = nlp(one_block)
nouns_verbs = [token.text for token in doc_block if token.pos_ in ('NOUN','VERB')]
print(nouns_verbs[:250])

"""Counting all the Nouns and Verbs present in the Tokens of words"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(nouns_verbs)
sum_words = X.sum(axis=0)

words_freq = [(word,sum_words[0,idx]) for word, idx in cv.vocabulary_.items()]
words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)

wd_df = pd.DataFrame(words_freq)
wd_df.columns = ['Words','Count']
wd_df[0:15]

"""Visualizing the Result of Top 30 Nouns and Verbs most Frequently

"""

import seaborn as sns
from matplotlib import pylab
fig, axe = plt.subplots(1,1, figsize=(10,7), dpi=200)
ax = sns.barplot(x= wd_df['Count'].head(30), y= wd_df.Words.head(30), data= wd_df, ax = axe,
            label= 'Total Profile Category : {}'.format(len(resume_data.Category.unique())))

axe.set_xlabel('Frequency', size=16,fontweight= 'bold')
axe.set_ylabel('Words', size=16, fontweight= 'bold')
plt.xticks(rotation = 0)
plt.legend(loc='best', fontsize= 'x-large')
plt.title('Top 30 Most used Nouns and Verbs in Resumes', fontsize= 18, fontweight= 'bold')
rcParams = {'xtick.labelsize':'14','ytick.labelsize':'14','axes.labelsize':'16'}

for i in ax.containers:
    ax.bar_label(i,color = 'black', fontweight = 'bold', fontsize= 12)

pylab.rcParams.update(rcParams)
fig.tight_layout()
plt.show()
fig.savefig('/content/drive/MyDrive/Project_Resume/Resumes/Top_Nouns_Verbs_Bar', dpi = 500)

from wordcloud import WordCloud, STOPWORDS
text = " ".join(cat for cat in wd_df.Words) # Creating the text variable

word_cloud = WordCloud(width=1000, height=800, random_state=10, background_color="black",
                       colormap="Pastel1", collocations=False, stopwords=STOPWORDS).generate(text)

plt.figure(figsize=(10,7), dpi=800) # Display the generated Word Cloud
plt.title('Most used Nouns and Verbs in Resumes', fontsize= 15, fontweight= 'bold')
plt.imshow(word_cloud)
plt.axis("off")
word_cloud.to_file('/content/drive/MyDrive/Project_Resume/Resumes/Word_Clowds_Noun_Verb.png')
plt.show()

df['Category'].value_counts().sort_index().plot(kind='bar', figsize=(8, 4))
plt.title("category Distribution")
plt.show()
df['Education'].value_counts().sort_index().plot(kind='bar', figsize=(8, 4))
plt.title("Education Distribution")
plt.show()
df['Experience'].value_counts().sort_index().plot(kind='bar', figsize=(8, 4))
plt.title("Experience Distribution")
plt.show()
df['Work Experience'].value_counts().sort_index().plot(kind='bar', figsize=(8, 4))
plt.title("Work Experience Distribution")
plt.show()
df['Technical Skills'].value_counts().sort_index().plot(kind='bar', figsize=(8, 4))
plt.title("Technical skills Distribution")
plt.show()
df['Location'].value_counts().sort_index().plot(kind='bar', figsize=(8, 4))
plt.title("Location Distribution")
plt.show()
df['Link'].value_counts().sort_index().plot(kind='bar', figsize=(8, 4))
plt.title("Links Distribution")
plt.show()

def wordcloud(df):
    txt = ' '.join(txt for txt in df['Resume_Details'])
    wordcloud = WordCloud(
        height=2000,
        width=4000,
        colormap=WORDCLOUD_COLOR_MAP
    ).generate(txt)

    return wordcloud

# Commented out IPython magic to ensure Python compatibility.
# for other theme, please run: mpl.pyplot.style.available
PLOT_PALETTE = 'tableau-colorblind10'
# for other color map, please run: mpl.pyplot.colormaps()
WORDCLOUD_COLOR_MAP = 'tab10_r'
plt.style.use(PLOT_PALETTE)
# %matplotlib inline

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Define the desired color map
WORDCLOUD_COLOR_MAP = 'tab10_r'

# Set the desired color map
plt.set_cmap(WORDCLOUD_COLOR_MAP)

# Generate the word cloud
text_data = df['Resume_Details'].astype(str).str.cat(sep=' ')
wordcloud = WordCloud().generate(text_data)

# Plot the word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

categories = np.sort(df['Category'].unique())
categories

df_categories = [df[df['Category'] == category].loc[:, ['Resume_Details', 'Category']] for category in categories]
df_categories

import matplotlib.pyplot as plt
from wordcloud import WordCloud
plt.figure(figsize=(80, 60))

# Define the desired color map
WORDCLOUD_COLOR_MAP = 'tab10_r'

# Set the desired color map
plt.set_cmap(WORDCLOUD_COLOR_MAP)

# Generate word clouds for each category
for i, Category in enumerate(categories):
    wc_category = WordCloud().generate(str(df_categories[i]))

    plt.subplot(5, 5, i + 1).set_title(Category)
    plt.imshow(wc_category, interpolation='bilinear')
    plt.axis('off')

plt.tight_layout()
plt.show()

def wordfreq(df):
    count = df['Resume_Details'].str.split(expand=True).stack().value_counts().reset_index()
    count.columns = ['Word', 'Frequency']
    return count.head(10)

word_frequency = wordfreq(df)
print(word_frequency)

fig = plt.figure(figsize=(80, 60))

for i, Category in enumerate(categories):
    wf = wordfreq(df_categories[i])

    fig.add_subplot(5, 5, i + 1).set_title(category)
    plt.bar(wf['Word'], wf['Frequency'])
    plt.ylim(0, 500)

plt.show()
plt.close()

df=pd.read_csv("/content/finalCleaned_Resumesnlp.csv")
import numpy as np
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
for i in range(0,8):
    df.iloc[:,i]=le.fit_transform(df.iloc[:,i])
print(df)

df

df.value_counts()

import seaborn as sns
sns.pairplot(data = df)

plt.figure(figsize=(10,10))
plt.xticks()
sns.countplot(y="Category", data=df)

import nltk
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

# Create an instance of the WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Define a function to lemmatize words
def lemmatize_words(words):
    lem_words = [lemmatizer.lemmatize(word) for word in words]
    return lem_words

# Apply the lemmatization function to a list of words
words_list = df['Resume_Details']
lemmatized_words = lemmatize_words(words_list)
print(lemmatized_words)

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
requiredText = df['Resume_Details'].values
requiredTarget = df['Category'].values

word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    stop_words='english')
word_vectorizer.fit(requiredText)
WordFeatures = word_vectorizer.transform(requiredText)

print ("Feature completed .....")
WordFeatures

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(WordFeatures, requiredTarget, random_state=30, test_size=0.20, shuffle = True, stratify=requiredTarget)
X_train.shape, X_test.shape

from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.metrics import f1_score,precision_score,confusion_matrix,recall_score,accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

rf_clf = RandomForestClassifier()
rf_clf.fit(X_train, y_train)
prediction_1 = rf_clf.predict(X_test)
print('Accuracy of Decision Tree Classifier on training set: {:.4f}'.format(rf_clf.score(X_train, y_train)))
print('Accuracy of Decision Tree Classifier on test set    : {:.4f}'.format(rf_clf.score(X_test, y_test)))
from sklearn.metrics import f1_score,precision_score,confusion_matrix,recall_score,accuracy_score
from sklearn import metrics
print("\n Classification report for Decision Tree Classifier %s:\n%s\n" % (rf_clf, metrics.classification_report(y_test, prediction_1)))
accuracy_1 = round(accuracy_score(y_test,prediction_1),4)
precision_1 = round(precision_score(y_test,prediction_1,average = 'macro'),4)
recall_1 = round(recall_score(y_test,prediction_1, average = 'macro'),4)
f1_1 = round(f1_score(y_test,prediction_1, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_1)
print('Precision Score  : ', precision_1)
print('Recall Score     : ', recall_1)
print('f1-Score         : ', f1_1)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_1))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_1 )
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

sv_clf = SVC()
sv_clf.fit(X_train, y_train)
prediction_2 = sv_clf.predict(X_test)
print('Accuracy of Support Vector Classifier on training set: {:.4f}'.format(sv_clf.score(X_train, y_train)))
print('Accuracy of Support Vector Classifier on test set    : {:.4f}'.format(sv_clf.score(X_test, y_test)))
print("\n Classification report for Support vector Classifier %s:\n%s\n" % (sv_clf, metrics.classification_report(y_test, prediction_2)))
accuracy_2 = round(accuracy_score(y_test,prediction_2),4)
precision_2 = round(precision_score(y_test,prediction_2,average = 'macro'),4)
recall_2 = round(recall_score(y_test,prediction_2, average = 'macro'),4)
f1_2 = round(f1_score(y_test,prediction_2, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_2)
print('Precision Score  : ', precision_2)
print('Recall Score     : ', recall_2)
print('f1-Score         : ', f1_2)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_2))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_2)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

nb_clf = MultinomialNB()
nb_clf.fit(X_train, y_train)
prediction_3 = nb_clf.predict(X_test)
print('Accuracy of Multinomial NB Classifier on training set: {:.4f}'.format(nb_clf.score(X_train, y_train)))
print('Accuracy of Multinomial NB Classifier on test set    : {:.4f}'.format(nb_clf.score(X_test, y_test)))
print("\n Classification report for multinomialNB Classifier %s:\n%s\n" % (nb_clf, metrics.classification_report(y_test, prediction_3)))
accuracy_3= round(accuracy_score(y_test,prediction_3),4)
precision_3 = round(precision_score(y_test,prediction_3,average = 'macro'),4)
recall_3 = round(recall_score(y_test,prediction_3, average = 'macro'),4)
f1_3 = round(f1_score(y_test,prediction_3, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_3)
print('Precision Score  : ', precision_3)
print('Recall Score     : ', recall_3)
print('f1-Score         : ', f1_3)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_3))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_3)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

logistic_clf = LogisticRegression()
logistic_clf.fit(X_train, y_train)
prediction_4 = logistic_clf.predict(X_test)
print('Accuracy of Logistic Regression Classifier on training set: {:.4f}'.format(logistic_clf.score(X_train, y_train)))
print('Accuracy of Logistic Regression Classifier on test set    : {:.4f}'.format(logistic_clf.score(X_test, y_test)))
print("\n Classification report for Logistic Classifier %s:\n%s\n" % (logistic_clf, metrics.classification_report(y_test, prediction_4)))
accuracy_4= round(accuracy_score(y_test,prediction_4),4)
precision_4 = round(precision_score(y_test,prediction_4,average = 'macro'),4)
recall_4 = round(recall_score(y_test,prediction_4, average = 'macro'),4)
f1_4 = round(f1_score(y_test,prediction_4, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_4)
print('Precision Score  : ', precision_4)
print('Recall Score     : ', recall_4)
print('f1-Score         : ', f1_4)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_4))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_4)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier
ab_clf = AdaBoostClassifier()
ab_clf.fit(X_train, y_train)
prediction_5 = ab_clf.predict(X_test)
print('Accuracy of AdaBoost Classifier on training set: {:.4f}'.format(ab_clf.score(X_train, y_train)))
print('Accuracy of AdaBoost Classifier on test set    : {:.4f}'.format(ab_clf.score(X_test, y_test)))

print("\n Classification report for AdaBoost Classifier %s:\n%s\n" % (ab_clf, metrics.classification_report(y_test, prediction_5)))
accuracy_5= round(accuracy_score(y_test,prediction_5),4)
precision_5 = round(precision_score(y_test,prediction_5,average = 'macro'),4)
recall_5= round(recall_score(y_test,prediction_5, average = 'macro'),4)
f1_5 = round(f1_score(y_test,prediction_5, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_5)
print('Precision Score  : ', precision_5)
print('Recall Score     : ', recall_5)
print('f1-Score         : ', f1_5)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_5))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_5)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

gb_clf = GradientBoostingClassifier()
gb_clf.fit(X_train, y_train)
prediction_6 = gb_clf.predict(X_test)
print('Accuracy of GradientBoosting Classifier on training set: {:.4f}'.format(gb_clf.score(X_train, y_train)))
print('Accuracy of GradientBoosting Classifier on test set    : {:.4f}'.format(gb_clf.score(X_test, y_test)))

print("\n Classification report for GradientBoosting Classifier %s:\n%s\n" % (gb_clf, metrics.classification_report(y_test, prediction_6)))
accuracy_6= round(accuracy_score(y_test,prediction_6),4)
precision_6 = round(precision_score(y_test,prediction_6,average = 'macro'),4)
recall_6= round(recall_score(y_test,prediction_6, average = 'macro'),4)
f1_6 = round(f1_score(y_test,prediction_6, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_6)
print('Precision Score  : ', precision_6)
print('Recall Score     : ', recall_6)
print('f1-Score         : ', f1_6)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_6))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_6)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

from lightgbm import LGBMClassifier
lgb_clf = LGBMClassifier()
lgb_clf.fit(X_train, y_train)
prediction_7 = lgb_clf.predict(X_test)
print('Accuracy of LightGradientBoosting Classifier on training set: {:.4f}'.format(lgb_clf.score(X_train, y_train)))
print('Accuracy of LightGradientBoosting Classifier on test set    : {:.4f}'.format(lgb_clf.score(X_test, y_test)))
print("\n Classification report for GradientBoosting Classifier %s:\n%s\n" % (lgb_clf, metrics.classification_report(y_test, prediction_7)))
accuracy_7= round(accuracy_score(y_test,prediction_7),4)
precision_7 = round(precision_score(y_test,prediction_7,average = 'macro'),4)
recall_7= round(recall_score(y_test,prediction_7, average = 'macro'),4)
f1_7 = round(f1_score(y_test,prediction_7, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_7)
print('Precision Score  : ', precision_7)
print('Recall Score     : ', recall_7)
print('f1-Score         : ', f1_7)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_7))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_7)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
cart = DecisionTreeClassifier()
bg_clf = BaggingClassifier(base_estimator=cart,n_estimators=10,random_state=8)
bg_clf.fit(X_train , y_train)
#Predict for X test dataset
prediction_8 = bg_clf.predict(X_test)
print('Accuracy of Bagging Classifier Classifier on training set: {:.4f}'.format(bg_clf.score(X_train, y_train)))
print('Accuracy of Bagging Classifier Classifier on test set    : {:.4f}'.format(bg_clf.score(X_test, y_test)))
print("\n Classification report for Bagging Classifier %s:\n%s\n" % (bg_clf, metrics.classification_report(y_test, prediction_8)))
accuracy_8= round(accuracy_score(y_test,prediction_8),4)
precision_8 = round(precision_score(y_test,prediction_8,average = 'macro'),4)
recall_8= round(recall_score(y_test,prediction_8, average = 'macro'),4)
f1_8 = round(f1_score(y_test,prediction_8, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_8)
print('Precision Score  : ', precision_8)
print('Recall Score     : ', recall_8)
print('f1-Score         : ', f1_8)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_8))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_8)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

#KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.neighbors  import KNeighborsClassifier
kfold = KFold(n_splits=10)
knn_clf= KNeighborsClassifier(n_neighbors = 5 , metric = "minkowski" , p = 2)
results = cross_val_score(knn_clf, X_train, y_train, cv=kfold)
print(results.mean())
knn_clf.fit(X_train , y_train)
prediction_9=knn_clf.predict(X_test)
print('Accuracy of knn Classifier Classifier on training set: {:.4f}'.format(knn_clf.score(X_train, y_train)))
print('Accuracy of knn Classifier Classifier on test set    : {:.4f}'.format(knn_clf.score(X_test, y_test)))
print("\n Classification report for knn Classifier %s:\n%s\n" % (knn_clf, metrics.classification_report(y_test, prediction_9)))
accuracy_9= round(accuracy_score(y_test,prediction_9),4)
precision_9 = round(precision_score(y_test,prediction_9,average = 'macro'),4)
recall_9= round(recall_score(y_test,prediction_9, average = 'macro'),4)
f1_9= round(f1_score(y_test,prediction_9, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_9)
print('Precision Score  : ', precision_9)
print('Recall Score     : ', recall_9)
print('f1-Score         : ', f1_9)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_9))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_9)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

pip install xgboost

from xgboost import XGBClassifier
xgb_clf = XGBClassifier()
xgb_clf.fit(X_train, y_train)
prediction_10 = xgb_clf.predict(X_test)
print('Accuracy of extreme GradientBoosting Classifier on training set: {:.4f}'.format(xgb_clf.score(X_train, y_train)))
print('Accuracy of extreme GradientBoosting Classifier on test set    : {:.4f}'.format(xgb_clf.score(X_test, y_test)))
print("\n Classification report for extremeGradientBoosting Classifier %s:\n%s\n" % (xgb_clf, metrics.classification_report(y_test, prediction_10)))
accuracy_10= round(accuracy_score(y_test,prediction_10),4)
precision_10= round(precision_score(y_test,prediction_10,average = 'macro'),4)
recall_10= round(recall_score(y_test,prediction_10, average = 'macro'),4)
f1_10 = round(f1_score(y_test,prediction_10, average = 'macro'),4)
print('Accuracy Score   : ', accuracy_10)
print('Precision Score  : ', precision_10)
print('Recall Score     : ', recall_10)
print('f1-Score         : ', f1_10)
print('Confusion Matrix :\n',confusion_matrix(y_test,prediction_10))
from  sklearn.metrics import confusion_matrix , accuracy_score
cm_log = confusion_matrix(y_test ,prediction_10)
import seaborn as sn
plt.figure(figsize = (10,7))
sn.heatmap(cm_log, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

table = {'Classifier' : ['Random Forest Classifier', 'SVM Classifier', 'Multinomial NB Classifier', 'Logistic Regression', 'AdaBoost Classifier', 'Gradient Boosting Classifier', 'Xtreme Gradient Boosting Classifier', 'Light Gradient Boosting Classifier','Bagging Classifier','knn Classifier'], 'Accuracy Score' : [accuracy_1, accuracy_2, accuracy_3, accuracy_4, accuracy_5, accuracy_6, accuracy_7, accuracy_8,accuracy_9,accuracy_10], 'Precision Score' : [precision_1, precision_2, precision_3, precision_4, precision_5, precision_6, precision_7, precision_8,precision_9,precision_10], 'Recall Score' : [recall_1, recall_2, recall_3, recall_4, recall_5, recall_6, recall_7, recall_8,recall_9,recall_10], 'f1-Score' : [f1_1, f1_2, f1_3, f1_4, f1_5, f1_6, f1_7, f1_8,f1_9,f1_10]}
table = pd.DataFrame(table)
table

