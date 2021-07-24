
import numpy as np

from scipy.signal import savgol_filter
import copy

def formatOpenPoseStickIndices():
    """
    generate dictionary of arrays, each containing the 'connect-the-dots' order to draw a given body segment
    
    returns:
    openPoseBodySegmentIds= a dictionary of arrays containing indices of individual body segments (Note, a lot of markerless mocap comp sci types like to say 'pose' instead of 'body'. They also use 'pose' to refer to camera 6 DoF position sometimes. Comp sci is frustrating like that lol)
    openPoseHandIds = a dictionary of arrays containing indices of individual hand segments, along with offset to know where to start in the 'skel_fr_mar_dim.shape[1]' part of the array
    dict_of_skel_lineColor = a dictionary of arrays, each containing the color (RGBA) to use for a given body segment
    """
    dict_of_openPoseSegmentIdx_dicts = dict()

    #make body dictionary
    openPoseBodySegmentIds = dict()
    openPoseBodySegmentIds['head'] = [17, 15, 0, 1,0, 16, 18, ]
    openPoseBodySegmentIds['spine'] = [1,8,5,1, 2, 12, 8, 9, 5, 1, 2, 8]
    openPoseBodySegmentIds['rArm'] = [1, 2, 3, 4, ]
    openPoseBodySegmentIds['lArm'] = [1, 5, 6, 7, ]
    openPoseBodySegmentIds['rLeg'] = [8, 9, 10, 11, 22, 23, 11, 24, ]
    openPoseBodySegmentIds['lLeg'] = [8,12, 13, 14, 19, 20, 14, 21,]
    dict_of_openPoseSegmentIdx_dicts['body'] = openPoseBodySegmentIds


    # dict_of_skel_lineColor = dict()
    # dict_of_skel_lineColor['head'] = np.append(humon_dark, 0.5)
    # dict_of_skel_lineColor['spine'] = np.append(humon_dark, 1)
    # dict_of_skel_lineColor['rArm'] = np.append(humon_red, 1)
    # dict_of_skel_lineColor['lArm'] = np.append(humon_blue, 1)
    # dict_of_skel_lineColor['rLeg'] = np.append(humon_red, 1)
    # dict_of_skel_lineColor['lLeg'] = np.append(humon_blue, 1)


    # Make some handy maps ;D
    openPoseHandIds = dict()
    rHandIDstart = 25
    lHandIDstart = rHandIDstart + 21

    openPoseHandIds['thumb'] = np.array([0, 1, 2, 3, 4,  ]) 
    openPoseHandIds['index'] = np.array([0, 5, 6, 7, 8, ])
    openPoseHandIds['bird']= np.array([0, 9, 10, 11, 12, ])
    openPoseHandIds['ring']= np.array([0, 13, 14, 15, 16, ])
    openPoseHandIds['pinky'] = np.array([0, 17, 18, 19, 20, ])
    

    rHand_dict = copy.deepcopy(openPoseHandIds.copy()) #copy.deepcopy() is necessary to make sure the dicts are independent of each other
    lHand_dict = copy.deepcopy(rHand_dict)

    for key in rHand_dict: 
        rHand_dict[key] += rHandIDstart 
        lHand_dict[key] += lHandIDstart 

    dict_of_openPoseSegmentIdx_dicts['rHand'] = rHand_dict
    dict_of_openPoseSegmentIdx_dicts['lHand'] = lHand_dict

    
    #how to face --> :D <--
    openPoseFaceIDs = dict()
    faceIDStart = 67
    #define face parts
    openPoseFaceIDs['jaw'] = np.arange(0,16) + faceIDStart 
    openPoseFaceIDs['rBrow'] = np.arange(17,21) + faceIDStart
    openPoseFaceIDs['lBrow'] = np.arange(22,26) + faceIDStart
    openPoseFaceIDs['noseRidge'] = np.arange(27,30) + faceIDStart
    openPoseFaceIDs['noseBot'] = np.arange(31,35) + faceIDStart
    openPoseFaceIDs['rEye'] = np.concatenate((np.arange(36,41), [36])) + faceIDStart
    openPoseFaceIDs['lEye'] = np.concatenate((np.arange(42,47), [42])) + faceIDStart    
    openPoseFaceIDs['upperLip'] = np.concatenate((np.arange(48,54), np.flip(np.arange(60, 64)), [48])) + faceIDStart
    openPoseFaceIDs['lowerLip'] = np.concatenate(([60], np.arange(64,67), np.arange(54, 59), [48], [60])) + faceIDStart
    openPoseFaceIDs['rPupil'] = np.array([68]) + faceIDStart
    openPoseFaceIDs['lPupil'] = np.array([69]) + faceIDStart #nice

    dict_of_openPoseSegmentIdx_dicts['face'] = openPoseFaceIDs
    
    return dict_of_openPoseSegmentIdx_dicts 


file_path = '/home/prakyath/gitfolder/dash_c3d/freemocap/sesh_21-07-20_165209_noOpenPose/DataArrays/'
skel_fr_mar_dim = np.load( file_path+'openPoseSkel_3d.npy')
openPoseData_nCams_nFrames_nImgPts_XYC = np.load(file_path+'openPoseData_2d.npy')


# smoothThese = np.arange(67, skel_fr_mar_dim.shape[1])
smoothThese = np.arange(0, skel_fr_mar_dim.shape[1])

for mm in smoothThese:
    if mm > 24 and mm < 67: #don't smooth the hands, or they disappear! :O
        pass
    else:
        for dim in range(skel_fr_mar_dim.shape[2]):
            skel_fr_mar_dim[:,mm,dim] = savgol_filter(skel_fr_mar_dim[:,mm,dim], 5, 3)

figure_data = dict()

skel_trajectories = [skel_fr_mar_dim[:,markerNum,:] for markerNum in range(skel_fr_mar_dim.shape[1])]
figure_data['skel_trajectories|mar|fr_dim'] = skel_trajectories
figure_data['skel_fr_mar_dim'] = skel_fr_mar_dim
print(skel_fr_mar_dim.shape)


for key, value in formatOpenPoseStickIndices().items():
    print(key)
    print(value)

