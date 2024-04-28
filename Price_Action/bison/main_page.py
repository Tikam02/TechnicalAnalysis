import streamlit as st

# Add a title to your app
st.markdown("<h1 style='text-align: center; color: black;'>BISON</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Calm In The Storm</h2>", unsafe_allow_html=True)



# Display the two images side by side
col1, col2 = st.columns(2)

# Add your logo with increased height and width using CSS styling
with col1:
    st.markdown(
        '<style> img {max-width: 100%; height: auto;} </style>', 
        unsafe_allow_html=True
    )
    st.image("./img/logo-03.jpg")

with col2:
    st.markdown(
        '<style> img {max-width: 100%; height: auto;} </style>', 
        unsafe_allow_html=True
    )
    st.image("./img/logo.jpg")



# # Display the text in a box
# st.text_area("", """
# This symbolism of the majestic Bison heading directly into the storm is very fitting and an interesting reminder of how to confront life’s obstacles. 
# We all know that the worst thing we can do when confronted with a major challenge in life is to run from it.
# """)