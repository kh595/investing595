from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# 이차함수 오목함수 꼴이면 turn around 로 판단
def get_coef_regression(x,y):
    degree = 2
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(x, y)
    y_plot = model.predict(x)
   
    start_val = y[0]
    curvature = model.steps[1][1].coef_[2]
    end_val = y[-1]    
    
    is_ta = False
    if (curvature > 2) & (y.min() < end_val):
        is_ta = True
            
    return is_ta, start_val, curvature, end_val, y_plot