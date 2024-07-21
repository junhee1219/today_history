// 시계 업데이트 함수 추가
function updateClock() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 월은 0부터 시작하므로 +1
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    const formattedTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    
    document.getElementById('clock').textContent = formattedTime;
}

function CurMap() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1); // 월은 0부터 시작하므로 +1
    const day = String(date.getDate());
    const hour = String(date.getHours());
    const minute = String(date.getMinutes());
  
    return {
        "year":year,
        "month":month,
        "day":day,
        "hour":hour,
        "minute" :minute
    }
  }
  
  function UTCMap() {
    const date = new Date();
    const year = date.getUTCFullYear();
    const month = String(date.getUTCMonth() + 1); // 월은 0부터 시작하므로 +1
    const day = String(date.getUTCDate());
    const hour = String(date.getUTCHours());
    const minute = String(date.getUTCMinutes());
  
    return {
        "year":year,
        "month":month,
        "day":day,
        "hour":hour,
        "minute" :minute
    }
  }
  
  
const submit = async () => {
    const eventList = document.getElementById('event-list');
    try {
        let contents = {
            "UTCMap": UTCMap(),
            "CurMap": CurMap()
        };
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contents)
        });

        const datalist = await response.json();  
        console.log(datalist);
        datalist.forEach(data => {
            const card = document.createElement('div');
            card.className = 'col-md-4 event-card';
            card.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${data.year}년에는...</h5>
                        <p class="card-text">${data.content}</p>
                    </div>
                </div>
            `;
            eventList.appendChild(card);
        });
    } catch (e) {
        eventList.innerHTML += '<hr>' + e;
    }finally {
        // 로딩 바 숨기기
        loading.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    submit();
    updateClock();
    setInterval(updateClock, 1000);
});