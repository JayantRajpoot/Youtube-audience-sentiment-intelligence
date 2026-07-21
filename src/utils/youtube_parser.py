from urllib.parse import urlparse, parse_qs

def extract_video_id(url):

    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    video_id = parse_qs(parsed_url.query).get("v")

    if video_id:
        return video_id[0]

    path_parts = parsed_url.path.strip("/").split("/")

    if len(path_parts) == 2 and path_parts[0] == "live":
        return path_parts[1]

    return None

if __name__ == "__main__":

    urls = [
        "https://www.youtube.com/watch?v=c35fpGWqXnk",
        "https://youtu.be/c35fpGWqXnk",
        "https://www.youtube.com/watch?v=c35fpGWqXnk&t=20s",
        "https://www.youtube.com/live/c35fpGWqXnk"
    ]

    for url in urls:
        print(extract_video_id(url))