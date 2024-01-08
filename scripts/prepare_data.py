import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


path = "data/"
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

labeled = pd.read_csv(os.path.join(path,'labeled.csv'))
labeled = labeled.dropna()
print(labeled.is_affordable.value_counts())


vectorizer = CountVectorizer(binary=True, token_pattern=r'\b[A-Za-z]+\b', min_df = 2)
# model_vectorizer = 'models/trained_MultinomialNB_classifier_vectorizer.joblib'
# joblib.dump(vectorizer, model_vectorizer)


vectors = vectorizer.fit_transform(labeled.content)
words_df = pd.DataFrame(vectors.toarray(), columns=vectorizer.get_feature_names_out())
words_df.shape


X = words_df
y = labeled.is_affordable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


clf = MultinomialNB()
clf.fit(X_train, y_train)

model_filename = 'models/trained_MultinomialNB_classifier_model.joblib'
joblib.dump(clf, model_filename)


y_true = y_test
y_pred = clf.predict(X_test)

matrix = confusion_matrix(y_true, y_pred)

label_names = pd.Series(['not affordable', 'affordable'])
conf_matrix  = pd.DataFrame(matrix,
     columns='Predicted ' + label_names,
     index='Is ' + label_names).div(matrix.sum(axis=1), axis=0)

tn, fn, fp, tp = conf_matrix.loc['Is not affordable':'Is affordable', 'Predicted not affordable':'Predicted affordable'].values.flatten()
fpr = fp / (fp + tn)
tpr = tp / (tp + fn)
accuracy = (tp + tn) / (tp + tn + fp + fn)
print("False Positive Rate (FPR):", fpr)
print("True Positive Rate (TPR):", tpr)
print("Accuracy:", accuracy)


plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='.2f', cmap='Blues', cbar=False)

# Set labels and title
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Multinomial Naive Bayes Classifier \nConfusion Matrix Heatmap')

# Save the figure 
os.makedirs('figures', exist_ok=True)
plt.savefig('figures/confusion_matrix_heatmap.png')
# plt.show()

tn, fn, fp, tp = conf_matrix.loc['Is not affordable':'Is affordable', 'Predicted not affordable':'Predicted affordable'].values.flatten()
fpr = fp / (fp + tn)
tpr = tp / (tp + fn)
accuracy = (tp + tn) / (tp + tn + fp + fn)
print("False Positive Rate (FPR):", fpr)
print("True Positive Rate (TPR):", tpr)
print("Accuracy:", accuracy)


df = pd.read_csv('data/urbanize.csv')

vectors_new_data = vectorizer.transform(df['content'])
words_df_new_data = pd.DataFrame(vectors_new_data.toarray(), columns=vectorizer.get_feature_names_out())

# Make predictions on the new data
y_pred_new_data = clf.predict(words_df_new_data)
df['prediction'] =y_pred_new_data
print(df['prediction'].value_counts())

df.to_csv('data/prediction.csv', index=False)