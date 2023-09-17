import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import gdown

def load_csv_from_google_drive(file_id, csv_file_name):
    """
    Load a CSV file from Google Drive into a DataFrame.

    Parameters:
    file_id (str): The file ID of the CSV file in Google Drive.
    csv_file_name (str): The desired file name for saving the CSV file locally.

    Returns:
    pd.DataFrame: The DataFrame containing the CSV data.
    """
    # Construct the download link
    url = f'https://drive.google.com/uc?id={file_id}'

    # Download the CSV file
    gdown.download(url, csv_file_name, quiet=False)

    # Load CSV into a DataFrame
    df = pd.read_csv(csv_file_name)

    return df

# Example usage
if __name__ == "__main__":
    file_id = 'YOUR_FILE_ID'  # Replace with your file ID
    csv_file_name = 'example.csv'  # Replace with your desired CSV file name

    # Load the CSV file into a DataFrame
    df = load_csv_from_google_drive(file_id, csv_file_name)

    # Display the DataFrame
    print(df.head())



def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L


def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


movies = load_csv_from_google_drive('1PgNO9Wlz6Nwlxf5Rph-in_Q8WNH_L8hF','movies.csv')
credits = load_csv_from_google_drive('1TGNw6x7WCgZSasl4kWTLWw1aG7LAhVQK','crdits.csv')

movies = movies.merge(credits,on='title')

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

movies['cast'] = movies['cast'].apply(convert)

movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

movies['crew'] = movies['crew'].apply(fetch_director)

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies.drop(columns=['overview','genres','keywords','cast','crew'])

new['tags'] = new['tags'].apply(lambda x: " ".join(x))

cv = CountVectorizer(max_features=5000,stop_words='english')

vector = cv.fit_transform(new['tags']).toarray()

similarity = cosine_similarity(vector)

pickle.dump(similarity,open('siml.pkl','wb'))