import streamlit as st
import sqlite3 as sq
from pathlib import Path

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="FUTA Housing", layout="wide")

# ------------------ DATABASE ------------------
con = sq.connect('houses.db', check_same_thread=False)
c = con.cursor()

# Houses table
c.execute('''
CREATE TABLE IF NOT EXISTS houses(
    area TEXT,
    price INTEGER,
    distance TEXT,
    image_paths TEXT,  -- comma-separated local paths
    video_path TEXT,
    contact TEXT
)
''')

# Submissions table
c.execute('''
CREATE TABLE IF NOT EXISTS submissions(
    area TEXT,
    price INTEGER,
    distance TEXT,
    image_paths TEXT,
    video_path TEXT,
    contact TEXT
)
''')
con.commit()

# ------------------ SIDEBAR ------------------
st.sidebar.title("🏠 FUTA Housing")
role = st.sidebar.selectbox("Login as", ["Student", "Agent", "Admin"])

# Admin password
if role == "Admin":
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password != "admin123":
        st.warning("Wrong admin password!")
        st.stop()

page = st.sidebar.radio("Navigate", ["Home", "Search", "Post House"])

# ------------------ HOME ------------------
if page == "Home":
    st.markdown('<h1 style="text-align:center">Find Your Perfect Hostel 🏠</h1>', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1560185127-6ed189bf02f4", use_column_width=True)

# ------------------ SEARCH ------------------
elif page == "Search":
    st.header("🔍 Search Houses")
    area = st.selectbox("Area", ["North Gate", "South Gate", "West Gate", "Ipinsa", "Roadblock"])
    price = st.number_input("Max Price (₦)", min_value=0)

    if st.button("Search"):
        c.execute("SELECT * FROM houses")
        houses = c.fetchall()
        results = [h for h in houses if h[0] == area and h[1] <= price]

        if results:
            st.success(f"{len(results)} house(s) found 🎉")
            for house in results:
                with st.container():
                    col1, col2 = st.columns([1,2])
                    with col1:
                        for img_path in house[3].split(","):
                            st.image(img_path)
                    with col2:
                        st.subheader(f"{house[0]} - ₦{house[1]}")
                        st.write(f"🚶 Distance: {house[2]}")
                        st.markdown(f"📞 Contact: {house[5]}")
                        if house[4]:
                            st.video(house[4])
        else:
            st.warning("No houses found 😢 Try increasing your budget")

# ------------------ POST HOUSE ------------------
elif page == "Post House":
    st.header("🏘️ Submit a House")
    area_input = st.selectbox("Area", ["North Gate", "South Gate", "West Gate", "Ipinsa", "Roadblock"])
    price_input = st.number_input("Price", min_value=0)
    distance_input = st.text_input("Distance")
    contact_input = st.text_input("Contact")

    # Upload multiple images
    uploaded_images = st.file_uploader("Upload Images", type=["png","jpg","jpeg"], accept_multiple_files=True)
    uploaded_video = st.file_uploader("Upload Video (optional)", type=["mp4","mov","avi"])

    if st.button("Submit House"):
        # Save uploaded files locally
        images_paths = []
        for img in uploaded_images:
            img_path = f"uploads/{img.name}"
            Path("uploads").mkdir(parents=True, exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(img.getbuffer())
            images_paths.append(img_path)

        video_path = ""
        if uploaded_video:
            video_path = f"uploads/{uploaded_video.name}"
            with open(video_path, "wb") as f:
                f.write(uploaded_video.getbuffer())

        # Save to submissions if Agent, directly if Admin
        if role == "Agent":
            c.execute(
                "INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?)",
                (area_input, price_input, distance_input, ",".join(images_paths), video_path, contact_input)
            )
            st.success("✅ House submitted! Admin will approve it.")
        elif role == "Admin":
            c.execute(
                "INSERT INTO houses VALUES (?, ?, ?, ?, ?, ?)",
                (area_input, price_input, distance_input, ",".join(images_paths), video_path, contact_input)
            )
            st.success("✅ House added directly!")
        con.commit()
