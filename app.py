import streamlit as st
import nltk
import pages, helpy
from components.preprocess import getMostCommonFeatures
from components.util import loadFiles, transformData, readRawData
import pickle

st.set_page_config(page_title="Lixplore", page_icon="🔍", initial_sidebar_state="expanded")

# 1. Sidebar Button Design (no borders & background and boldy)
# 2. Make Sidebar smaller, to the top and Hide Sidebar Close-Button (X)
# 3. Hide Anchors for header tags
# 4. Hide Footer
THEME = [
     " .css-1qrvfrg {background-color: rgba(249, 249, 251, 0); border: 0px solid rgba(49, 51, 63, 0.2); font-weight: 600} ", # 1. (light)
     " .css-wq85zr {background-color: rgba(249, 249, 251, 0); border: 0px solid rgba(49, 51, 63, 0.2); font-weight: 600} ",  # 1. (dark)
     " .css-zbg2rx, .css-4s3xrj {width: 12rem; padding: 1rem 1rem} .css-119ihf6 {display: none} ",   # 2. (light)
     " .css-sygy1k, .css-4s3xrj {width: 12rem; padding: 1rem 1rem} .css-1f7vzus {display: none} ",   # 2. (dark)
     " .css-eczf16 {display: none} ",   # 3. (light)
     " .css-15zrgzn {display: none} ",  # 3. (dark)
     " .css-1q1n0ol {display: none} ",  # 4. (light)
     " .css-1lsmgbg {display: none} "   # 4. (dark)
]
st.markdown("<style>"+"".join(THEME)+"</style>", unsafe_allow_html=True)


# ADD NEW PAGE HERE:
# (name according to .py file in pages subfolder!)
page_list = ["examine", "extract", "exercise"]#, "playground"]
# Also add new page in pages/__init__.py !!!

### SESSION STATE ###
if "cur_page" not in st.session_state:
    st.session_state.cur_page = "start"
    helpy.greet()
if "data" not in st.session_state:
    st.session_state.data = transformData(readRawData())
if "pdf_files" not in st.session_state:
    st.write("loaded new pdf_files")
    st.session_state.pdf_files = loadFiles("../pdfs/", "pdf")
if "references" not in st.session_state:
    st.session_state.references = helpy.getReferences()
if "most_common_features" not in st.session_state:
    st.session_state.most_common_features = getMostCommonFeatures(loadFiles("../pdfs/extracted_text/", "pickle", open_pickle=True))
    
st.experimental_set_query_params(page=st.session_state.cur_page)

### PAGE & SIDEBAR CONTENT ###
st.sidebar.title("🔍 Lixplore")
for page in page_list:
    if st.session_state.cur_page == page:
        eval(f"pages.{page}.renderPage()")
    if st.sidebar.button(page.title()):
        st.session_state.cur_page = page
        st.experimental_rerun()

st.sidebar.write("---")

st.sidebar.caption("Made with ❤️")
st.sidebar.caption("[Source](https://github.com/dunder-1/Lixplore)")