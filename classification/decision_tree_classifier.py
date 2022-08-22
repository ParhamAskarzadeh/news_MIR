import pandas as pd
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics, tree
from sklearn.metrics import classification_report


class DecisionTreeClassify:
    def __init__(self, file):
        self.file = file
        self.le = preprocessing.LabelEncoder()
        self.cv = CountVectorizer()
        self.dt_model = tree.DecisionTreeClassifier()

    def __set_data_frame_of_news(self, file, default_categories):
        if default_categories is None:
            default_categories = {'استان ها', 'ورزشی', 'سیاسی', 'علمی پزشکی', 'شهروند خبرنگار'}
        contents = []
        labels = []
        count = 0
        for data in file:
            count += 1
            if 'content' in data and 'categories' in data:
                intersection = default_categories.intersection(set(data['categories']))
                if len(intersection) != 0:
                    labels.append(list(intersection)[0])
                else:
                    continue
                contents.append(data['content'])
            if count > 9000:
                break
        df = pd.DataFrame({
            'contents': contents,
            'labels': labels
        })
        return df

    def job(self, default_categories=None):
        df = self.__set_data_frame_of_news(self.file, default_categories=default_categories)
        df['v_labels'] = self.le.fit_transform(df['labels'])
        bow = self.cv.fit_transform(df['contents']).toarray()
        x_train, x_test, y_train, y_test = train_test_split(bow, df['labels'], test_size=0.3, random_state=0)
        self.dt_model.fit(x_train, y_train)
        y_pred = self.dt_model.predict(x_test)
        return y_pred

    def report(self, y_test, y_pred):
        print('Accuracy:', metrics.accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))
