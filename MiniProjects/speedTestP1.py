from speedtest import Speedtest

#creating an object 
st = Speedtest()
try:
    print(f"Downloading speed: {st.download()}kb\s")
    print(f"Uploading speed: {st.upload()}kb\s")
except Exception:
    print("Error!.. Please check internet connection")
