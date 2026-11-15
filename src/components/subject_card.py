import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback= None):
    html = f"""
    <div style = "
         background:white;border-left:8px solid black; padding:20px; border-radius:20px; border:3px solid black; margin-bottom:20px;
    ">
        <h3 style="margin:0; color:darkblue; font-size:1.5rem;">
        {name}
        </h3>
        <p style="color: blue; margin:10px 0;">
            Code:
            <span style="background:#faeeee; color: Black; padding:4px 8px; border-radius:4px;">
                {code}
            </span> | Section: <span style="background:#faeeee; color: Black;padding:4px 8px; border-radius:4px;">{section}</span>
        </p>
    """
    if stats:
        html += '<div style="display:flex; gap:8px; flex-wrap:wrap;">'
        for icon, label, value in stats:
            html += f'<div style="background: yellow; padding:5px 12px; border-radius:12px; font-size:0.9rem">{icon} <b> {label} :  </b> {value}</div>'
        # closing the main div
        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)
        # The share button
        if footer_callback:
            footer_callback()
