import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from textstat import flesch_reading_ease, gunning_fog

# Load the dataset
data = pd.read_csv('quiz_questions.csv')

data['id'] = data.index + 1

# Combine description and detailed_solution
data['text'] = data['description'].fillna('') + ' ' + data['detailed_solution'].fillna('')

# Feature engineering
data['word_count'] = data['text'].apply(lambda x: len(x.split()))
data['sentence_count'] = data['text'].apply(lambda x: x.count('.'))
data['flesch_score'] = data['text'].apply(lambda x: flesch_reading_ease(x) if x else 0)
data['fog_index'] = data['text'].apply(lambda x: gunning_fog(x) if x else 0)

# Text vectorization using TF-IDF
vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
text_features = vectorizer.fit_transform(data['text']).toarray()

# Combine all features
features = pd.DataFrame(text_features, columns=vectorizer.get_feature_names_out())
features['word_count'] = data['word_count']
features['sentence_count'] = data['sentence_count']
features['flesch_score'] = data['flesch_score']
features['fog_index'] = data['fog_index']

# Scale the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
data['difficulty_cluster'] = kmeans.fit_predict(scaled_features)

# Evaluate clustering
silhouette_avg = silhouette_score(scaled_features, data['difficulty_cluster'])
print(f'Silhouette Score for clustering: {silhouette_avg:.2f}')

# Map cluster numbers to difficulty labels (assign based on inspection)
difficulty_map = {0: 'easy', 1: 'medium', 2: 'hard'}
data['predicted_difficulty'] = data['difficulty_cluster'].map(difficulty_map)

# Save to CSV
data[['id', 'description', 'detailed_solution', 'predicted_difficulty']].to_csv('categorized_questions.csv', index=False)
