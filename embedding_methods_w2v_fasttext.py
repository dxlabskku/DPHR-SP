import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt, Mecab
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, plot_roc_curve, roc_curve, f1_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
from gensim.models import FastText
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.linear_model import LogisticRegression


def mecab_w2v_target_rf(data): # Mecab + Word2Vec Binary Classification

    X = data['clean_words_mecab']
    labels = data['target'].tolist()

    X_train, X_test, Y_train, Y_test = train_test_split(X, labels, test_size = 0.2, random_state = 42)
    X_tr, X_val, Y_tr, Y_val = train_test_split(X_train, Y_train, test_size = 0.2, random_state = 42)   

    model = Word2Vec(sentences = X_tr, vector_size = 100, window = 5, min_count = 0, workers = 4, sg = 1)
    
    words = set(model.wv.index_to_key)
    X_train_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_tr])
    X_val_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_val])
    X_test_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_test])

    X_train_vect_avg = []
    for v in X_train_vect:
        if v.size:
            X_train_vect_avg.append(v.mean(axis = 0))
        else:
            X_train_vect_avg.append(np.zeros(100,dtype = float))

    X_val_vect_avg = []
    for v in X_val_vect:
        if v.size:
            X_val_vect_avg.append(v.mean(axis = 0))
        else:
            X_val_vect_avg.append(np.zeros(100,dtype = float))

    X_test_vect_avg = []
    for v in X_test_vect:
        if v.size:
            X_test_vect_avg.append(v.mean(axis = 0))
        else:
            X_test_vect_avg.append(np.zeros(100,dtype = float))

    clf = RandomForestClassifier()
    clf.fit(X_train_vect_avg, Y_tr)

    y_pred_tr = clf.predict(X_train_vect_avg)
    report = classification_report(Y_tr, y_pred_tr, labels = [0, 1], target_names = ['not helpful', 'helpful'], output_dict = True, digits = 4)

    fig, axes = plt.subplots(nrows = 3, sharex = True)
    fig.tight_layout(pad = 2.0)
    plt.figure(figsize = (10, 10))
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[0])

    y_pred_va = clf.predict(X_val_vect_avg)
    report = classification_report(Y_val, y_pred_va, labels = [0, 1], target_names = ['not helpful', 'helpful'], output_dict = True, digits = 4)
    
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[1])

    y_pred_te = clf.predict(X_test_vect_avg)
    report = classification_report(Y_test, y_pred_te, labels = [0, 1], target_names = ['not helpful', 'helpful'], output_dict = True, digits = 4)

    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[2])
    
    axes[0].set_title('Train Classification Report')
    axes[1].set_title('Validation Classification Report')
    axes[2].set_title('Test Classification Report')
    plt.show()
    print(pd.DataFrame(report))
    print(accuracy_score(Y_test, y_pred_te))

def mecab_w2v_cat_rf(data): # Mecab + Word2Vec Multi-class Classification

    data = data[data['category'] > 0].reset_index(drop = True)
    X = data['clean_words_mecab']
    labels = data['category'].tolist()

    X_train, X_test, Y_train, Y_test = train_test_split(X, labels, test_size = 0.2, random_state = 42)
    X_tr, X_val, Y_tr, Y_val = train_test_split(X_train, Y_train, test_size = 0.2, random_state = 42)   

    model = Word2Vec(sentences = X_tr, vector_size = 100, window = 5, min_count = 0, workers = 4, sg = 1)
    
    words = set(model.wv.index_to_key)
    X_train_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_tr])
    X_val_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_val])
    X_test_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_test])

    X_train_vect_avg = []
    for v in X_train_vect:
        if v.size:
            X_train_vect_avg.append(v.mean(axis = 0))
        else:
            X_train_vect_avg.append(np.zeros(100,dtype = float))

    X_val_vect_avg = []
    for v in X_val_vect:
        if v.size:
            X_val_vect_avg.append(v.mean(axis = 0))
        else:
            X_val_vect_avg.append(np.zeros(100,dtype = float))

    X_test_vect_avg = []
    for v in X_test_vect:
        if v.size:
            X_test_vect_avg.append(v.mean(axis = 0))
        else:
            X_test_vect_avg.append(np.zeros(100,dtype = float))

    clf = RandomForestClassifier()
    clf.fit(X_train_vect_avg, Y_tr)

    y_pred_tr = clf.predict(X_train_vect_avg)
    report = classification_report(Y_tr, y_pred_tr, labels = [1, 2, 3, 4], target_names = ['cat1', 'cat2', 'cat3', 'cat4'], output_dict = True, digits = 4)

    fig, axes = plt.subplots(nrows = 3, sharex = True)
    fig.tight_layout(pad = 2.0)
    plt.figure(figsize = (10, 10))
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[0])

    y_pred_va = clf.predict(X_val_vect_avg)
    report = classification_report(Y_val, y_pred_va, labels = [1, 2, 3, 4], target_names = ['cat1', 'cat2', 'cat3', 'cat4'], output_dict = True, digits = 4)
    
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[1])

    y_pred_te = clf.predict(X_test_vect_avg)
    report = classification_report(Y_test, y_pred_te, labels = [1, 2, 3, 4], target_names = ['cat1', 'cat2', 'cat3', 'cat4'], output_dict = True, digits = 4)

    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[2])
    
    axes[0].set_title('Train Classification Report')
    axes[1].set_title('Validation Classification Report')
    axes[2].set_title('Test Classification Report')
    plt.show()
    print(pd.DataFrame(report))
    print(accuracy_score(Y_test, y_pred_te))

def mecab_fasttext_target_rf(data): # Mecab + Fasttext Binary Classification

    X = data['clean_words_mecab']
    labels = data['target'].tolist()

    X_train, X_test, Y_train, Y_test = train_test_split(X, labels, test_size = 0.2, random_state = 42)
    X_tr, X_val, Y_tr, Y_val = train_test_split(X_train, Y_train, test_size = 0.2, random_state = 42)   

    model = FastText(sentences = X_tr, vector_size = 100, window = 5, min_count = 0, workers = 4, sg = 1)
    
    words = set(model.wv.index_to_key)
    X_train_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_tr])
    X_val_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_val])
    X_test_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_test])

    X_train_vect_avg = []
    for v in X_train_vect:
        if v.size:
            X_train_vect_avg.append(v.mean(axis = 0))
        else:
            X_train_vect_avg.append(np.zeros(100,dtype = float))

    X_val_vect_avg = []
    for v in X_val_vect:
        if v.size:
            X_val_vect_avg.append(v.mean(axis = 0))
        else:
            X_val_vect_avg.append(np.zeros(100,dtype = float))

    X_test_vect_avg = []
    for v in X_test_vect:
        if v.size:
            X_test_vect_avg.append(v.mean(axis = 0))
        else:
            X_test_vect_avg.append(np.zeros(100,dtype = float))

    clf = RandomForestClassifier()
    clf.fit(X_train_vect_avg, Y_tr)

    y_pred_tr = clf.predict(X_train_vect_avg)
    report = classification_report(Y_tr, y_pred_tr, labels = [0, 1], target_names = ['not helpful', 'helpful'], output_dict = True, digits = 4)

    fig, axes = plt.subplots(nrows = 3, sharex = True)
    fig.tight_layout(pad = 2.0)
    plt.figure(figsize = (10, 10))
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[0])

    y_pred_va = clf.predict(X_val_vect_avg)
    report = classification_report(Y_val, y_pred_va, labels = [0, 1], target_names = ['not helpful', 'helpful'], output_dict = True, digits = 4)
    
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[1])

    y_pred_te = clf.predict(X_test_vect_avg)
    report = classification_report(Y_test, y_pred_te, labels = [0, 1], target_names = ['not helpful', 'helpful'], output_dict = True, digits = 4)

    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[2])
    
    axes[0].set_title('Train Classification Report')
    axes[1].set_title('Validation Classification Report')
    axes[2].set_title('Test Classification Report')
    plt.show()
    print(pd.DataFrame(report))
    print(accuracy_score(Y_test, y_pred_te))

def mecab_fasttext_cat_rf(data): # Mecab + Fasttext Multi-class Classification

    data = data[data['category'] > 0].reset_index(drop = True)
    X = data['clean_words_mecab']
    labels = data['category'].tolist()

    X_train, X_test, Y_train, Y_test = train_test_split(X, labels, test_size = 0.2, random_state = 42)
    X_tr, X_val, Y_tr, Y_val = train_test_split(X_train, Y_train, test_size = 0.2, random_state = 42)   

    model = FastText(sentences = X_tr, vector_size = 100, window = 5, min_count = 0, workers = 4, sg = 1)
    
    words = set(model.wv.index_to_key)
    X_train_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_tr])
    X_val_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_val])
    X_test_vect = np.array([np.array([model.wv[i] for i in ls if i in words]) for ls in X_test])

    X_train_vect_avg = []
    for v in X_train_vect:
        if v.size:
            X_train_vect_avg.append(v.mean(axis = 0))
        else:
            X_train_vect_avg.append(np.zeros(100,dtype = float))

    X_val_vect_avg = []
    for v in X_val_vect:
        if v.size:
            X_val_vect_avg.append(v.mean(axis = 0))
        else:
            X_val_vect_avg.append(np.zeros(100,dtype = float))

    X_test_vect_avg = []
    for v in X_test_vect:
        if v.size:
            X_test_vect_avg.append(v.mean(axis = 0))
        else:
            X_test_vect_avg.append(np.zeros(100,dtype = float))

    clf = RandomForestClassifier()
    clf.fit(X_train_vect_avg, Y_tr)

    y_pred_tr = clf.predict(X_train_vect_avg)
    report = classification_report(Y_tr, y_pred_tr, labels = [1, 2, 3, 4], target_names = ['cat1', 'cat2', 'cat3', 'cat4'], output_dict = True, digits = 4)

    fig, axes = plt.subplots(nrows = 3, sharex = True)
    fig.tight_layout(pad = 2.0)
    plt.figure(figsize = (10, 10))
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[0])

    y_pred_va = clf.predict(X_val_vect_avg)
    report = classification_report(Y_val, y_pred_va, labels = [1, 2, 3, 4], target_names = ['cat1', 'cat2', 'cat3', 'cat4'], output_dict = True, digits = 4)
    
    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[1])

    y_pred_te = clf.predict(X_test_vect_avg)
    report = classification_report(Y_test, y_pred_te, labels = [1, 2, 3, 4], target_names = ['cat1', 'cat2', 'cat3', 'cat4'], output_dict = True, digits = 4)

    sns.heatmap(pd.DataFrame(report).iloc[:-1, :-2].T, annot = True, ax = axes[2])
    
    axes[0].set_title('Train Classification Report')
    axes[1].set_title('Validation Classification Report')
    axes[2].set_title('Test Classification Report')
    plt.show()
    print(pd.DataFrame(report))
    print(accuracy_score(Y_test, y_pred_te))