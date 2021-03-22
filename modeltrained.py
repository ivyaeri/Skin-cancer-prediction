import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
# Load dataset
def model(feat):
        
        X_test1=feat
        print(X_test1)
        
        df=pd.read_csv('C:/Users/lahar/OneDrive/Desktop/project/skincann.csv')
        df.shape

        x=df.drop('class',axis=1)

        y=df['class']
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)
        from sklearn.svm import SVC
        svclassifier = SVC(kernel='linear')
        svclassifier.fit(X_train, y_train)
        y=svclassifier.predict(X_test)
        from sklearn.metrics import confusion_matrix,accuracy_score
        a=accuracy_score(y_test, y)
        print(confusion_matrix(y_test,y))
                
        if len(X_test1)==1:
                y_pred=['non cancer']
                
                return (y_pred,a)
                
        else:
                y_pred = svclassifier.predict(np.reshape(X_test1,(1,-1)))
                
                
                return(y_pred,a)
        
        
                        


