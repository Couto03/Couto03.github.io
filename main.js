window.addEventListener('DOMContentLoaded', () => {

    const apiKey = 'AIzaSyAaiTkIZROTx8mrKoQgyov7fkKgx0rpBbs';

    document.getElementById('search_button').addEventListener('click', function() {

        console.log("Pressed");

        const queryElement = document.getElementById('search_query');
        const query = queryElement.value;
        const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${query}&key=${apiKey}`;

        fetch(url)
        .then(response => response.json())
        .then(data => {
            let videoIds = [];
            for (let i = 0; i < data.items.length; i++) {
                videoIds.push(data.items[i].id.videoId);
            }
            const ids = videoIds.join(',');
                const newUrl = `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${ids}&key=${apiKey}`;
                fetch(newUrl)
                .then(response => response.json())
                .then(data => {
                
                    const container = document.getElementById('response');
                    data.items.forEach((value) => {
                        const title = value.snippet.title;
                        const thumbnail = value.snippet.thumbnails.maxres.url;
                        const channel = value.snippet.channelTitle;

                        const videoPlaceholder = document.createElement('div');
                        videoPlaceholder.style.display = "flex";
                        videoPlaceholder.style.marginBottom = "16px";

                        const image = document.createElement('img');
                        image.src = thumbnail;
                        image.style.display = 'block';
                        image.style.width = '100px';
                        image.style.height = '100px';
                        image.style.borderRadius = '8px';
                        image.style.objectFit = 'cover';

                        videoPlaceholder.appendChild(image);

                        const titleAuthorPlaceholder = document.createElement('div');
                        titleAuthorPlaceholder.style.fontSize = "small";
                        titleAuthorPlaceholder.style.paddingLeft = "20px";

                        const titlePlaceholder = document.createElement('h2');
                        titlePlaceholder.innerText = title;

                        const authorPlaceholder = document.createElement('h4');
                        authorPlaceholder.innerText = channel;
                        authorPlaceholder.style.color = "gray";

                        titleAuthorPlaceholder.appendChild(titlePlaceholder);
                        titleAuthorPlaceholder.appendChild(authorPlaceholder);

                        videoPlaceholder.appendChild(titleAuthorPlaceholder);

                        container.appendChild(videoPlaceholder);
                    })
                })
                .catch(error => console.error('Error:', error));
         
        })
        .catch(error => console.error('Error:', error));
    })

})
