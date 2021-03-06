import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.externals import joblib 


# Load Data
df=pd.read_csv('gauge_data.csv', sep=',')
husum_ft = df.pop('husum_ft').values
usgs_cfs = df.pop('usgs_cfs').values[:, np.newaxis]
usgs_ft = df.pop('usgs_ft').values[:, np.newaxis]

# Calculate Linear Regression for height
linear_model_height = LinearRegression()
linear_model_height.fit(usgs_ft, husum_ft)
x_height = np.linspace(3,7,100)[:, np.newaxis]
y_linear_pred_height = linear_model_height.predict(x_height)

# Calculate Polynomial Regression for height
poly_model_height = make_pipeline(PolynomialFeatures(3),LinearRegression())
poly_model_height.fit(usgs_ft, husum_ft)
y_poly_pred_height = poly_model_height.predict(x_height)

# Calculate Linear Regression for CFS
linear_model_cfs = LinearRegression()
linear_model_cfs.fit(usgs_cfs, husum_ft)
x_cfs = np.linspace(500,3500,100)[:, np.newaxis]
y_linear_pred_cfs = linear_model_cfs.predict(x_cfs)

# Calculate Polynomial Regression for CFS
poly_model_cfs = make_pipeline(PolynomialFeatures(3),LinearRegression())
poly_model_cfs.fit(usgs_cfs, husum_ft)
y_poly_pred_cfs = poly_model_cfs.predict(x_cfs)

# Plot Height Regression
axes_ht = plt.subplot(1,2,1)
axes_ht.scatter(usgs_ft,husum_ft,marker='+')
axes_ht.plot(x_height,y_linear_pred_height,color='r')
axes_ht.plot(x_height,y_poly_pred_height,color='g')
axes_ht.plot(x_height,(-4.020+1.539*x_height),color='y')


axes_ht.legend(['linear model', 'cubic model','wkcc model','raw data'])
axes_ht.set_xlabel('Underwood Gauge Height (ft)')
axes_ht.set_ylabel('Husum Gauge Height (ft)')
axes_ht.set_title('Husum Height vs Underwood Height')

# Plot CFS Regression
axes_cfs = plt.subplot(1,2,2)
axes_cfs.scatter(usgs_cfs,husum_ft,marker='+')
axes_cfs.plot(x_cfs,y_linear_pred_cfs,color='r')
axes_cfs.plot(x_cfs,y_poly_pred_cfs,color='g')

axes_cfs.legend(['linear model', 'cubic model','raw data'])
axes_cfs.set_xlabel('Underwood Gauge Flow Rate (CFS)')
axes_cfs.set_ylabel('Husum Gauge Height (ft)')
axes_cfs.set_title('Husum Height vs Underwood CFS')


plt.show()

joblib.dump(poly_model_cfs, 'poly_model_cfs.pkl') 
print(linear_model_height.coef_)
print(linear_model_height.intercept_)
print(poly_model_height.steps[1][1].coef_)
print(poly_model_height.steps[1][1].intercept_)




