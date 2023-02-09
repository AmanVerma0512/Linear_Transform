#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
import matplotlib.pyplot as plt
import numpy as np
from Updated_Scores import get_score
import pandas as pd
import yaml
import boto3
import streamlit as st
import gspread
from SignalProcessing import *
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(layout="wide")
st.title("Signal Comparison")


# In[7]:


def return_sig(y, label):
    
    if label == "decay":
        return decay(y)
    
    elif label == "noisy":
        return noisy(y)
    
    elif label == "release":
        return release(y)
    
    elif label == "distort":
        return distort(y)
    
    elif label == "smoothen":
        return smoothen(y)   


# In[23]:


signal_input = st.text_input('Pass the signal array(with [])', key = "signal_input", value = "[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11.729523198375265, 13.683759597296039, 14.660438032882045, 16.614332452678642, 16.613501842951518, 15.635455317411328, 13.68033943958757, 14.656773761393556, 14.656041017006194, 13.67828775530125, 13.677603928918678, 12.699997269814238, 13.676236378712586, 10.74507708598158, 9.767763546600355, 9.767275221268166, 9.766786920349103, 9.766298643841944, 9.765810391745468, 9.765322164058455, 9.764833960779686, 9.76434578190794, 9.763857627441997, 9.763369497380635, 0, 9.76239331046678, 0, 9.761417221156615, 12.689207977029827, 13.664617721216535, 15.615925232283104, 16.591091070024145, 16.590261622216623, 14.637734308126017, 14.63700251558882, 13.660519375660773, 12.684133834898372, 13.659153533647462, 12.682865616434805, 11.706675281312029, 10.730582520962272, 9.754587328069164, 9.754099661463126, 9.75361201923728, 9.75312440139041, 9.752636807921295, 9.752149238828716, 9.751661694111455, 9.751174173768293, 9.750686677798011, 9.75019920619939, 9.749711758971214, 9.749224336112263, 10.723610631383451, 9.748249563497163, 11.697314656486293, 12.671457354847648, 15.594860139701195, 16.56871052809491, 16.567882199170487, 15.592521328618524, 14.617257940193754, 14.616527171343211, 12.667023580489554, 12.666390310809318, 11.691468067189374, 11.690883569008143, 10.716107508377391, 9.741428883589723, 9.740941874821248, 10.714500379440087, 9.739967930325, 9.739480994594789, 9.738994083208233, 9.738507196164113, 9.738020333461213, 9.737533495098315, 10.710751349181624, 10.710215880526427, 10.709680438641218, 10.709145023524657, 10.708609635175408, 9.734612975992848, 0, 10.707003630718146, 14.5997295673974, 15.572266319842901, 15.571487806717835, 15.570709332513417, 15.5699308972277, 15.569152500858738, 14.595350759441802, 11.675696868647476, 11.675113158924702, 11.674529478383658, 10.701117008104312, 10.700582021104182, 9.7273155098636, 9.726829206673008, 0, 10.698442340549372, 10.697907487265411, 9.724884237018793, 10.69683786091382, 9.723911898039564, 0, 9.722939656279289, 10.694698929038545, 11.6663610140739, 10.693629623493472, 11.665194557252072, 10.69256042486252, 0, 11.66344509069273, 16.522387824096704, 16.521561811009445, 16.520735839217522, 16.51990990871888, 14.575662370157158, 11.659946944653994, 10.687750353798911, 11.658781129140543, 10.686681743004582, 9.714679525158939, 9.714193853686282, 10.685079027143484, 9.713222583581103, 9.712736984946153, 9.71225141058801, 9.71176586050546, 9.71128033469729, 9.71079483316229, 9.71030935589924, 9.70982390290693, 9.709338474184145, 10.679738376702643, 9.708367689542303, 0, 9.707397001964006, 14.560367541855983, 16.500924899447238, 15.529505844111172, 16.499275060530696, 14.557456061411392, 13.58627973011869, 12.615200467577877, 12.614569788719859, 11.64363613051544, 10.672799521654687, 10.672265950346688, 10.671732405713819, 10.67119888775475, 9.700604905880134, 9.700119938047887, 10.669598493907003, 9.699150075117995, 9.698665180017926, 0, 9.697695462541482, 10.66693170417895, 10.66639842622407, 9.696241068117871, 9.695756318449437, 10.664798752316901, 9.694786891814447, 9.694302214845472, 9.693817562107226, 0, 9.692848329318078, 15.507781998823605, 15.507006709499702, 15.506231458935279, 14.536365231682868, 15.504681074077112, 15.503905939779496, 13.565239488704405, 12.595664077292977, 11.626185577041948, 10.656803980684767, 10.656271209050901, 10.65573846405219, 10.655205745687299, 9.686066412686273, 9.685582171685146, 9.685097954892953, 9.684613762308485, 9.684129593930532, 9.683645449757881, 9.683161329789325, 9.682677234023652, 9.682193162459653, 10.649880026605729, 9.681225091931834, 10.648815202262156, 9.680257118196193, 10.647750484384655, 9.67928924124305, 0, 9.67832146106273, 13.548972650163094, 15.483766044232885, 15.482991955552196, 16.449856524669144, 15.481443894287242, 15.480669921699109, 14.512402488566835, 13.544231831026623, 12.576157941822204, 11.608180813697796, 11.607600479343375, 10.63976849283511, 9.672033248060028, 10.638704679489528, 10.638172812704273, 10.637640972508933, 10.637109158902183, 9.669615792620629, 9.669132374044663, 10.635513877600168, 9.668165609394979, 10.634450489650728, 9.667198941406902, 9.666715643657948, 10.632855607077849, 9.665749120644163, 9.665265895376919, 10.631260963694611, 10.630729469047253, 0]")
signal_desc = st.text_input('Enter Signal Description', key = "signal_desc")

signal_fields = ["decay","noisy","release","distort","smoothen"]

signal_b = st.selectbox('Choose Second Signal',signal_fields,key="s_b")
meta_tag = st.selectbox("Display Meta Values?",["False","True"],key="meta_tag")


# In[26]:


flag = True
if flag == True:
    st.header("Signal Plots and Scores")
    x1 = eval(signal_input)
    workoutData1 = list(map(float, x1))
    x2 = return_sig(x1, signal_b)
    workoutData2 = list(map(float, x2))

    st.subheader("Plots")
    st.write("Plot Corresponding to Base Signal")
    chart_data1 = pd.DataFrame(
    np.array(workoutData1),
    columns=['workout'])
    st.line_chart(chart_data1)

    st.write("Plot Corresponding to Signal " + str(signal_b))
    chart_data2 = pd.DataFrame(
    np.array(workoutData2),
    columns=['workout'])
    st.line_chart(chart_data2)

    header={
        "subScores":True,
        "coachingTip":True,
        "score":True,
        "meta":True
    }

    h_params={
                            "global_score": 25,
                            "setting":"experiment",
                             "bwt": 60,
                             "gender": "men's",
                             "exercise_mode": "Equipped Powerlifting",
                             "l0": 1,
                             "l1": 1,
                             "l2": 1,
                             "l3": 1,
                             "power":{
                                 "w_power": 1,
                                 "w_explosiveness": 1,
                                  "peaks": {
                                      "sz": 12,
                                      "max_win": 100
                                  },

                                  "mode": {
                                      "sz": 12
                                  },
                                "power":{
                                    "growth factor":1.15,
                                     "bwt": 60,
                                     "gender": "men's",
                                     "exercise_mode": "Equipped Powerlifting",
                                     "scipyPeaks":False,
                                     "intervalPeaks":None
                                     # "peaks": {
                                     #     "sz": 12,
                                     #     "max_win": 100
                                     # },
                                 },
                                 "explosiveness":{
                                     "scipyPeaks":False,
                                     "intervalPeaks":None
                                     # "peaks": {
                                     #     "sz": 12,
                                     #     "max_win": 100
                                     # },
                                 }
                             },

                             "formScore":{
                                "w_jitter": 1,
                                "w_tempo": 1,
                                "w_sudden release": 1,
                                "sudden release": {
                                    "max_to_fall_ratio": 0.4,
                                    "fall_time": 4
                                },
                                "tempo":{
                                    "scipyPeaks":False,
                                    "intervalPeaks":False
                                },
                                "peaks": {
                                    "sz": 12,
                                    "max_win": 100
                                },
                                "jitter": {
                                    "window_size": 4,
                                    "delta": 2,
                                    "t0": 2,
                                    "x_dist_rel": 0.2,
                                    "jitterPolicyThreshold":4,
                                    "scipyPeaks":False,

                                    # "smoothBlips": {
                                    #     "smoothenFactor": 2,
                                    #     "prominentPeaksProminence":0.5,
                                    #     "prominentPeaksWidth":2,
                                    #     "smallPeaksHeightLowerFactor":0.6,
                                    #     "smallPeaksHeightHigherFactor":0.8,
                                    #     "smallPeaksWidth":2
                                    # }
                                },

                                "peaks": {
                                    "sz": 12,
                                    "max_win": 100
                                },

                                "mode": {
                                    "sz": 12
                                },
                             },

                             "stamina":{
                                "w_ring stamina": 1,
                                "w_area stamina": 1,
                                "w_total time":1,
                                "peaks": {
                                    "scipyPeaks":False,
                                    "intervalPeaks":None,
                                    "sz": 12,
                                    "max_win": 100
                                },
                                "area stamina":
                                {
                                    "referenceFactor":1.4,
                                    "peaks":{
                                    "scipyPeaks":False,
                                    "intervalPeaks":None
                                    # "peaks": {
                                    #     "sz": 12,
                                    #     "max_win": 100
                                    # },
                                    }
                                },
                                "total time":
                                {
                                    "referenceFactor":1.4,
                                    "peaks":{
                                    "scipyPeaks":False,
                                    "intervalPeaks":None
                                    # "peaks": {
                                    #     "sz": 12,
                                    #     "max_win": 100
                                    # },
                                    }
                                },
                                "ring stamina":{
                                    "baseBased":False,
                                    "peakBased":{
                                        "power_ref":0.8,
                                        "time_ref":200
                                    }
                                },
                                "peaks":{
                                     "scipyPeaks":False,
                                     "intervalPeaks":None
                                     # "peaks": {
                                     #     "sz": 12,
                                     #     "max_win": 100
                                     # },
                                     },
                                 "mode": {
                                     "sz": 12
                                 },
                             },

                             "discount": 0.9,
                             "peaks": {
                                 "sz": 12,
                                 "max_win": 100
                             },

                             "mode": {
                                 "sz": 12
                             },

                             "print": 0,
                             "plot": 0,
                             "log_dir": "D:/Forge/Forge/jupyter/formscore-log/",
                             }


    score_object1 = get_score(workoutData1,h_params,header)
    score_object1 = score_object1['scores']
    agg_power1 = score_object1["agg power"]
    stamina1 = score_object1["stamina"]
    formscore1 = score_object1["formscore"]
#     total_time1 = score_object1['total time']
    
    score_object2 = get_score(workoutData2,h_params,header)
    score_object2 = score_object2['scores']
    agg_power2 = score_object2["agg power"]
    stamina2 = score_object2["stamina"]
    formscore2 = score_object2["formscore"]
#     total_time2 = score_object2['total time']


# In[ ]:


st.subheader("Scores")
st.write("Scores Corresponding to Base Signal")
col1, col2, col3 = st.columns(3)

with col1:

    st.write("AGGREGATE POWER SCORES")
    st.write("Explosiveness Score: " + str(round(agg_power1['subScores']['explosiveness']['score'],2)))
    st.write("Explosiveness Coaching Tip: " + str(agg_power1['subScores']['explosiveness']['coachingTip']))
    st.write("Power Score: " + str(round(agg_power1['subScores']['power']['score'],2)))
    st.write("Power Coaching Tip: " + str(agg_power1['subScores']['power']['coachingTip']))
    st.write("Net Score: " + str(round(agg_power1['score'],2)))
    st.write("Net Coaching Tip: " + str(agg_power1['coachingTip']))

with col2:

    st.write("STAMINA SCORES")
#         st.write("Total Time Score: " + str(round(total_time1['score'],2)))
#         st.write("Total Time Coaching Tip: " + str(total_time1['coachingTip']))
    st.write("Area Stamina Score: " + str(round(stamina1['subScores']['area stamina']['score'],2)))
    st.write("Area Stamina Coaching Tip: " + str(stamina1['subScores']['area stamina']['coachingTip']))
    st.write("Net Score: " + str(round(stamina1['score'],2)))
    st.write("Net Coaching Tip: " + str(stamina1['coachingTip']))

with col3:
    
    st.write("FORM SCORES")
    st.write("Sudden Release Score: " + str(round(formscore1['subScores']['sudden release']['score'],2)))
    st.write("Sudden Release Coaching Tip: " + str(formscore1['subScores']['sudden release']['coachingTip']))
    st.write("Tempo Score: " + str(round(formscore1['subScores']['tempo']['score'],2)))
    st.write("Tempo Coaching Tip: " + str(formscore1['subScores']['tempo']['coachingTip']))
    st.write("Jitter Score: " + str(round(formscore1['subScores']['jitter']['score'],2)))
    st.write("Jitter Coaching Tip: " + str(formscore1['subScores']['jitter']['coachingTip']))
    st.write("Net Score: " + str(round(formscore1['score'],2)))
    st.write("Net Coaching Tip: " + str(formscore1['coachingTip']))

st.write("Scores Corresponding to Signal " + str(signal_b))
col4, col5, col6 = st.columns(3)

with col4:

    st.write("AGGREGATE POWER SCORES")
    st.write("Explosiveness Score: " + str(round(agg_power2['subScores']['explosiveness']['score'],2)))
    st.write("Explosiveness Coaching Tip: " + str(agg_power2['subScores']['explosiveness']['coachingTip']))
    st.write("Power Score: " + str(round(agg_power2['subScores']['power']['score'],2)))
    st.write("Power Coaching Tip: " + str(agg_power2['subScores']['power']['coachingTip']))
    st.write("Net Score: " + str(round(agg_power2['score'],2)))
    st.write("Net Coaching Tip: " + str(agg_power2['coachingTip']))

with col5:

    st.write("STAMINA SCORES")
#         st.write("Total Time Score: " + str(round(total_time2['score'],2)))
#         st.write("Total Time Coaching Tip: " + str(total_time2['coachingTip']))
    st.write("Area Stamina Score: " + str(round(stamina2['subScores']['area stamina']['score'],2)))
    st.write("Area Stamina Coaching Tip: " + str(stamina2['subScores']['area stamina']['coachingTip']))
    st.write("Net Score: " + str(round(stamina2['score'],2)))
    st.write("Net Coaching Tip: " + str(stamina2['coachingTip']))

with col6:
    
    st.write("FORM SCORES")
    st.write("Sudden Release Score: " + str(round(formscore2['subScores']['sudden release']['score'],2)))
    st.write("Sudden Release Coaching Tip: " + str(formscore2['subScores']['sudden release']['coachingTip']))
    st.write("Tempo Score: " + str(round(formscore2['subScores']['tempo']['score'],2)))
    st.write("Tempo Coaching Tip: " + str(formscore2['subScores']['tempo']['coachingTip']))
    st.write("Jitter Score: " + str(round(formscore2['subScores']['jitter']['score'],2)))
    st.write("Jitter Coaching Tip: " + str(formscore2['subScores']['jitter']['coachingTip']))
    st.write("Net Score: " + str(round(formscore2['score'],2)))
    st.write("Net Coaching Tip: " + str(formscore2['coachingTip']))

st.subheader("Meta Values: Set to " + str(meta_tag))

if meta_tag == "True":
    
    st.write("Meta Scores Corresponding to Base Signal")
    col7, col8, col9 = st.columns(3)
    
    with col7:

        st.write("AGGREGATE POWER META VALUES")
        st.write("A. Explosiveness ")
        st.write("Base/Mode: " + str(round(agg_power1['subScores']['explosiveness']['meta']['base/mode'],2)))
        st.write("Average Ascent: " + str(round(agg_power1['subScores']['explosiveness']['meta']['average ascent'],2)))
        st.write("Peak Value Used: " + str(round(agg_power1['subScores']['explosiveness']['meta']['peak value used'],2)))

        st.write("B. Power")
        st.write("Power: " + str(round(agg_power1['subScores']['power']['meta']['power'],2)))
        st.write("Power Reference From History: " + str(round(agg_power1['subScores']['power']['meta']['powerReferenceFromHistory'],2)))

    with col8:

        st.write("STAMINA META VALUES")
#             st.write("A. Time ")
#             st.write("Start/End: " + str(total_time1['meta']['start,end']))
#             st.write("Low Filter: " + str(round(total_time1['meta']['low_filter'],2)))
        st.write("A. Stamina")
        st.write("Total Power/Area: " + str(round(stamina1['subScores']['area stamina']['meta']['total power/area'],2)))
        st.write("Length: " + str(round(stamina1['subScores']['area stamina']['meta']['length'],2)))
        st.write("Ideal Power/Reference x Length: " + str(round(stamina1['subScores']['area stamina']['meta']['ideal power/reference x length'],2)))

    with col9:
        st.write("FORM META VALUES")
        st.write("A. Sudden Release")
        st.write("Max To Fall Ratio: " + str(round(formscore1['subScores']['sudden release']['meta']['max_to_fall_ratio'],2)))
        st.write("Fall Time: " + str(round(formscore1['subScores']['sudden release']['meta']['fall_time'],2)))
        st.write("Points: " + str(formscore1['subScores']['sudden release']['meta']['points']))
        st.write("B. Tempo")
        st.write("Peaks: " + str(formscore1['subScores']['tempo']['meta']['peaks']))
        st.write("Current Tempo: " + str(formscore1['subScores']['tempo']['meta']['curr_tempo']))
        st.write("Average: " + str(round(formscore1['subScores']['tempo']['meta']['avg'],2)))
        st.write("Current Score: " + str(round(formscore1['subScores']['tempo']['meta']['currScore'],2)))
        st.write("C. Jitter")
        st.write("Per Rep Jitter Dictionary: " + str(formscore1['subScores']['jitter']['meta']['per rep jitter dictionary']))
        
    st.write("Meta Scores Corresponding to Signal " + str(signal_b))
    col10, col11, col12 = st.columns(3)
    
    with col10:

        st.write("AGGREGATE POWER META VALUES")
        st.write("A. Explosiveness ")
        st.write("Base/Mode: " + str(round(agg_power2['subScores']['explosiveness']['meta']['base/mode'],2)))
        st.write("Average Ascent: " + str(round(agg_power2['subScores']['explosiveness']['meta']['average ascent'],2)))
        st.write("Peak Value Used: " + str(round(agg_power2['subScores']['explosiveness']['meta']['peak value used'],2)))

        st.write("B. Power")
        st.write("Power: " + str(round(agg_power2['subScores']['power']['meta']['power'],2)))
        st.write("Power Reference From History: " + str(round(agg_power2['subScores']['power']['meta']['powerReferenceFromHistory'],2)))

    with col11:

        st.write("STAMINA META VALUES")
#             st.write("A. Time ")
#             st.write("Start/End: " + str(total_time2['meta']['start,end']))
#             st.write("Low Filter: " + str(round(total_time2['meta']['low_filter'],2)))
        st.write("A. Stamina ")
        st.write("Total Power/Area: " + str(round(stamina2['subScores']['area stamina']['meta']['total power/area'],2)))
        st.write("Length: " + str(round(stamina2['subScores']['area stamina']['meta']['length'],2)))
        st.write("Ideal Power/Reference x Length: " + str(round(stamina2['subScores']['area stamina']['meta']['ideal power/reference x length'],2)))
    
    with col12:
        st.write("FORM META VALUES")
        st.write("A. Sudden Release")
        st.write("Max To Fall Ratio: " + str(round(formscore2['subScores']['sudden release']['meta']['max_to_fall_ratio'],2)))
        st.write("Fall Time: " + str(round(formscore2['subScores']['sudden release']['meta']['fall_time'],2)))
        st.write("Points: " + str(formscore2['subScores']['sudden release']['meta']['points']))
        st.write("B. Tempo")
        st.write("Peaks: " + str(formscore2['subScores']['tempo']['meta']['peaks']))
        st.write("Current Tempo: " + str(formscore2['subScores']['tempo']['meta']['curr_tempo']))
        st.write("Average: " + str(round(formscore2['subScores']['tempo']['meta']['avg'],2)))
        st.write("Current Score: " + str(round(formscore2['subScores']['tempo']['meta']['currScore'],2)))
        st.write("C. Jitter")
        st.write("Per Rep Jitter Dictionary: " + str(formscore2['subScores']['jitter']['meta']['per rep jitter dictionary']))


cred = {
"type": st.secrets["type_s"],
"project_id": st.secrets["project_id_s"],
"private_key_id": st.secrets["private_key_id_s"],
"private_key": st.secrets["private_key_s"],
"client_email": st.secrets["client_email_s"],
"client_id": st.secrets["client_id_s"],
"auth_uri": st.secrets["auth_uri_s"],
"token_uri": st.secrets["token_uri_s"],
"auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url_s"],
"client_x509_cert_url": st.secrets["client_x509_cert_url_s"]}

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
           "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred, scope)

client = gspread.authorize(credentials)
# Open the spreadhseet
sheet_fd = client.open("DFIA").worksheet("Linear_Transform")

st.subheader("Linear Adjustment")

param_fields = ["explosiveness","power","Net Power Score","Area Stamina Score","Net Stamina Score","sudden release","tempo","jitter"]
check_parameter = st.selectbox('Choose Parameter',param_fields,key="c_param") # X 
check_parameter = str(check_parameter)

if (check_parameter == "explosiveness" or check_parameter == "power"):     
    signal_1_val = round(agg_power1['subScores'][check_parameter]['score'],2)
    signal_2_val = round(agg_power2['subScores'][check_parameter]['score'],2)

elif check_parameter == "Net Power Score": 

    signal_1_val = round(agg_power1['score'],2)
    signal_2_val = round(agg_power2['score'],2)

elif check_parameter == "Area Stamina Score": 

    signal_1_val = round(stamina1['subScores']['area stamina']['score'],2)
    signal_2_val = round(stamina2['subScores']['area stamina']['score'],2)

elif check_parameter == "Net Stamina Score": 

    signal_1_val = round(stamina1['score'],2)
    signal_2_val = round(stamina2['score'],2)

else: 
    signal_1_val = round(formscore1['subScores'][check_parameter]['score'],2)
    signal_2_val = round(formscore2['subScores'][check_parameter]['score'],2)

st.write("Score for " + check_parameter + " corresponding to Base Signal is: " + str(signal_1_val) + " (X1)")
st.write("Score for " + check_parameter + " corresponding to " + signal_b + " is: " + str(signal_2_val) + " (X2)")
y_1_input = st.number_input('Insert Score Value for Signal(Y1) For Base Signal', key="y1_input")
y_2_input = st.number_input('Insert Score Value for Signal(Y2) ' + str(signal_b), key="y2_input")

if st.button("Find A and B"):

    if signal_1_val == signal_2_val:
        st.write("Score Value for the both the signal are same! (X1=X2)")
    else:
        A = round((y_1_input - y_2_input)/(signal_1_val - signal_2_val),2)
        B = round(((y_1_input*signal_2_val) - (y_2_input*signal_1_val))/(signal_2_val - signal_1_val),2)

        if A < 0:
            st.write("A is less than 0")
        else:
            st.write("Value of A is: " + str(A))
            st.write("Value of B is: " + str(B))
            sheet_fd.append_row(["Base Signal",signal_b,check_parameter,y_1_input,y_2_input,signal_1_val,signal_2_val,A,B],value_input_option="USER_ENTERED")
            st.write("Values are stored!")    
