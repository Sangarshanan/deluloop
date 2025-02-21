![delulu](assets/logo.png)

Generative looper for musicians built with [streamlit](https://streamlit.io/) and [Jasco](https://huggingface.co/facebook/jasco-chords-drums-melody-1B)

Install requirements

```sh
pip install -r requirements.txt
```


Create a .env file with HF_KEY

```sh
HF_KEY="test"
```

Run the app

```sh
streamlit run app.py
```

Docker build & run

```sh
docker build -t deluloop .
docker run -p 8501:8501 deluloop
```

This project was built and presented for the Music Hack Day at ADCx India 2025 https://audio.dev/adcx-india-25/

Demo: https://drive.google.com/file/d/19ZUuHIMaOiaToT_uqX5C51Zemq5u_cqO/view?t=1

### References

- https://arxiv.org/pdf/2406.10970


### Future Ideas

- Allow trimming of loops
- Multiple loop generations on single page
- Volume Control of loops
