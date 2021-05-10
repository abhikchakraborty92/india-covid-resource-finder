import streamlit as st
from data import searchresources

st.set_page_config(page_title='COVID19 India Resources',layout='wide')

def generatetweetlayout(name,tweet,created_at,url):
    tweet = st.beta_container()
    with tweet:
        st.markdown(f'**Author:** _{name}_ | **Tweet Date:** _{created_at}_')
        st.write(tweet)
        st.markdown(f'''<a href={url}>Read Original Tweet...</a> <br>''',unsafe_allow_html=True)

st.markdown('<center> <h1 style="font-size:69px; color:#89d2dc;"> COVID19 INDIA RESOURCES </h1> </center>',unsafe_allow_html=True)
st.markdown('<center> <h3> Latest and verified resources fetched from different twitter feeds and streams </h3> </center>',unsafe_allow_html=True)
st.markdown('<br>',unsafe_allow_html=True)
st.markdown('<br> <br>',unsafe_allow_html=True)

options = st.beta_columns(3)

with options[0]:
    resource = st.selectbox('Please select the resource you are looking for',options=['Oxygen','Plasma','Ambulance','Beds','Ventilator','ICUBeds','Remdesivir'])

with options[1]:
    place = st.text_input('Enter the city name where you are looking for the resource')

with options[2]:
    hours = st.number_input('What should be the maximum age of the search result (in hours)',min_value=2,max_value=144,value=36,step=1,help='Decreasing this value would produce latest leads. However, if leads are not available within the selected hours, increasing the number will fetch older leads.')


search = st.button('Search')

if search:
    with st.spinner('Fetching results. This might take a few moments...'):
        data = searchresources(resource,place,hours)
        st.markdown('<center> <h1> RESULTS </h1> <br> </center>',unsafe_allow_html=True)
        
        if len(data)>0:
            st.markdown(f'<center> <h3 style="color:#6DF5B8;"> SUCCESS! Showing {len(data)} results... </h3> <br> </center>',unsafe_allow_html=True)
            st.markdown(f'<center> <h5 style="color:#FF5F6F;"> NOTE: While the engine tries to provide the most relevant leads, some leads might be outside the preferred location to provide the user with all possible options  </h5> <br> </center>',unsafe_allow_html=True)
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
            
    