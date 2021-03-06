#!/usr/bin/env python

'''
This is only to be used for the demo not a true classifier it is just a simulation since we did not have data to properly train a classifier

'''
import matplotlib as mpl
mpl.use('pdf')
from time import time
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import glob
import shutil
import os
import zipfile
import uuid
from sklearn import svm
np.random.seed(42)


def machinelearningpipeline(dataset,output='output.pdf'):

	subdir = str(uuid.uuid4())

	# Create a folder for all the temporary stuff and remove at the end
	directory='/tmp/'+subdir+'/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	print ('I am saving temporary things in: %s'%(directory))
	# The input is a zip file: Unzip it in a temp folder and load the csv file as pandas
	ziptoproces=glob.glob("*.zip")
	zip_ref = zipfile.ZipFile(ziptoproces[0], 'r')
	zip_ref.extractall(directory)
	zip_ref.close()
	# Load CSV
	data=pd.read_csv(directory+'/3D.feature.csv', index_col=0, header=None).T
	h = .02  # step size in the mesh
	name =data['aa_info.patient.FamilyName'].values[0]
	volume=data['size.volume(mm^3)'].values[0]
	print volume
	volume=float(volume)/1000
	sphericity=float(data['sphericity.value'].values[0])
	print sphericity
	class1=np.random.random((40, 2))
	class1[:,0]=5*class1[:,0]
	class2=np.random.random((40, 2))
	class2[:,0]=class2[:,0]
	X=np.append(class1,class2,axis=0)
	y=np.append(np.zeros((len(class1))),np.ones((len(class2))),axis=0)
	C = 1.0  # SVM regularization parameter
	svc = svm.SVC(kernel='rbf', gamma=1, C=C).fit(X, y)
	# create a mesh to plot in
	x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
						 np.arange(y_min, y_max, h))
	# title for the plots
	titles = ['SVC with linear kernel']
	f=plt.figure( figsize=(16, 12), dpi=300, facecolor='w', edgecolor='k')
	clf=svc
	Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	# Plot also the training points
	plt.contourf(xx, yy, Z, cmap=plt.cm.bwr, alpha=0.8)
	# Plot also the training points
	classes = ['Benign','Malignant']
	colours = ['b','r']
	for (i,cla) in enumerate(set(classes)):
		print i
		Xz=X.copy()
		Xz=np.delete(Xz,np.nonzero(y==i),axis=0)	
		plt.scatter(Xz[:, 0], Xz[:, 1],c=colours[i],label=classes[i])
	plt.xlabel('Volume mm^3')
	plt.ylabel('Sphericity(range: 0-1)')
	plt.plot(volume,sphericity,'k*', markersize=20,label='Unknown Case')
	plt.annotate('Unknown Case: Features --> Volume '+str(1000*volume)+ ' Sphericity '+str(sphericity), xy=(volume+0.05,sphericity+0.05), xytext=(volume+0.3,sphericity+0.3),
            arrowprops=dict(facecolor='black', shrink=0.03),color='black', fontsize=9)
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.xticks(())
	plt.yticks(())
	plt.legend()
	noduletype=clf.predict([volume,sphericity])
	if noduletype==0.:
		plt.title('The classification for this case is benign')
	else:
		plt.title('The classification for this case is malignant')
	f.savefig(output)

	return output


def main(argv):
	machinelearningpipeline(argv.dataset, argv.output)
	return 0

if __name__ == "__main__":
	parser = argparse.ArgumentParser( description='Apply a trained model')
	parser.add_argument ("-i", "--dataset",  help="unknowdata these data have to be in the format that standford feature calculator outputs" , required=True)
	parser.add_argument ("-o", "--output",  help="output name of zip file" , required=False)
	parser.add_argument('--version', action='version', version='%(prog)s 0.1')
	parser.add_argument("-q", "--quiet",
						  action="store_false", dest="verbose",
						  default=True,
						  help="don't print status messages to stdout")
	args = parser.parse_args()
	main(args)
