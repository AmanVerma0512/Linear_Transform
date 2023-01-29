#!/usr/bin/env python
# coding: utf-8

# In[28]:


import json
import matplotlib.pyplot as plt
import numpy as np
from Updated_Scores import get_score
import pandas as pd
import yaml
import boto3
import streamlit as st
import gspread

st.set_page_config(layout="wide")
st.title("Signal Comparison")


# In[29]:


s3_client = boto3.client('s3')
s3_bucket_name = 'forgefait'
s3 = boto3.resource('s3',
                     aws_access_key_id = 'AKIATEQDTHIB3HXL546P',
                     aws_secret_access_key = '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')

@st.experimental_singleton
def load_data():
    print('Object Initialised')
    content_object = s3.Object('forgefait', 'fabricated_signals.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    print('File Read')

    data = yaml.safe_load(file_content)
    print('File Converted to JSON')
    return data

data = load_data()


# In[30]:


name_fields_array = []

for idx, elem in enumerate(data):
    name_fields_array.append(elem['user_id'])


# In[31]:


signal_dict = st.selectbox('Choose the ID you want to compare signals for?', name_fields_array, key="comp_signals")


# In[32]:


curr_elem_idx = 0
flag = False
for idx, elem in enumerate(data):
    if elem['user_id'] == signal_dict:
        curr_elem_idx = idx
        flag = True


# In[33]:


signal_vals = data[curr_elem_idx]['signals']


# In[34]:


signal_fields = list(signal_vals.keys())


# In[35]:


signal_a = st.selectbox('Choose First Signal',signal_fields,key="s_a")
signal_b = st.selectbox('Choose Second Signal',signal_fields,key="s_b")
meta_tag = st.selectbox("Display Meta Values?",["False","True"],key="meta_tag")

if flag == True:
    st.header("Signal Plots and Scores")
    x1 = signal_vals[signal_a]
    workoutData1 = list(map(float, x1))
    x2 = signal_vals[signal_b]
    workoutData2 = list(map(float, x2))

    st.subheader("Plots")
    st.write("Plot Corresponding to Signal " + str(signal_a))
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

    st.subheader("Scores")
    st.write("Scores Corresponding to Signal " + str(signal_a))
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
        
        st.write("Meta Scores Corresponding to Signal " + str(signal_a))
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
    
    st.write("Score for " + check_parameter + " corresponding to " + signal_a + " is: " + str(signal_1_val) + " (X1)")
    st.write("Score for " + check_parameter + " corresponding to " + signal_b + " is: " + str(signal_2_val) + " (X2)")
    y_1_input = st.number_input('Insert Score Value for Signal(Y1) ' + str(signal_a), key="y1_input")
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