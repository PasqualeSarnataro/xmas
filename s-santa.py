import streamlit as st
import random
import pandas as pd

def generate_secret_santa(participants):
    names = list(participants.keys())
    shuffled = names[:]
    random.shuffle(shuffled)

    # Ensure no one gets themselves
    while any(names[i] == shuffled[i] for i in range(len(names))):
        random.shuffle(shuffled)

    return {giver: receiver for giver, receiver in zip(names, shuffled)}

st.title("🎅 Secret Santa App")
st.write("Organize your Secret Santa draw with ease!")

# Step 1: Input participant details
st.header("Step 1: Add Participants")
with st.form(key="participant_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    add_button = st.form_submit_button("Add Participant")

    # Store participants in session state
    if "participants" not in st.session_state:
        st.session_state["participants"] = {}

    if add_button and name and email:
        st.session_state["participants"][name] = email
        st.success(f"Added {name} with email {email}!")

# Display participants
if st.session_state.get("participants"):
    st.header("Participants")
    df = pd.DataFrame(st.session_state["participants"].items(), columns=["Name", "Email"])
    st.table(df)

# Step 2: Generate Secret Santa pairs
if st.session_state.get("participants"):
    st.header("Step 2: Generate Secret Santa Pairs")
    if st.button("Generate Pairs"):
        pairs = generate_secret_santa(st.session_state["participants"])
        st.session_state["pairs"] = pairs
        st.success("Secret Santa pairs generated! Scroll down to see them.")

# Step 3: Display Secret Santa assignments
if st.session_state.get("pairs"):
    st.header("Step 3: View Your Secret Santa Assignment")
    st.write("Each participant can check who they are gifting to by selecting their name below.")

    selected_name = st.selectbox("Select your name", list(st.session_state["pairs"].keys()))
    if selected_name:
        receiver = st.session_state["pairs"][selected_name]
        st.info(f"🎁 {selected_name}, you are gifting to **{receiver}**!")

    # Display the full list of pairings
    st.write("Or view the full list of pairings below:")
    if st.checkbox("Show full list of pairings"):
        full_list = [{"Giver": giver, "Receiver": receiver} for giver, receiver in st.session_state["pairs"].items()]
        full_df = pd.DataFrame(full_list)
        st.table(full_df)

# Reset app
if st.button("Reset App"):
    st.session_state.clear()
    st.success("App has been reset!")
