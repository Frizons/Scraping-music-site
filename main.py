import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

finding_song = input("Input song name: ")

edge_options = Options()
edge_options.add_argument("--headless")
driver = webdriver.Edge(options=edge_options)
driver.get("https://z3.fm/")
find_song = driver.find_element(By.ID, "topkeywords")
find_song.send_keys(finding_song)
button = driver.find_element(By.CSS_SELECTOR, "#yt0.btn2")
driver.execute_script("arguments[0].click();", button)
driver.get(driver.current_url)

full_list_songs = []
URL = "https://z3.fm/mp3/search"
finding_song_repl = finding_song.replace(" ", "+")
button_class = "next next-btn"
number_page = 0

while button_class == "next next-btn":
    number_page += 1
    param = {"keywords": finding_song_repl, "page": number_page}
    full_url = requests.Request("GET", URL, params=param).prepare().url
    driver.get(full_url)
    if number_page == 1:
        count_songs = driver.find_element(By.CSS_SELECTOR, "b.grey").text
        try:
            int(count_songs)
            print(f"Found total count songs: {count_songs}")
        except:
            print("Songs don't found")
    else:
        pass
    print(f"Copy page {number_page}")
    find_tag_songs = driver.find_elements(By.CLASS_NAME, "mb-tooltip")
    songs_list = [
        [elem.text, elem.get_attribute("href").replace("song", "download")]
        for elem in find_tag_songs
        if elem.get_attribute("href").count("song") == 1
    ]
    for el in songs_list:
        full_list_songs.append(el)
    print(f"Page {number_page} Comlete")
    try:
        button_next = driver.find_element(By.CSS_SELECTOR, "a.next.next-btn")
        button_class = button_next.get_attribute("class")
    except:
        button_class = None

n = 0
for song in full_list_songs:
    n += 1
    print(f"Number: {n}, Name: {song[0]}, Link: {song[1]}")
