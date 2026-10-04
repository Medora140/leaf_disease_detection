import requests
import streamlit as st
from PIL import Image
from app.knowledge_base import get_disease_advice


st.set_page_config(
    page_title="UrbanLeaf AI | Plant health, made clearer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = "http://127.0.0.1:8000/predict"
PAGES = ["Home", "Upload a leaf", "Your results", "Remedies & chat"]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --teal:#001e2b; --deep:#003d4f; --green:#00ed64; --mint:#e3fcef; --ink:#001e2b; --muted:#52636d; --line:#d9e2e0; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:#fff; color:var(--ink); }
    [data-testid="stHeader"] { background:#fff; }
    [data-testid="stToolbar"] { visibility:hidden; }
    .block-container { max-width:1160px; padding:0 28px 3rem; }
    p, li, label, [data-testid="stCaptionContainer"] { color:#344b56; }
    h1,h2,h3,h4 { color:var(--teal) !important; font-family:'Manrope',sans-serif !important; letter-spacing:-.5px; }
    [data-testid="stMarkdownContainer"] p { color:#344b56; line-height:1.7; }
    [data-testid="stFileUploader"] section { background:#f7faf8; border:1px dashed #7b9b8d; border-radius:16px; }
    [data-testid="stFileUploader"] section *, [data-testid="stFileUploader"] small { color:#173b31 !important; }
    [data-testid="stFileUploader"] button { background:#fff !important; color:#003d4f !important; border:1px solid #7b9b8d !important; }
    .stButton > button { border:0; border-radius:999px; background:#00ed64; color:#001e2b; font-weight:700; min-height:44px; padding:0 22px; }
    .stButton > button:hover { background:#00d85b; color:#001e2b; }
    [data-testid="stChatMessage"] { background:#f6f9f7; border:1px solid #e2ebe7; border-radius:14px; }
    [data-testid="stChatMessage"] p { color:#203a45 !important; }
    [data-testid="stChatInput"] textarea { color:#001e2b !important; background:#fff !important; }
    [data-testid="stChatInput"] textarea::placeholder { color:#657780 !important; opacity:1; }
    .brandbar { display:flex; align-items:center; justify-content:space-between; padding:14px 0; border-bottom:1px solid #e5ece9; margin-bottom:14px; }
    .brand { display:flex; align-items:center; gap:10px; color:#001e2b; font:800 18px Manrope,sans-serif; }
    .brand-mark { width:34px; height:34px; display:grid; place-items:center; border-radius:12px; background:#00ed64; }
    .brand-note { color:#52636d; font-size:12px; }
    .nav-caption { margin:0 0 8px; color:#52636d; font-size:10px; font-weight:700; letter-spacing:1.3px; }
    [data-testid="stBaseButton-secondary"] { background:#f5f8f7 !important; color:#24444d !important; border:1px solid #d9e2e0 !important; }
    [data-testid="stBaseButton-primary"] { background:#00ed64 !important; color:#001e2b !important; border:1px solid #00b545 !important; box-shadow:0 3px 10px #00ed642b; }
    [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"] { min-height:44px !important; font-size:13px !important; white-space:nowrap !important; }
    .step-label { margin:8px 0 4px; color:#00844a; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1.4px; }
    .hero { display:grid; grid-template-columns:1.08fr .92fr; gap:30px; align-items:center; background:radial-gradient(ellipse at 85% 15%,#07543e,transparent 42%),#001e2b; color:white; padding:56px 48px; border-radius:24px; overflow:hidden; }
    .hero h1 { color:#fff !important; font-size:clamp(40px,5vw,63px); line-height:1.08; margin:10px 0 18px; letter-spacing:-2px; }
    .hero h1 span { color:#00ed64; }
    .hero p { color:#e0ece8 !important; font-size:16px; max-width:490px; }
    .hero .mini { color:#c0d1cb !important; font-size:12px; margin-top:20px; }
    .hero-visual { min-height:290px; position:relative; display:grid; place-items:center; border:1px solid #ffffff2b; border-radius:22px; background:linear-gradient(140deg,#0a6548,#003d4f 62%,#002d3b); }
    .hero-leaf { font-size:116px; filter:drop-shadow(0 15px 24px #001a); transform:rotate(-18deg); }
    .hero-badge { position:absolute; right:16px; bottom:16px; background:#fff; color:#001e2b; padding:13px 16px; border-radius:13px; font-size:12px; font-weight:700; box-shadow:0 10px 30px #00131c66; }
    .statrow { display:flex; gap:12px; margin:20px 0; }
    .stat { flex:1; padding:15px; border:1px solid #e1e8e5; border-radius:13px; background:#f9fbfa; }
    .stat b { display:block; color:#003d4f; font:700 22px Manrope,sans-serif; }
    .stat span { color:#455c65; font-size:11px; }
    .info-card { padding:22px; border:1px solid #e0e8e5; background:#fff; border-radius:16px; }
    .info-card h3 { margin-top:0; }
    .remedy { padding:18px 20px; margin:10px 0; background:#f7faf8; border:1px solid #e2ebe7; border-radius:14px; }
    .remedy h4 { margin:0 0 7px; }
    .footer { text-align:center; color:#52636d; font-size:11px; padding:30px 0 4px; }
    @media(max-width:760px) { .block-container { padding:0 16px 2rem; } .hero { grid-template-columns:1fr; padding:34px 24px; } .hero-visual { min-height:210px; } .hero-leaf { font-size:82px; } .brand-note { display:none; } .statrow { flex-wrap:wrap; } }
    </style>
    """,
    unsafe_allow_html=True,
)

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "report" not in st.session_state:
    st.session_state.report = None
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "upload_error" not in st.session_state:
    st.session_state.upload_error = ""

st.markdown(
    '<div class="brandbar"><div class="brand"><span class="brand-mark">✳</span> urbanleaf<span style="color:#008c54;font-weight:500">.ai</span></div><div class="brand-note">A little more life in every leaf.</div></div>',
    unsafe_allow_html=True,
)

def go_to(page):
    # Button callbacks update the page before Streamlit reruns the script.
    st.session_state.page = page


def analyze_uploaded_leaf():
    uploaded_file = st.session_state.get("leaf_upload")
    if not uploaded_file:
        return
    image_bytes = uploaded_file.getvalue()
    st.session_state.image_bytes = image_bytes
    st.session_state.image_name = uploaded_file.name
    try:
        response = requests.post(
            API_URL,
            files={"file": (uploaded_file.name, image_bytes, uploaded_file.type)},
            timeout=60,
        )
        response.raise_for_status()
        st.session_state.report = response.json()["data"]
        st.session_state.chat_history = []
        st.session_state.upload_error = ""
        go_to("Your results")
    except requests.RequestException:
        st.session_state.upload_error = "We couldn’t reach the diagnosis service. Start the FastAPI server and try again."
    except (KeyError, ValueError):
        st.session_state.upload_error = "The diagnosis service returned an unexpected response. Please try again."


def get_report():
    report = st.session_state.report or {}
    prediction = report.get("prediction", "")
    guidance = report.get("agricultural_guidance") or get_disease_advice(prediction)
    return report, guidance


selected_page = st.session_state.page
st.markdown('<div class="nav-caption">YOUR GARDEN · YOUR PROGRESS</div>', unsafe_allow_html=True)
nav_columns = st.columns(4, gap="small")
for index, (nav_column, page) in enumerate(zip(nav_columns, PAGES), start=1):
    with nav_column:
        st.button(
            f"{index:02d}  {page}",
            key=f"nav_{index}",
            type="primary" if selected_page == page else "secondary",
            use_container_width=True,
            on_click=go_to,
            args=(page,),
        )


if selected_page == "Home":
    st.markdown(
        """
        <section class="hero">
          <div><div class="step-label" style="color:#a9f6c7">A little more life in every leaf</div>
            <h1>Healthy plants<br>start with a<br><span>closer look.</span></h1>
            <p>Your pocket plant-health companion. Check a leaf, understand what you’re seeing, and find practical care guidance for your garden.</p>
            <p class="mini">For pepper · potato · tomato &nbsp; | &nbsp; 10 health categories</p>
          </div>
          <div class="hero-visual"><div class="hero-leaf">🌿</div><div class="hero-badge">✳ &nbsp; A clearer view of plant health</div></div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="step-label">From leaf to next step</div><h2>Simple by nature</h2>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, number, title, copy in zip(
        cols,
        ["01", "02", "03"],
        ["Choose a leaf", "Get an AI check", "Find your next step"],
        ["Add a clear photo of a pepper, potato, or tomato leaf.", "The image classifier checks for supported healthy and disease categories.", "Read the result and explore practical plant-care notes."],
    ):
        with col:
            st.markdown(f'<div class="info-card"><div class="step-label">{number}</div><h3>{title}</h3><p>{copy}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="statrow"><div class="stat"><b>3</b><span>garden crops</span></div><div class="stat"><b>10</b><span>health categories</span></div><div class="stat"><b>1</b><span>simple next step</span></div></div>', unsafe_allow_html=True)
    st.button("Start with a leaf photo  →", on_click=go_to, args=("Upload a leaf",))

elif selected_page == "Upload a leaf":
    st.markdown('<div class="step-label">Your garden, in focus · 01</div><h1>Upload a leaf photo</h1><p>Choose a clear, well-lit JPG or PNG image with one leaf in focus.</p>', unsafe_allow_html=True)
    col_image, col_upload = st.columns([1, 1], gap="large")
    with col_upload:
        uploaded_file = st.file_uploader("Choose a leaf photo", type=["jpg", "jpeg", "png"], key="leaf_upload")
        if uploaded_file:
            st.session_state.image_bytes = uploaded_file.getvalue()
            st.session_state.image_name = uploaded_file.name
            st.button("Analyze this leaf  →", use_container_width=True, on_click=analyze_uploaded_leaf)
        if st.session_state.upload_error:
            st.error(st.session_state.upload_error)
        elif st.session_state.image_bytes:
            st.info(f"Photo ready: {st.session_state.get('image_name', 'leaf image')}. Choose another image above or continue your previous result.")
            st.button("View previous result  →", on_click=go_to, args=("Your results",))
    with col_image:
        if st.session_state.image_bytes:
            st.image(st.session_state.image_bytes, caption="Selected leaf photo", use_container_width=True)
        else:
            st.markdown('<div class="info-card"><h3>For a clearer check</h3><p>Use natural light, keep the leaf in focus, and include as little background as possible.</p><p>UrbanLeaf currently checks pepper, potato, and tomato leaves.</p></div>', unsafe_allow_html=True)

elif selected_page == "Your results":
    st.markdown('<div class="step-label">Your plant health check · 02</div><h1>Your results</h1>', unsafe_allow_html=True)
    if not st.session_state.report:
        st.info("Upload a leaf photo first to see your diagnosis.")
        st.button("Go to photo upload  →", on_click=go_to, args=("Upload a leaf",))
    else:
        report, guidance = get_report()
        left, right = st.columns([0.8, 1.2], gap="large")
        with left:
            if st.session_state.image_bytes:
                st.image(st.session_state.image_bytes, caption=st.session_state.get("image_name", "Your leaf photo"), use_container_width=True)
        with right:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("#### Classification")
            st.success(guidance.get("disease_name", report.get("prediction", "Plant health result")))
            confidence = report.get("confidence")
            if confidence is not None:
                st.metric("Model confidence", f"{confidence}%")
                st.progress(max(0.0, min(float(confidence) / 100, 1.0)))
            st.markdown("**What this result means**")
            st.write(guidance.get("symptoms", "No additional symptom notes are available."))
            st.caption("This is an AI-assisted image classification. Check the plant and growing conditions directly if symptoms persist.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("")
        st.button("See remedies and ask a question  →", on_click=go_to, args=("Remedies & chat",))

else:
    st.markdown('<div class="step-label">Practical plant care · 03</div><h1>Remedies & chat</h1><p>Review the guidance for this result, then ask the UrbanLeaf helper a question.</p>', unsafe_allow_html=True)
    if not st.session_state.report:
        st.info("Upload a leaf photo and view its result to get tailored remedies and chat guidance.")
        st.button("Go to photo upload  →", on_click=go_to, args=("Upload a leaf",))
    else:
        report, guidance = get_report()
        crop_name = guidance.get("disease_name", report.get("prediction", "this result"))
        remedy_col, chat_col = st.columns([0.9, 1.1], gap="large")
        with remedy_col:
            st.markdown(f"### Guidance for {crop_name}")
            st.markdown(f'<div class="remedy"><div class="step-label">Immediate care</div><p>{guidance.get("immediate_action", "No immediate care notes are available.")}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="remedy"><div class="step-label">Prevention</div><p>{guidance.get("prevention", "No prevention notes are available.")}</p></div>', unsafe_allow_html=True)
            st.caption("Use any plant protection product only as its label directs and follow local guidance.")
        with chat_col:
            st.markdown("### Ask the UrbanLeaf helper")
            st.caption("Answers use the diagnosis and care notes available in this project.")
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            question = st.chat_input("Ask about symptoms, care, or prevention…")
            if question:
                st.session_state.chat_history.append({"role": "user", "content": question})
                normalized = question.lower()
                if any(word in normalized for word in ["symptom", "look", "spot", "mean", "sign"]):
                    answer = guidance.get("symptoms", "No symptom details are available for this result.")
                elif any(word in normalized for word in ["prevent", "avoid", "next time", "stop spread"]):
                    answer = guidance.get("prevention", "No prevention details are available for this result.")
                elif any(word in normalized for word in ["treat", "remedy", "care", "do", "help", "now", "action"]):
                    answer = guidance.get("immediate_action", "No immediate care details are available for this result.")
                else:
                    answer = (f"For **{crop_name}**, here are the project’s care notes:\n\n"
                              f"**Symptoms:** {guidance.get('symptoms', 'Not available.')}\n\n"
                              f"**Immediate care:** {guidance.get('immediate_action', 'Not available.')}\n\n"
                              f"**Prevention:** {guidance.get('prevention', 'Not available.')}")
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()

st.markdown('<div class="footer">✳ &nbsp; urbanleaf.ai &nbsp; · &nbsp; Helping home growers take a closer look.</div>', unsafe_allow_html=True)
