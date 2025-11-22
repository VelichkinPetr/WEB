const API_KEY = '4c9cd7c1a8524b7bae7132636250610';
const cities = new Set();

async function addCity() {
            const cityInput = document.getElementById('cityInput');
            const cityName = cityInput.value;
            if (cities.has(cityName)){cityInput.value = '';}

            if (cityName && !cities.has(cityName))  {
                cities.add(cityName);   
                cityInput.value = '';
                createSkeleton(cityName);
                await getWeatherForCity(cityName);
            }
        }

// Функция для получения погоды для одного города
async function getWeatherForCity(cityName) {
        const loadingMessage = document.getElementById('loadingMessage');
        const skeleton = document.getElementById(`skeleton-${cityName}`);
            
        if (loadingMessage) {
                loadingMessage.style.display = 'none';
            }
    try {
        
        const response = await fetch(
            `https://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${cityName}&lang=ru`
        );
        if (skeleton) {
                skeleton.remove();
            }
        const data = await response.json();
        displayWeather(data)
        
    } catch (error) {
        console.error('Ошибка получения погоды:', error);
    }
}

// Функция для получения погоды для всех городов
async function getWeatherForAll() {
    const weatherContainer = document.getElementById('weatherContainer');

    if (cities.size === 0) {
        weatherContainer.innerHTML = '<div class="loading">Добавьте города для отображения погоды</div>';
        return;
    }
    weatherContainer.innerHTML = '';
    const skeletons = Array.from(cities).forEach(city => {
        createSkeleton(city);
    });
    const promises = Array.from(cities).map(city => 
        getWeatherForCity(city)
    );
    
}

function createSkeleton(cityName) {
    const weatherContainer = document.getElementById('weatherContainer');
    const skeleton = document.createElement('div');
    skeleton.className = 'skeleton-card';
    skeleton.id = `skeleton-${cityName}`;
    
    skeleton.innerHTML = `
        <div class="skeleton-header"></div>
        <div class="skeleton-content">
            <div class="skeleton-temperature"></div>
            <div class="skeleton-details">
                <div class="skeleton-line"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line"></div>
            </div>
        </div>
        <div class="skeleton-icon"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line"></div>
    `;
    weatherContainer.appendChild(skeleton);
}

// Функция для отображения погоды
function displayWeather(data) {
    const weatherCard = document.createElement('div');
    weatherCard.className = 'weather-card';
    weatherCard.id = `weather-${data.location.name}`;
    
    weatherCard.innerHTML = `
        <h3>${data.location.name}, ${data.location.country}</h3>
        <div class="weather-info">
            <div class="temperature">${Math.round(data.current.temp_c)}°C</div>
            <div class="weather-details">
                <p><strong>${data.current.condition.text}</strong></p>
                <p>💧 Влажность: ${data.current.humidity}%</p>
                <p>💨 Ветер: ${data.current.wind_kph} км/ч</p>
                <p>👁️ Видимость: ${data.current.vis_km} км</p>
            </div>
        </div>
        <img src="https:${data.current.condition.icon}" alt="${data.current.condition.text}">
        <p><small>Обновлено: ${new Date(data.current.last_updated).toLocaleTimeString('ru-RU')}</small></p>
        <button onclick="removeCity('${data.location.name}')" style="margin-top: 10px; background: #e74c3c;">Удалить</button>
    `;
    
    weatherContainer.appendChild(weatherCard);
    
}


// Функция для удаления города
function removeCity(cityName) {
    cities.delete(cityName);
    const card = document.getElementById(`weather-${cityName}`);
    if (card) card.remove();
    
    if (cities.size === 0) {
        const weatherContainer = document.getElementById('weatherContainer');
        weatherContainer.innerHTML = '<div class="loading">Добавьте города для отображения погоды</div>';
    }
}

// Функция для очистки всех городов
function clearAll() {
    cities.clear();
    const weatherContainer = document.getElementById('weatherContainer');
    weatherContainer.innerHTML = '<div class="loading">Добавьте города для отображения погоды</div>';
}
