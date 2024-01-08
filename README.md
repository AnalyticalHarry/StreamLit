# Streamlit Tutorials

## Install & Import

```bash
pip install streamlit
```
```bash
import streamlit as st
```

## Run in CMD prompt or power shell 
```bash
streamlit run first_app.py
```

## Command Line
```bash
streamlit --help
streamlit run your_script.py
streamlit hello
streamlit config show
streamlit cache clear
streamlit docs
streamlit --version
```

## Magic commands
```bash
# Magic commands implicitly
# call st.write().
'_This_ is some **Markdown***'
my_variable
'dataframe:', my_data_frame

```

## Display text
```bash
st.text('Fixed width text')
st.markdown('_Markdown_') # see *
st.latex(r''' e^{i\pi} + 1 = 0 ''')
st.write('Most objects') # df, err, func, keras!
st.write(['st', 'is <', 3]) # see *
st.title('My title')
st.header('My header')
st.subheader('My sub')
st.code('for i in range(8): foo()')
# optional kwarg unsafe_allow_html = True

```


```bash
streamlit run first_app.py
```


```bash
streamlit run first_app.py
```


```bash
streamlit run first_app.py
```
