from streamlit_extras.app_logo import add_logo
from st_pages import Page, show_pages, add_page_title

def logo():
    add_logo("uploads/grt-health.png", height=300)

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("step1.py", "Enter your details", "🏠"),
        Page("pages/step2.py", "Create Me", "🧑‍🍳"),
        Page("pages/step3.py", "Chat With Me", "🤖")
    ]
)