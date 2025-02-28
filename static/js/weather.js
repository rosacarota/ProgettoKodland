document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("weatherForm").addEventListener("submit", function (event) {
        event.preventDefault();
        let city = document.getElementById("cityInput").value;

        // Ottenere latitudine e longitudine della città
        let geocodeUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${city}&count=1&language=it`;

        fetch(geocodeUrl)
            .then(response => response.json())
            .then(data => {
                if (!data.results || data.results.length === 0) {
                    document.getElementById("weatherResult").innerHTML = `<p class="text-danger">Città non trovata. Riprova!</p>`;
                    return;
                }

                let lat = data.results[0].latitude;
                let lon = data.results[0].longitude;

                // Ottenere previsioni meteo e temperature orarie
                let weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=weathercode&hourly=temperature_2m&timezone=Europe/Rome`;

                return fetch(weatherUrl);
            })
            .then(response => response.json())
            .then(weatherData => {
                if (!weatherData || !weatherData.daily || !weatherData.hourly) {
                    document.getElementById("weatherResult").innerHTML = `<p class="text-danger">Errore nel recupero dei dati meteo.</p>`;
                    return;
                }

                let today = new Date();
                let days = [
                    today.toLocaleDateString("it-IT", { weekday: "long", day: "numeric", month: "long" }),
                    new Date(today.getTime() + 86400000).toLocaleDateString("it-IT", { weekday: "long", day: "numeric", month: "long" }),
                    new Date(today.getTime() + 172800000).toLocaleDateString("it-IT", { weekday: "long", day: "numeric", month: "long" })
                ];

                let weatherCodes = weatherData.daily.weathercode;
                let hourlyTemps = weatherData.hourly.temperature_2m;
                let hourlyTimes = weatherData.hourly.time;

                let dayTemps = [];
                let nightTemps = [];

                // Trova le temperature diurne (11:00) e notturne (20:00) per i 3 giorni
                for (let d = 0; d < 3; d++) {
                    let tempDay = null;
                    let tempNight = null;

                    for (let i = d * 24; i < (d + 1) * 24; i++) {
                        let hour = new Date(hourlyTimes[i]).getHours();
                        if (hour === 11) tempDay = hourlyTemps[i];
                        if (hour === 20) tempNight = hourlyTemps[i];
                    }

                    dayTemps.push(tempDay);
                    nightTemps.push(tempNight);
                }

                // Mappatura dei codici meteo con descrizioni e icone
                const weatherMap = {
                    0: ["Soleggiato", "☀️"],
                    1: ["Prevalentemente sereno", "🌤️"],
                    2: ["Parzialmente nuvoloso", "⛅"],
                    3: ["Nuvoloso", "☁️"],
                    45: ["Nebbia", "🌫️"],
                    48: ["Nebbia ghiacciata", "🌫️❄️"],
                    51: ["Pioviggine leggera", "🌦️"],
                    53: ["Pioviggine moderata", "🌦️"],
                    55: ["Pioviggine intensa", "🌧️"],
                    61: ["Pioggia leggera", "🌧️"],
                    63: ["Pioggia moderata", "🌧️"],
                    65: ["Pioggia intensa", "🌧️⛈️"],
                    71: ["Neve leggera", "❄️"],
                    73: ["Neve moderata", "❄️"],
                    75: ["Neve intensa", "❄️❄️"],
                    80: ["Rovesci leggeri", "🌦️"],
                    81: ["Rovesci moderati", "🌧️"],
                    82: ["Rovesci intensi", "⛈️"],
                    95: ["Temporali", "⛈️"],
                    96: ["Temporali con grandine", "⛈️❄️"],
                    99: ["Temporali intensi con grandine", "⛈️❄️"]
                };

                let weatherDescriptions = [];
                for (let d = 0; d < 3; d++) {
                    weatherDescriptions.push(weatherMap[weatherCodes[d]] || ["Dato non disponibile", "❓"]);
                }

                document.getElementById("weatherResult").innerHTML = `
                    <h3 class="mt-3">
                        ${city} - ${days[0]}  
                        <span class="ms-3">🌞 ${dayTemps[0]}°C</span>  
                        <span class="ms-3">🌙 ${nightTemps[0]}°C</span>  
                    </h3>
                    <table class="table table-bordered mt-3">
                        <thead class="table-dark">
                            <tr>
                                <th>Giorno</th>
                                <th>Meteo</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>${days[0]}</td>
                                <td>${weatherDescriptions[0][1]} ${weatherDescriptions[0][0]}</td>
                            </tr>
                            <tr>
                                <td>${days[1]}</td>
                                <td>${weatherDescriptions[1][1]} ${weatherDescriptions[1][0]}</td>
                            </tr>
                            <tr>
                                <td>${days[2]}</td>
                                <td>${weatherDescriptions[2][1]} ${weatherDescriptions[2][0]}</td>
                            </tr>
                        </tbody>
                    </table>
                `;
            })
            .catch(error => {
                console.error("Errore:", error);
                document.getElementById("weatherResult").innerHTML = `<p class="text-danger">Errore nel recupero dei dati meteo.</p>`;
            });
    });
});
