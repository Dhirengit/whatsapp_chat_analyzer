mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"dhiren19gld@gmail.com\"\n\
" > ~/s.streamlit/credetials.toml
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml