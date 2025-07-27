import streamlit as st
import os
import MeCab

# For MeCab config (Windows users)
os.environ["MECABRC"] = r"C:\Program Files\MeCab\etc\mecabrc"

st.title("Japanese Text Segmenter (MeCab + Streamlit)")

text = st.text_area("Paste Japanese text here:")

# Define common particles
particles = {"は", "が", "を", "に", "で", "と", "も", "へ", "の", "より", "から", "まで", "や"}

def styled_segmentation(text):
    tagger = MeCab.Tagger("-Owakati")
    lines = []
    for line in text.splitlines():
        if not line.strip():
            lines.append("")  # Preserve blank lines
            continue
        words = tagger.parse(line).strip().split()
        styled = ""
        for word in words:
            if word in particles:
                styled += (
                    f"<span style='background:#B2DFDB;"
                    f"color:#004D40;border-radius:8px;"
                    f"font-weight:bold;padding:4px 10px 4px 10px;"
                    f"margin:2px;display:inline-block;'>{word}</span> "
                )
            else:
                styled += (
                    f"<span style='background:#FAFAFA;"
                    f"color:#111;border-radius:8px;"
                    f"padding:4px 10px 4px 10px;"
                    f"margin:2px;display:inline-block;'>{word}</span> "
                )
        lines.append(styled)
    return "<br>".join(lines)

def plain_segmented(text):
    tagger = MeCab.Tagger("-Owakati")
    return "\n".join(
        tagger.parse(line).strip() if line.strip() else ""
        for line in text.splitlines()
    )

if st.button("Segment"):
    # Styled preview (optional)
    st.markdown(
        "#### Visualized Segmentation",
        help="Words are separated in boxes, particles are colored."
    )
    st.markdown(
        styled_segmentation(text),
        unsafe_allow_html=True,
    )

    # Copy-paste box (large, like Jisho)
    segmented = plain_segmented(text)
    st.markdown(
        "#### Segmented Output (copy and use!)"
    )
    st.text_area(
        "Segmented Output",
        value=segmented,
        height=300,
    )
