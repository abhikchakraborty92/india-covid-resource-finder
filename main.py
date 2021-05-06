import streamlit as st
from data import searchresources

st.set_page_config(page_title='COVID19 India Resources',layout='wide')

def generatetweetlayout(name,tweet,created_at,url):
    tweet = st.beta_container()
    with tweet:
        st.markdown(f'**Author:** _{name}_ | **Tweet Date:** _{created_at}_')
        st.write(tweet)
        st.markdown(f'''<a href={url}>Read Original Tweet...</a> <br>''',unsafe_allow_html=True)

st.markdown('<center> <h1> COVID19 INDIA RESOURCES </h1> </center>',unsafe_allow_html=True)
st.markdown('<center> <h4> Latest and verified resources fetched from different twitter feeds and streams </h4> </center>',unsafe_allow_html=True)
st.markdown('<br> <br>',unsafe_allow_html=True)

options = st.beta_columns(3)

with options[0]:
    resource = st.selectbox('Please select the resource you are looking for',options=['Oxygen','Plasma','Ambulance','Beds','Ventilator','ICU','Remdesivir'])

with options[1]:
    place = st.text_input('Enter the city name where you are looking for the resource')

with options[2]:
    hours = st.number_input('What should be the maximum age of a tweet (in hours)',min_value=2,max_value=100,value=24,step=1,help='Number of hours from the current time from when the tweets have to be fetched. Increasing the number will fetch older tweets.')

# buttons = st.beta_columns(3)

# with buttons[2]:
    
search = st.button('Search')

if search:
    data = searchresources(resource,place,hours)
    st.markdown('<center> <h1> RESULTS </h1> <br> </center>',unsafe_allow_html=True)
    if len(data)>0:
        for row,index in data.iterrows():
            
            tweet = st.beta_container()
            with tweet:
                st.markdown(f"**Author:** _{data['name'][row]}_ | **Tweet Date:** _{data['created_at'][row]}_")
                st.markdown(f"{data['text'][row]}")
                st.markdown(f'''<a href={data['tweeturl'][row]} target="_blank">Read Original Tweet...</a>
                ''',unsafe_allow_html=True)
                st.markdown('<hr>',unsafe_allow_html=True)
    else:
        st.markdown('<center> <h3> Sorry. No resources found for now! Please call National Corona Helpline 1075 </h3> </center>',unsafe_allow_html=True)
    