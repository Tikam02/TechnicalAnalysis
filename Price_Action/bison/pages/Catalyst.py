import streamlit as st
import pandas as pd
import datetime

# Function to save blog post data
def save_blog_post(date, tags, events, affected_sectors, event_details, stocks_gap, images):
    # Assuming you want to save the data to a CSV file
    # You can modify this function to save the data in any format you prefer
    blog_data = {
        'date': [date],  # Change 'Date' to 'date' to match the key
        'Tags': [tags],
        'Events': [events],
        'Affected Sectors': [affected_sectors],
        'Event Details': [event_details],
        'Stocks Gap': [stocks_gap],
        'Images': [images] # This will need to be handled differently, as images are files
    }
    df = pd.DataFrame(blog_data)
    # Save the DataFrame to a CSV file
    # Note: Handling images in a CSV file is complex and not recommended. Consider saving images separately.
    df.to_csv('blog_posts.csv', mode='a', header=False, index=False)


# Streamlit page layout
st.title('Catalyst Blog Post Creator')

# Collect user inputs
date = st.date_input('Select Date')
tags = st.text_input('Enter Cataylst Tags (comma-separated)')
events = st.text_area('Enter Catalyst Events (comma-separated)')
affected_sectors = st.text_input('Enter Affected Sectors or Stocks')
event_details = st.text_area('Enter Catalyst Events Details')
stocks_gap = st.text_input('Enter Stocks Gap-Up / Gap-Down (comma-separated)')
images = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Button to submit the blog post
if st.button('Submit Blog Post'):
    # Save the blog post data
    save_blog_post(date, tags, events, affected_sectors, event_details, stocks_gap, images)
    st.success('Blog post submitted successfully.')

# Display existing blog posts
if st.button('Show Blog Posts'):
    try:
        df = pd.read_csv('blog_posts.csv')
        for index, row in df.iterrows():
            with st.expander(f"{row['Date']} - {row['Tags']}"):
                st.write(f"**Events:** {row['Events']}")
                st.write(f"**Affected Sectors:** {row['Affected Sectors']}")
                st.write(f"**Event Details:** {row['Event Details']}")
                st.write(f"**Stocks Gap:** {row['Stocks Gap']}")
                # Display images if they were uploaded
                if row['Images']:
                    for image in row['Images'].split(','):
                        st.image(image, caption=image.name)
    except FileNotFoundError:
        st.warning('No blog posts found.')
