import streamlit as st
import sqlite3 as sq
st.title("🏠 FUTA Homes")
st.caption("Find verified hostels around campus — fast, safe, and stress-free.")
st.warning("⚠️ Always inspect house physically before making payment.")

# ------------------ PAGE CONFIG ------------------
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)

st.set_page_config(page_title="FUTA Housing", layout="wide")

st.sidebar.title("🔐 Login")

role = st.sidebar.selectbox("Login as", ["Student", "Agent"])


password = st.sidebar.text_input("Enter Password", type="password")


if role == "Agent" and password != "admin123":
    st.warning("Wrong password for Agent")
    st.stop()

    
    
    
# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
}
.card {
    padding: 15px;
    border-radius: 20px;
    background-color: white;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
h1, h2, h3 {
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ------------------ DATABASE ------------------

con = sq.connect('houses.db')
c = con.cursor()
if st.button("View Database"):
    c.execute('SELECT * FROM houses')
    data = c.fetchall()
    st.write(data)

if st.button("Clear All Houses"):
    c.execute("DROP TABLE houses")
    con.commit()
    st.success("All houses deleted!")

c.execute('''
CREATE TABLE IF NOT EXISTS houses(
    area TEXT,
    price INTEGER,
    distance TEXT,
    image TEXT,
    video TEXT,
    contact TEXT
)
''')
con.commit()


# ------------------ SIDEBAR ------------------
st.sidebar.title("🏠 FUTA Housing")
page = st.sidebar.radio("Navigate", ["Home", "Search", "Post House"])

# ------------------ HOME ------------------
st.info("⚠️ Only contact verified agents. Always inspect house before payment.")
if page == "Home":
    st.markdown('<div class="title">Find Your Perfect Hostel 🏠</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Affordable housing around FUTA</div>', unsafe_allow_html=True)

    st.image("https://images.unsplash.com/photo-1560185127-6ed189bf02f4")

# ------------------ SEARCH ------------------
elif page == "Search":
    st.header("🔍 Search Houses")
    col1, col2 = st.columns(2)

    with col1:
        area = st.selectbox("Area", ["North Gate", "South Gate", "West Gate", "Ipinsa", "Roadblock"])
    
    with col2:
        price = st.number_input("Max Price (₦)", min_value=0)

    if st.button("Search"):
        c.execute('SELECT * FROM houses')
        houses = c.fetchall()

        results = []
        

        for house in houses:
            if house[0] == area and house[1] <= price:
                results.append(house)

        if results:
            st.success(f"{len(results)} house(s) found 🎉")

        cols = st.columns(2)  # 2 cards per row

        for i, house in enumerate(results):
            with cols[i % 2]:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.image(house[3], use_container_width=True)
                st.subheader(f"{house[0]} - ₦{house[1]}")
                st.write(f"🚶 {house[2]}")

                st.markdown(f"📞 {house[5]}")
                st.markdown(f"[💬 Chat on WhatsApp](https://wa.me/{house[5]})")

                if house[4]:  # only show video if exists
                    st.video(house[4])

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.warning("No houses found 😢 Try increasing your budget")

# ------------------ POST HOUSE ------------------

elif page == "Post House":
    st.header("🏘️ Post a House")
    

    area_input = st.selectbox("Area", ["North Gate", "South Gate", "West Gate", "Ipinsa", "Roadblock"])
    price_input = st.number_input("Price", min_value=0)
    distance_input = st.text_input("Distance")
    video_input = st.text_input("Video Link")
    contact_input = st.text_input("Contact")
    image_input = st.text_input("House Image URL")
    
    
    

    if st.button("Add House"):
        c.execute(
            'INSERT INTO houses VALUES (?, ?, ?, ?, ?, ?)',
            (area_input, price_input, distance_input,image_input, video_input,contact_input)
        )
        con.commit()
        st.success("✅ House Added Successfully!")
    
        
