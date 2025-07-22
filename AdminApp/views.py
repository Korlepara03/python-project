from django.shortcuts import render
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from AdminApp.Database import DBConnection
# Create your views here.
def index(request):
    return render(request,'AdminApp/index.html')
def loginaction(request):
    uname=request.POST['username']
    passw=request.POST['password']
    if uname == 'Admin' and passw == 'Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'msg':'Admin Login Failed..!!'}
        return render(request,'AdminApp/index.html')

def AdminHome(request):
    return render(request,'AdminApp/AdminHome.html')


    global df_books,df_ratings
def UploadDataset(request):
    global df_books,df_ratings

    df_books = pd.read_csv("dataset/Books.csv",
                           usecols=['ISBN', 'Book_Title', 'Book_Author'],
                           dtype={'ISBN': 'str', 'Book_Title': 'str', 'Book_Author': 'str'})
    df_ratings = pd.read_csv("dataset/Ratings.csv",
                           dtype={'User-ID': 'int32', 'ISBN': 'str', 'BookRating': 'float32'})

    context={'msg':'Books and Rating Two Dataset Successfully Loaded..!!'}
    return render(request,'AdminApp/AdminHome.html', context)


global df_ratings,df_ratings_rm,df,df_books

def Preprocess(request):

    global df_ratings,df_ratings_rm,df,df_books

    df_books.dropna(inplace=True)
    ratings=df_ratings['User-ID'].value_counts()
    ratings.sort_values(ascending=False).head()
    df_ratings['User-ID'].isin(ratings[ratings<200].index).sum()
    df_ratings_rm = df_ratings[
        ~df_ratings['User-ID'].isin(ratings[ratings < 200].index)]
    ratings = df_ratings['ISBN'].value_counts() # we have to use the original df_ratings to pass the challenge
    ratings.sort_values(ascending=False).head()
    df_books['ISBN'].isin(ratings[ratings < 100].index).sum()
    df_ratings_rm = df_ratings_rm[
        ~df_ratings_rm['ISBN'].isin(ratings[ratings < 100].index)
    ]
    # These should exist
    books = ["Where the Heart Is (Oprah's Book Club (Paperback))",
        "I'll Be Seeing You",
        "The Weight of Water",
        "The Surgeon",
        "I Know This Much Is True"]

    for book in books:
        print(df_ratings_rm.ISBN.isin(df_books[df_books.Book_Title == book].ISBN).sum())
    df = df_ratings_rm.pivot_table(index=['User-ID'],columns=['ISBN'],values='Book_Rating').fillna(0).T
    df.head()
    df.index = df.join(df_books.set_index('ISBN'))['Book_Title']
    df = df.sort_index()
    df.loc["The Queen of the Damned (Vampire Chronicles (Paperback))"][:5]

    context={'msg':'Dataset Successfully Processed...!!'}
    return render(request, 'AdminApp/AdminHome.html', context)

global model
def BuildKNN(request):
    global model
    model = NearestNeighbors(metric='cosine')
    model.fit(df.values)
    df.iloc[0].shape
    context={'msg':'KNN Model Successfully Built...!!'}
    return render(request, 'AdminApp/AdminHome.html', context)

def RecommendBook(request):
    return render(request, 'AdminApp/RecommendBook.html')

def get_recommends(title = ""):
  try:
    book = df.loc[title]
  except KeyError as e:
    print('The given book', e, 'does not exist')
    return

  distance, indice = model.kneighbors([book.values], n_neighbors=5)

  recommended_books = pd.DataFrame({
      'title'   : df.iloc[indice[0]].index.values,
      'distance': distance[0]
    }) \
    .sort_values(by='distance', ascending=False) \
    .head(5).values

  return [title, recommended_books]

def RecommendAction(request):
    bname=request.POST['bname']
    df.iloc[0].shape
    title = 'The Queen of the Damned (Vampire Chronicles (Paperback))'
    distance, indice = model.kneighbors([df.loc[title].values], n_neighbors=6)
    df.iloc[indice[0]].index.values
    pd.DataFrame({
        'title'   : df.iloc[indice[0]].index.values,
        'distance': distance[0]
    }) \
        .sort_values(by='distance', ascending=False)
    rec=get_recommends(bname)
    context={'book':rec}
    return render(request,'AdminApp/Recommended.html', context)


def userlogin(request):
    return render(request,'AdminApp/Login.html')


def register(request):
    return render(request,'AdminApp/Register.html')

def regaction(request):
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']
    address=request.POST['address']
    username=request.POST['username']
    password=request.POST['password']

    con=DBConnection()
    cur=con.cursor()
    cur.execute("select * from user where email='"+email+"'")
    data = cur.fetchone()
    if data is not None:
        context={'msg':'User Email Already Exist...!!!'}
        return render(request,'UserApp/Register.html',context)
    else:
        cur.execute("insert into user values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
        con.commit()
        context={'msg':'Registration Successful...!!!'}
        return render(request,'AdminApp/Register.html',context)

def uloginaction(request):
    user=request.POST['username']
    passw=request.POST['password']
    con=DBConnection()
    cur = con.cursor()
    cur.execute("select * from user where username='"+user+"' and password='"+passw+"'")
    data = cur.fetchone()

    global d
    if data is not None:
        uid=str(data[0])
        print("uid: "+uid)
        request.session['userid'] = uid
        request.session['email'] = data[2]
        return render(request,'AdminApp/UserHome.html')
    else:
        context={'msg':'Login Failed...!!!'}
        return render(request,'AdminApp/Login.html',context)

def UserHome(request):
    return render(request,'AdminApp/UserHome.html')


