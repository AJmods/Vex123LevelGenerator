import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import os

from PIL import Image
from fontTools.tfmLib import MATHSY

from levelGen import find_paths

# code to hide the watermark using CSS

# #MainMenu to hide the burger menu at the top-right side
# footer to hide the ```made with streamlit``` mark
hide = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide, unsafe_allow_html=True)

# --- KEEP YOUR find_paths FUNCTION HERE ---

def draw_paths_streamlit(A, paths, level_folder):

    fig, ax = plt.subplots(figsize=(A, A))

    # 1. Background Texture
    if os.path.exists('images/Vex123Sqaure.png'):
        from PIL import Image
        bg_img = Image.open('images/Vex123Sqaure.png').convert('RGB')
        for r in range(A):
            for c in range(A):
                ax.imshow(bg_img, extent=(c - 0.5, c + 0.5, r + 0.5, r - 0.5))

    if not paths:
        return fig

    path = random.choice(paths)
    base_path = f"images/{level_folder}"

    # 2. Load Start and End
    img_start = Image.open(f"{base_path}/start.png")
    img_end = Image.open(f"{base_path}/end.png")

    # 3. Load all available turn images into a list
    # This looks for turn1.png, turn2.png, etc.
    turn_images = []
    i = 1
    while os.path.exists(f"{base_path}/turn{i}.png"):
        turn_images.append(Image.open(f"{base_path}/turn{i}.png"))
        i += 1

    # If no turn images found, use a fallback or skip
    if not turn_images:
        st.error(f"No turn images (turn1.png, etc.) found in {base_path}")
        return fig

    # 4. Place images on the grid
    turn_count = 0
    for i, (r, c) in enumerate(path):
        current_img = None

        if i == 0:
            current_img = img_start
        elif i == len(path) - 1:
            current_img = img_end
        else:
            # Check for a turn
            prev_r, prev_c = path[i - 1]
            next_r, next_c = path[i + 1]

            # If the direction changed...
            if (r - prev_r != next_r - r) or (c - prev_c != next_c - c):
                # Use modulo (%) to cycle through turn_images
                current_img = turn_images[turn_count % len(turn_images)]
                turn_count += 1

        # if current_img:
        #         #     # extent=(left, right, bottom, top)
        #         #     ax.imshow(current_img, extent=(c - 0.4, c + 0.4, r + 0.4, r - 0.4), zorder=5)
        # Inside your loop where you place images:
        if current_img:
            # Full cell width: from (center - 0.5) to (center + 0.5)
            ax.imshow(
                current_img,
                extent=(c - 0.5, c + 0.5, r + 0.5, r - 0.5),  # Full square
                zorder=5
            )

    ax.set_xlim(-0.5, A - 0.5)
    ax.set_ylim(A - 0.5, -0.5)
    ax.set_axis_off()  # Cleaner look for kids
    return fig


import random


def get_random_edge_point(A):
    # A-1 is the maximum index
    limit = A - 1

    # 1. Pick a random index along the span (0 to limit)
    pos = random.randint(0, limit)

    # 2. Pick which of the 4 boundaries to place the point on
    # 0: Top, 1: Bottom, 2: Left, 3: Right
    side = random.randint(0, 3)

    if side == 0:  # Top Edge (row 0, any column)
        return 0, pos
    elif side == 1:  # Bottom Edge (row limit, any column)
        return limit, pos
    elif side == 2:  # Left Edge (any row, col 0)
        return pos, 0
    else:  # Right Edge (any row, col limit)
        return pos, limit

# --- STREAMLIT UI ---
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import os

# --- [KEEP YOUR find_paths AND draw_paths_streamlit FUNCTIONS HERE] ---

st.set_page_config(page_title="VEX 123 Level Gen", layout="wide")
st.title("VEX 123 Level Generator")

# Initialize session state for the custom menu
if 'show_custom' not in st.session_state:
    st.session_state.show_custom = False

# 1. Define the Level Settings
levels = {
    "Level 1": {"level":"level1", "A": 6, "turns": 1, "min_len": 3, "max_len": 4, "min_straight_length": 1},
    "Level 2": {"level":"level2", "A": 6, "turns": 2, "min_len": 6, "max_len": 7, "min_straight_length": 2},
    "Level 3": {"level":"level3", "A": 6, "turns": 3, "min_len": 7, "max_len": 9, "min_straight_length": 1},
}

# 2. Create the 4-Button Layout
col1, col2, col3, col4 = st.columns(4)
selected_config = None

with col1:
    if st.button("Level 1 🟢", use_container_width=True):
        selected_config = levels["Level 1"]
        st.session_state.show_custom = False

with col2:
    if st.button("Level 2 🟡", use_container_width=True):
        selected_config = levels["Level 2"]
        st.session_state.show_custom = False

with col3:
    if st.button("Level 3 🔴", use_container_width=True):
        selected_config = levels["Level 3"]
        st.session_state.show_custom = False

with col4:
    if st.button("Custom ⚙️", use_container_width=True):
        st.session_state.show_custom = not st.session_state.show_custom

# 3. The Custom Menu (Only shows if Custom button was clicked)
if st.session_state.show_custom:
    st.markdown("---")
    st.subheader("Custom Level Settings")
    c_col1, c_col2, c_col3 = st.columns(3)

    with c_col1:
        c_a = st.slider("Field Size", 4, 12, 6)
    with c_col2:
        c_t = st.slider("Turns", 1, 6, 2)
    with c_col3:
        c_l = st.slider("Min Length", 2, 15, 4)

    if st.button("Generate Custom Map 🚀", type="primary", use_container_width=True):
        selected_config = {"level":"level3", "A": c_a, "turns": c_t, "min_len": c_l, "max_len": c_l + 10, "min_straight_length":1}

# 4. Logic & Display
if selected_config:
    st.markdown("---")
    try:
        results = find_paths(
            A=selected_config["A"],
            start=get_random_edge_point(selected_config["A"]),
            required_turns=selected_config["turns"],
            min_length=selected_config["min_len"],
            max_length=selected_config["max_len"],
            allow_crossing=False,
            min_straight_length=selected_config["min_straight_length"]
        )

        if results:
            fig = draw_paths_streamlit(selected_config["A"], results, selected_config["level"])
            st.pyplot(fig)
            #st.balloons()
        else:
            st.warning("No path found with these exact settings. Try fewer turns or longer length!")
    except Exception as e:
        st.error(f"Error: {e}")

# --- PROFESSIONAL FOOTER ---
st.markdown("---") # Adds a clean horizontal line above the footer

footer_html = """
<style>
    .main-footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #6c757d; /* Professional slate gray */
        text-align: center;
        padding: 20px 0px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border-top: 1px solid #e9ecef;
        margin-top: 50px;
    }
    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .joker-signature {
        font-weight: bold;
        color: #1f77b4; /* A nice "tech" blue */
        letter-spacing: 1px;
    }
    .copyright {
        font-size: 0.85rem;
    }
</style>

<div class="main-footer">
    <div class="footer-content">
        <div class="copyright">
            © 2026 Andrew Danda
        </div>
        <div>
            Made for ASP Grade 1 VEX 123 Sandwich STEM fair project
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)