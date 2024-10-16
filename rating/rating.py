import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob

# Load the data
file_path = r'c:\code\rating\score.xlsx'  # Use raw string to avoid issues with backslashes
df = pd.read_excel(file_path)

# Step 1: Data Cleaning
# Removing rows with missing values in 'Ответ' or 'Вопрос' columns
df_cleaned = df.dropna(subset=['Ответ', 'Вопрос'])

print(f"Initial data shape: {df.shape}")
print(f"Cleaned data shape: {df_cleaned.shape}")

# Step 2: Sentiment Analysis
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Положительный'
    elif analysis.sentiment.polarity < 0:
        return 'Отрицательный'
    else:
        return 'Нейтральный'

# Apply sentiment analysis
df_cleaned['Sentiment'] = df_cleaned['Ответ'].apply(get_sentiment)

# Step 3: Define Top PLUs
top_positive_plu = (
    df_cleaned[df_cleaned['Sentiment'] == 'Положительный']
    .groupby('PLU')['Вопрос']
    .count()
    .nlargest(20)
    .reset_index(name='Количество положительных отзывов')
)

top_negative_plu = (
    df_cleaned[df_cleaned['Sentiment'] == 'Отрицательный']
    .groupby('PLU')['Вопрос']
    .count()
    .nlargest(20)
    .reset_index(name='Количество отрицательных отзывов')
)

# Step 4: Summarizing Feedback
def summarize_feedback(responses):
    russian_stop_words = [
        'и', 'в', 'во', 'не', 'что', 'всё', 'как', 'он', 'она', 'то', 
        'на', 'этот', 'за', 'с', 'к', 'по', 'из', 'кто', 'так', 'но', 
        'да', 'если' 'какая' 'оно' 'мне' 'это' 'было' 'была'
     ]
    vectorizer = CountVectorizer(stop_words=russian_stop_words)
    X = vectorizer.fit_transform(responses)
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = X.sum(axis=0).A1.argsort()[::-1]
    
    # Getting the top 5 words for summary
    top_words = feature_array[tfidf_sorting][:5]
    return ', '.join(top_words)

# Gathering responses for summarization
def get_responses(plu):
    return df_cleaned[df_cleaned['PLU'] == plu]['Ответ'].tolist()

# Applying summarization to the top PLUs
top_positive_plu['Обобщенная информация'] = top_positive_plu['PLU'].apply(lambda x: summarize_feedback(get_responses(x)))
top_negative_plu['Обобщенная информация'] = top_negative_plu['PLU'].apply(lambda x: summarize_feedback(get_responses(x)))

# Step 5: Prepare Excel with two sheets
output_file_path = 'PLU_analysis.xlsx'  # Specify output file path
with pd.ExcelWriter(output_file_path) as writer:
    top_positive_plu.to_excel(writer, sheet_name='Top Positive PLUs', index=False)
    top_negative_plu.to_excel(writer, sheet_name='Top Negative PLUs', index=False)

print("Excel file created successfully with top PLUs and their summaries.")
