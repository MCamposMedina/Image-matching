# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 08:43:50 2023

@author: camposm
"""
from skimage import io
from pytictoc import TicToc
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import tifffile




####### Definition of input output parameters

os.chdir('C:\\Users\\camposm\\Documents')
save_target = '\\Results\\'
dirt = os.getcwd()
t=TicToc()
List_Templates = glob.glob('*_Trans.tif')




##len(List_Templates)

for i in range(0,len(List_Templates)) :
    
    
    ### Reading section
    t.tic()
    print(List_Templates[i])
    Template= '\\' + List_Templates[i]
    name_fig=List_Templates[i]
    name_fig=name_fig.replace('_Trans.tif','', 1)
    Section= Template.replace('_Trans','',1)
    
    
    # the window showing output image         
    # with the corresponding thresholding         
    # techniques applied to the input image  
    
    try:
        print('Loading Images')
        image = cv2.imread(dirt + Template, 0)
        
        
        Size_f=970####970 for normal binning  ## 1552
        image_t = cv2.resize(image,(Size_f,Size_f), interpolation = cv2.INTER_CUBIC)
    
        ### try equalizing hist
    
       
     
        image_s = cv2.imread(dirt + Section, 0)
        ##image_s = cv2.resize(image_s,(648,484), interpolation = cv2.INTER_CUBIC)

       # image_t = cv2.equalizeHist(image_t)
        #image_s = cv2.equalizeHist(image_s)
        
        plt.imshow(image_t)  
        plt.imshow(image_s)
    
        ## 
        # All the 6 methods for comparison in a list
    ##methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
      ##          'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    
        (rows, cols) = image_t.shape[:2]
        angle = np.linspace(0,180,181)
        temp= np.zeros(len(angle))
        cont=0
        
        
        for j in angle:
            #### Section for optimizing images
            ######## Rotation
            temp_image= image_t
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2),j, 1)
            Trans = cv2.warpAffine(temp_image, M, (cols, rows))
            
        
            # warpAffine does appropriate shifting given the
            # translation matrix.
            #plt.imshow(Trans)
        
            temp_image= Trans    
                
            res=cv2.matchTemplate(temp_image,image_s,cv2.TM_CCOEFF)
            temp[cont]= np.max(res)
            cont=cont+1
        
        opt_angle= angle[temp == np.max(temp)]
        print('The optimized angle is: ',opt_angle[0])
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2),opt_angle[0], 1)
        Trans = cv2.warpAffine(image_t, M, (cols, rows))
            
        
            # warpAffine does appropriate shifting given the
            # translation matrix.
            #plt.imshow(Trans)
        
        image_t= Trans    
                
        res=cv2.matchTemplate(image_t,image_s,cv2.TM_CCOEFF)
        threshold = np.max(res)
        w, h = image_s.shape[::-1]
        loc=np.where(res >= threshold)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
    
        cv2.rectangle(image_t,top_left, bottom_right, 0, 10)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(image_t,cmap = 'gray')
        plt.title(Section), plt.xticks([]), plt.yticks([])
        plt.show()
        plt.close()
   
        
        #### Open all slides of .tif
        im = io.imread(dirt + Template)
        im = cv2.resize(im,(Size_f, Size_f), interpolation = cv2.INTER_CUBIC)
        Trans = cv2.warpAffine(im[:,:,0], M, (cols, rows)) ### Transmission image
        
        
        image_s_1=Trans[top_left[1]:(top_left[1]+484),top_left[0]:(top_left[0]+648)]
        
        plt.subplot(121),plt.imshow(image_s,cmap = 'gray')
        plt.title('Color image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(image_s_1,cmap = 'gray')
        plt.title('Extracted Segment'), plt.xticks([]), plt.yticks([])
       # plt.show()
    #    plt.savefig('Comparison.jpeg')    
        #
        plt.savefig('Comparison_'+name_fig+'.png', format="png", dpi =600) # specify filetype explicitly
        plt.show()

        plt.close()
     #   Trans = cv2.warpAffine(im[:,:,3], M, (cols, rows))
     #   plt.imshow(Trans)
     
          
        ######### Saving images as a single tif
        #Full_tiff= Dummy=np.zeros((484,648,5)) ##### Colo + Trans + 3F
        Mono_tiff= Dummy=np.zeros((4,484,648)) ##### Trans + 3F
        Fluor_tiff= Dummy=np.zeros((3,484,648)) #####3F
        T_DAPI_tiff= Dummy=np.zeros((2,484,648)) #####3F
        T_D_R_tiff= Dummy=np.zeros((3,484,648)) #####3F
        D_R_tiff= Dummy=np.zeros((3,484,648)) #####3F

    ######### Saving section
        #### Transmission images
        #mono= Image.fromarray(image_s_1)
        
        ### DAPI
        Trans_2 = cv2.warpAffine(im[:,:,1], M, (cols, rows)) ### Transmission image
        image_s_2=Trans_2[top_left[1]:(top_left[1]+484),top_left[0]:(top_left[0]+648)]
      #  fluor_1= Image.fromarray(image_s_2)
        
        ##### Yellow
       # Trans_3 = cv2.warpAffine(im[:,:,2], M, (cols, rows)) ### Transmission image
      #  image_s_3=Trans_3[top_left[1]:(top_left[1]+484),top_left[0]:(top_left[0]+648)]
       # fluor_2= Image.fromarray(image_s_3)  
        
        
        ##### Red
        Trans_4 = cv2.warpAffine(im[:,:,2], M, (cols, rows)) ### Transmission image
        image_s_4=Trans_4[top_left[1]:(top_left[1]+484),top_left[0]:(top_left[0]+648)]
        #fluor_3= Image.fromarray(image_s_4)  
        
        
        
        
        
        
        
        
        ####### Saving transmission Images
        tifffile.imwrite(dirt + save_target + 'Transmission\\'  + name_fig + '.tif' ,image_s_1,photometric='minisblack')
      
        
      
        ##### Saving Transmission + DAPI images

        T_DAPI_tiff[0,:,:]= image_s_1 #####1F
        T_DAPI_tiff[1,:,:]= image_s_2 #####1F



        tifffile.imwrite(dirt + save_target + 'T_DAPI\\' + name_fig + '.tif',  T_DAPI_tiff ,photometric='minisblack')
      
        
        ##### Saving Transmission + DAPI images

        T_D_R_tiff[0,:,:]= image_s_1 #####1F
        T_D_R_tiff[1,:,:]= image_s_2 #####1F
        T_D_R_tiff[2,:,:]= image_s_4 #####2F

        tifffile.imwrite(dirt + save_target + 'T_D_R\\' + name_fig + '.tif',  T_D_R_tiff ,photometric='minisblack')


       ##### Saving Transmission + DAPI images

        D_R_tiff[0,:,:]= image_s_2 #####1F
        D_R_tiff[1,:,:]= image_s_4 #####1F



        tifffile.imwrite(dirt + save_target + 'D_R\\' + name_fig + '.tif',  D_R_tiff ,photometric='minisblack')
        
      
        
        ##### Saving Fluorescent images

        #Fluor_tiff[0,:,:]= image_s_2 #####1F
       # Fluor_tiff[1,:,:]= image_s_3 #####2F
        #Fluor_tiff[2,:,:]= image_s_4 #####2F


        #tifffile.imwrite(dirt + save_target + 'Fluor\\' + name_fig + '.tif', Fluor_tiff ,photometric='minisblack')

        






        ##### Saving Monochromatic images

       # Mono_tiff[0,:,:]= image_s_1 #####1F
        #Mono_tiff[1,:,:]= image_s_2 #####1F
        #Mono_tiff[2,:,:]= image_s_3 #####2F
        #Mono_tiff[2,:,:]= image_s_4 #####2F


        #tifffile.imwrite(dirt + save_target + 'Full_mono\\' + name_fig + '.tif', Mono_tiff ,photometric='minisblack')




       ## Make a matrix of zeros 3 or more dimensions. Store the grayscale things and then save
      ### Good for saving the tiff tifffile.imwrite('yourfile7.tiff',Dummy.transpose(),photometric='minisblack')
     
     
     
     
     
     
        t.toc()
        
    except IOError:
        print("Files couldn't be loaded")
    
        






