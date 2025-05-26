from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)
PROGRESO_PATH = 'progreso.json'

if not os.path.exists(PROGRESO_PATH):
    with open(PROGRESO_PATH, 'w') as f:
        json.dump({"nivel_actual": 1, "puntos": 0}, f)

def leer_progreso():
    with open(PROGRESO_PATH, 'r') as f:
        return json.load(f)

def guardar_progreso(data):
    with open(PROGRESO_PATH, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def inicio():
    return render_template_string("""
    <html>
    <head>
        <title>El Jardín de los Secretos</title>
        <style>
            body {
                background: linear-gradient(to bottom, #fce4ec, #f3e5f5);
                color: #5e2c3c;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
                padding-top: 10%;
                overflow: hidden;
                position: relative;
                height: 100vh;
            }
            .boton {
                background-color: #5e2c3c;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 20px;
                font-size: 20px;
                text-decoration: none;
            }
            .petalo {
                position: absolute;
                width: 20px;
                height: 20px;
                background: radial-gradient(circle at center, #f8bbd0 0%, #e1bee7 70%);
                border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
                opacity: 0.8;
                animation-name: caer;
                animation-iteration-count: infinite;
                animation-timing-function: linear;
            }
            @keyframes caer {
                0% {
                    transform: translateY(-30px) rotate(0deg);
                    opacity: 0.8;
                }
                100% {
                    transform: translateY(110vh) rotate(360deg);
                    opacity: 0;
                }
            }
        </style>
    </head>
    <body>
        <h1>🌸 Bienvenida Eli al Jardín de los Secretos 🌸</h1>
        <a class="boton" href="/mapa">Comenzar a jugar</a>

        <script>
            function crearPetalo() {
                const petalo = document.createElement('div');
                petalo.classList.add('petalo');
                petalo.style.left = Math.random() * window.innerWidth + 'px';
                petalo.style.animationDuration = (4 + Math.random() * 4) + 's';
                petalo.style.animationDelay = Math.random() * 10 + 's';
                document.body.appendChild(petalo);

                petalo.addEventListener('animationend', () => {
                    petalo.remove();
                });
            }
            setInterval(crearPetalo, 500);
        </script>
    </body>
    </html>
    """)

@app.route('/mapa')
def mapa():
    progreso = leer_progreso()
    nivel_actual = progreso['nivel_actual']

    flores = ''
    for i in range(1, 11):
        estado = 'desbloqueado' if i <= nivel_actual else 'bloqueado'
        flores += f'''
        <div class="flor-container">
            <button class="flor {estado}" onclick="jugarNivel({i})" {'disabled' if estado == 'bloqueado' else ''} title="Nivel {i}">
                🌸<br><span class="numero">{i}</span>
            </button>
        </div>
        '''

    return render_template_string(f"""
    <html>
    <head>
        <title>Mapa de Niveles</title>
        <style>
            body {{
                background: #fff0f5;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
                overflow: hidden;
                height: 100vh;
                position: relative;
            }}
            h1 {{
                color: #5e2c3c;
                margin-top: 20px;
            }}
            .jardin {{
                display: grid;
                grid-template-columns: repeat(6, 1fr);
                gap: 15px;
                margin: 30px auto;
                max-width: 800px;
            }}
            .flor {{
                padding: 10px;
                font-size: 24px;
                border: none;
                border-radius: 50%;
                width: 80px;
                height: 80px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                box-shadow: 0 0 10px transparent;
            }}
            .flor:hover {{
                transform: scale(1.15);
                cursor: pointer;
                box-shadow: 0 0 15px #ba68c8;
            }}
            .desbloqueado {{
                background: linear-gradient(145deg, #f8bbd0, #e1bee7);
                color: #5e2c3c;
                animation: suaveBrillo 3s ease-in-out infinite;
            }}
            .bloqueado {{
                background: #dcdcdc;
                color: #aaa;
                cursor: default;
                filter: grayscale(60%);
            }}
            .numero {{
                font-size: 16px;
                display: block;
                margin-top: 5px;
                font-weight: bold;
            }}
            @keyframes suaveBrillo {{
                0%, 100% {{
                    box-shadow: 0 0 15px #ba68c8;
                }}
                50% {{
                    box-shadow: 0 0 25px #ce93d8;
                }}
            }}
            .petalo {{
                position: absolute;
                width: 20px;
                height: 20px;
                background: radial-gradient(circle at center, #f8bbd0 0%, #e1bee7 70%);
                border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
                opacity: 0.8;
                animation-name: caer;
                animation-iteration-count: infinite;
                animation-timing-function: linear;
                pointer-events: none;
                z-index: 1000;
            }}
            @keyframes caer {{
                0% {{
                    transform: translateY(-30px) rotate(0deg);
                    opacity: 0.8;
                }}
                100% {{
                    transform: translateY(110vh) rotate(360deg);
                    opacity: 0;
                }}
            }}
        </style>
        <script>
            function jugarNivel(n) {{
                const botones = document.querySelectorAll('.flor');
                const boton = botones[n - 1];
                if (!boton.classList.contains('bloqueado')) {{
                    window.location.href = '/nivel/' + n;
                }}
            }}

            function crearPetalo() {{
                const petalo = document.createElement('div');
                petalo.classList.add('petalo');
                petalo.style.left = Math.random() * window.innerWidth + 'px';
                petalo.style.animationDuration = (4 + Math.random() * 4) + 's';
                petalo.style.animationDelay = Math.random() * 10 + 's';
                document.body.appendChild(petalo);

                petalo.addEventListener('animationend', () => {{
                    petalo.remove();
                }});
            }}

            setInterval(crearPetalo, 300);
        </script>
    </head>
    <body>
        <h1>🌷 Mapa del Jardín 🌷</h1>
        <div class="jardin">
            {flores}
        </div>
    </body>
    </html>
    """)

@app.route('/nivel/<int:n>')
def nivel(n):
    progreso = leer_progreso()
    if n > progreso['nivel_actual']:
        return "<h1>❌ Nivel bloqueado</h1>"

    if n == 1:
        return render_template_string("""
        <html>
        <head>
            <title>Nivel 1 - Captura las Flores</title>
            <style>
                body {
                    background: linear-gradient(to bottom, #fce4ec, #f3e5f5);
                    text-align: center;
                    font-family: 'Segoe UI', sans-serif;
                    overflow: hidden;
                    height: 100vh;
                    margin: 0;
                    padding: 0;
                    color: #5e2c3c;
                }
                h1 {
                    margin-top: 20px;
                }
                #juego {
                    position: relative;
                    width: 100vw;
                    height: 70vh;
                    background: linear-gradient(to top, #f3e5f5, #fce4ec);
                    overflow: hidden;
                    border-radius: 15px;
                    margin: 20px auto;
                    max-width: 600px;
                    box-shadow: 0 0 20px #ba68c8aa;
                }
                .flor {
                    position: absolute;
                    width: 50px;
                    height: 50px;
                    cursor: pointer;
                    user-select: none;
                    transition: transform 0.3s ease, opacity 0.5s ease;
                    filter: drop-shadow(0 0 4px #ba68c8);
                    font-size: 40px;
                }
                .flor.capturada {
                    animation: capturar 0.5s forwards;
                }
                @keyframes capturar {
                    0% {
                        transform: scale(1);
                        opacity: 1;
                        filter: drop-shadow(0 0 4px #ba68c8);
                    }
                    50% {
                        transform: scale(1.5) rotate(15deg);
                        opacity: 0.7;
                        filter: drop-shadow(0 0 10px #f48fb1);
                    }
                    100% {
                        transform: scale(0);
                        opacity: 0;
                        filter: drop-shadow(0 0 20px #f48fb1);
                    }
                }
                #info {
                    font-size: 18px;
                    margin: 10px 0;
                }
                #puntos {
                    font-weight: bold;
                    font-size: 22px;
                }
                #tiempo {
                    font-weight: bold;
                    font-size: 22px;
                }
                .boton {
                    background-color: #5e2c3c;
                    color: white;
                    padding: 10px 25px;
                    border: none;
                    border-radius: 20px;
                    font-size: 18px;
                    cursor: pointer;
                    margin-top: 15px;
                }
                #mensajeFinal {
                    margin-top: 20px;
                    font-size: 24px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>🌸 Nivel 1: Captura las Flores 🌸</h1>
            <div id="info">
                Tiempo: <span id="tiempo">15</span> segundos | Puntos: <span id="puntos">0</span>
            </div>
            <div id="juego"></div>
            <div id="mensajeFinal"></div>
            <button class="boton" id="btn-reiniciar" style="display:none;">Jugar otra vez</button>

            <audio id="audio-captura" src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" preload="auto"></audio>

            <script>
                const juego = document.getElementById('juego');
                const puntosSpan = document.getElementById('puntos');
                const tiempoSpan = document.getElementById('tiempo');
                const mensajeFinal = document.getElementById('mensajeFinal');
                const btnReiniciar = document.getElementById('btn-reiniciar');
                const audioCaptura = document.getElementById('audio-captura');

                let puntos = 0;
                let tiempo = 15;
                let intervaloTiempo;
                let intervaloFlor;
                let juegoActivo = true;

                // Crear flores
                function crearFlor() {
                    const flor = document.createElement('div');
                    flor.classList.add('flor');
                    flor.textContent = "🌸";

                    // Posición inicial aleatoria horizontal (10 a 90 %)
                    flor.style.left = (10 + Math.random() * 80) + 'vw';
                    flor.style.top = '-50px';

                    // Añadir animación caída con duración y retraso aleatorios
                    const duracion = 4000 + Math.random() * 1000; // 4-7 seg
                    flor.style.transition = `top ${duracion}ms linear, transform 0.3s ease`;

                    // Añadir evento click para capturar
                    flor.addEventListener('click', () => {
                        if (!juegoActivo) return;
                        puntos++;
                        puntosSpan.textContent = puntos;
                        audioCaptura.currentTime = 0;
                        audioCaptura.play();
                        flor.classList.add('capturada');
                        setTimeout(() => flor.remove(), 500);
                    });

                    juego.appendChild(flor);

                    // Forzar movimiento con setTimeout
                    setTimeout(() => {
                        flor.style.top = '70vh';
                        flor.style.transform = `rotate(${Math.random()*90 - 45}deg)`;
                    }, 100);

                    // Eliminar flor si llega abajo sin ser capturada
                    setTimeout(() => {
                        if (flor.parentElement) flor.remove();
                    }, duracion + 100);
                }

                // Inicio del juego
                function iniciarJuego() {
                    puntos = 0;
                    tiempo = 20;
                    juegoActivo = true;
                    puntosSpan.textContent = puntos;
                    tiempoSpan.textContent = tiempo;
                    mensajeFinal.textContent = '';
                    btnReiniciar.style.display = 'none';

                    intervaloTiempo = setInterval(() => {
                        tiempo--;
                        tiempoSpan.textContent = tiempo;
                        if (tiempo <= 0) {
                            finalizarJuego();
                        }
                    }, 1000);

                    intervaloFlor = setInterval(() => {
                        if (juegoActivo) crearFlor();
                    }, 800);
                }

                // Fin del juego
                function finalizarJuego() {
                    juegoActivo = false;
                    clearInterval(intervaloTiempo);
                    clearInterval(intervaloFlor);

                    // Eliminar todas las flores restantes
                    document.querySelectorAll('.flor').forEach(f => f.remove());

                    if (puntos >= 10) {
                        mensajeFinal.textContent = "🎉 ¡Nivel completado! 🎉";
                        // Guardar progreso en backend
                        fetch('/completar', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ nivel: 1 })
                        }).then(res => res.json()).then(data => {
                            // Espera 2 segundos y redirige al mapa
                            setTimeout(() => window.location.href = '/mapa', 2000);
                        });
                    } else {
                        mensajeFinal.textContent = "❌ Intenta otra vez. Necesitas al menos 10 flores.";
                        btnReiniciar.style.display = 'inline-block';
                    }
                }

                btnReiniciar.addEventListener('click', iniciarJuego);

                window.onload = iniciarJuego;
            </script>
        </body>
        </html>
        """)
    elif n == 2:
        return render_template_string("""
        <html>
        <head>
            <title>Nivel 2 - Memoria Floral</title>
            <style>
                body {
                    background: linear-gradient(to bottom, #fce4ec, #f3e5f5);
                    font-family: 'Segoe UI', sans-serif;
                    color: #5e2c3c;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    margin: 20px 0;
                }
                #tablero {
                    display: grid;
                    grid-template-columns: repeat(4, 80px);
                    gap: 15px;
                    justify-content: center;
                    margin-top: 20px;
                }
                .carta {
                    width: 80px;
                    height: 80px;
                    font-size: 32px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background-color: #f8bbd0;
                    border-radius: 15px;
                    cursor: pointer;
                    user-select: none;
                    box-shadow: 0 0 10px #ba68c8;
                    transition: background 0.3s ease;
                }
                .carta.volteada {
                    background-color: #fff;
                }
                .carta.encontrada {
                    background-color: #c8e6c9;
                    cursor: default;
                    box-shadow: none;
                }
                #mensaje {
                    margin-top: 20px;
                    font-size: 22px;
                    font-weight: bold;
                }
                .boton {
                    background-color: #5e2c3c;
                    color: white;
                    padding: 10px 25px;
                    border: none;
                    border-radius: 20px;
                    font-size: 18px;
                    cursor: pointer;
                    margin-top: 20px;
                    display: none;
                }
            </style>
        </head>
        <body>
            <h1>🌼 Nivel 2: Memoria Floral 🌼</h1>
            <div id="tablero"></div>
            <div id="mensaje"></div>
            <button id="btn-reiniciar" class="boton">Jugar de nuevo</button>

            <script>
                const flores = ['🌹', '🌻', '🌷', '🌼', '💐', '🥀', '🌺', '🌸'];
                let cartas = flores.concat(flores).sort(() => Math.random() - 0.5);
                const tablero = document.getElementById('tablero');
                const mensaje = document.getElementById('mensaje');
                const btnReiniciar = document.getElementById('btn-reiniciar');

                let primera = null;
                let bloqueo = false;
                let encontrados = 0;

                function crearTablero() {
                    tablero.innerHTML = '';
                    cartas.forEach((flor, i) => {
                        const carta = document.createElement('div');
                        carta.classList.add('carta');
                        carta.dataset.flor = flor;
                        carta.dataset.index = i;
                        carta.addEventListener('click', voltearCarta);
                        tablero.appendChild(carta);
                    });
                }

                function voltearCarta(e) {
                    if (bloqueo) return;
                    const carta = e.currentTarget;
                    if (carta.classList.contains('volteada') || carta.classList.contains('encontrada')) return;

                    carta.textContent = carta.dataset.flor;
                    carta.classList.add('volteada');

                    if (!primera) {
                        primera = carta;
                    } else {
                        bloqueo = true;
                        setTimeout(() => {
                            if (primera.dataset.flor === carta.dataset.flor) {
                                primera.classList.add('encontrada');
                                carta.classList.add('encontrada');
                                encontrados += 2;
                                if (encontrados === cartas.length) {
    mensaje.textContent = "🎉 ¡Nivel completado!";
    btnReiniciar.style.display = "inline-block";
    fetch('/completar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nivel: 2 })
    }).then(res => res.json()).then(data => {
        setTimeout(() => {
            window.location.href = '/mapa';
        }, 2000);
    });
}

                            } else {
                                primera.textContent = '';
                                carta.textContent = '';
                                primera.classList.remove('volteada');
                                carta.classList.remove('volteada');
                            }
                            primera = null;
                            bloqueo = false;
                        }, 800);
                    }
                }

                btnReiniciar.addEventListener('click', () => {
                    cartas = flores.concat(flores).sort(() => Math.random() - 0.5);
                    encontrados = 0;
                    mensaje.textContent = '';
                    btnReiniciar.style.display = 'none';
                    crearTablero();
                });

                crearTablero();
            </script>
        </body>
        </html>
        """)
    
    elif n == 3:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 3 - Laberinto de la Abeja</title>
        <style>
            body {
                background: #fff8e1;
                font-family: sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            h1 {
                padding-top: 20px;
                color: #6d4c41;
            }
            #laberinto {
                display: grid;
                grid-template-columns: repeat(10, 40px);
                justify-content: center;
                gap: 2px;
                margin-top: 20px;
            }
            .celda {
                width: 40px;
                height: 40px;
                font-size: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                user-select: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .pared {
                background-color: #8d6e63;
            }
            .camino {
                background-color: #fffde7;
            }
            .meta {
                background-color: #ffe082;
            }
            .abeja {
                background-color: #fff59d;
            }
            #mensaje {
                margin-top: 20px;
                font-size: 22px;
                font-weight: bold;
                color: #4e342e;
            }
        </style>
    </head>
    <body>
        <h1>🐝 Nivel 3: Guía a la abeja hasta la miel 🍯</h1>
        <div id="laberinto"></div>
        <div id="mensaje"></div>

        <script>
            const mapa = [
                "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛",
                "⬛⬜⬜⬜⬛⬜⬜⬜⬜⬛",
                "⬛⬜⬛⬜⬛⬜⬛⬛⬜⬛",
                "⬛⬜⬛⬜⬜⬜⬛⬜⬜⬛",
                "⬛⬜⬛⬛⬛⬜⬛⬜⬛⬛",
                "⬛⬜⬜⬜⬛⬜⬛⬜⬜⬜",
                "⬛⬛⬛⬜⬛⬛⬛⬛⬛⬜",
                "⬛⬜⬜⬜⬛⬜⬜⬛⬛⬜",
                "⬛⬜⬛⬛⬛⬜⬛⬛⬜⬜",
                "⬛⬜⬜⬜⬜⬜⬛⬛🍯⬛"
            ];

            const laberinto = document.getElementById("laberinto");
            const mensaje = document.getElementById("mensaje");
            let celdas = [];⬛

            // Crear el tablero
            mapa.forEach((fila, y) => {
                [...fila].forEach((celda, x) => {
                    const div = document.createElement("div");
                    div.classList.add("celda");
                    if (celda === "⬛") {
                        div.classList.add("pared");
                        div.dataset.tipo = "pared";
                    } else if (celda === "⬜") {
                        div.classList.add("camino");
                        div.dataset.tipo = "camino";
                    } else if (celda === "🍯") {
                        div.classList.add("meta");
                        div.textContent = "🍯";
                        div.dataset.tipo = "meta";
                    }
                    div.dataset.x = x;
                    div.dataset.y = y;
                    laberinto.appendChild(div);
                    celdas.push(div);
                });
            });

            // Posición inicial
            let posX = 1;
            let posY = 1;
            getCelda(posX, posY).classList.add("abeja");
            getCelda(posX, posY).textContent = "🐝";

            function getCelda(x, y) {
                return celdas[y * 10 + x];
            }

            function moverAbeja(x, y) {
                const destino = getCelda(x, y);
                if (!destino || destino.dataset.tipo === "pared") return;

                // Limpiar anterior
                const actual = getCelda(posX, posY);
                actual.textContent = "";
                actual.classList.remove("abeja");

                // Mover
                posX = x;
                posY = y;
                destino.classList.add("abeja");
                destino.textContent = "🐝";

                // Verificar meta
                if (destino.dataset.tipo === "meta") {
                    mensaje.textContent = "🎉 ¡Nivel completado!";
                    fetch('/completar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nivel: 3 })
                    }).then(res => res.json()).then(data => {
                        setTimeout(() => {
                            window.location.href = '/mapa';
                        }, 2000);
                    });
                }
            }

            // Movimiento con mouse o touch
            laberinto.addEventListener("mousemove", (e) => {
                const celda = e.target;
                if (!celda.classList.contains("celda")) return;
                const x = parseInt(celda.dataset.x);
                const y = parseInt(celda.dataset.y);
                if (Math.abs(x - posX) + Math.abs(y - posY) === 1) {
                    moverAbeja(x, y);
                }
            });

            laberinto.addEventListener("touchmove", (e) => {
                const touch = e.touches[0];
                const target = document.elementFromPoint(touch.clientX, touch.clientY);
                if (!target || !target.classList.contains("celda")) return;
                const x = parseInt(target.dataset.x);
                const y = parseInt(target.dataset.y);
                if (Math.abs(x - posX) + Math.abs(y - posY) === 1) {
                    moverAbeja(x, y);
                }
            });
        </script>
    </body>
    </html>
    """)

    elif n == 4:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 4 - Carrera del Gusanito</title>
        <style>
            body {
                background: linear-gradient(to bottom, #e8f5e9, #a5d6a7);
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
            h1 {
                margin-top: 20px;
                color: #2e7d32;
            }
            #zona-juego {
                width: 100vw;
                height: 80vh;
                position: relative;
                margin: 20px auto;
                border: 5px dashed #66bb6a;
                background-color: #f1f8e9;
                overflow: hidden;
            }
            #gusano, #meta, .piedra, .obstaculo {
                position: absolute;
                font-size: 36px;
                user-select: none;
                pointer-events: none;
            }
            #gusano {
                z-index: 3;
                cursor: grab;
                pointer-events: auto;
            }
            .piedra {
                z-index: 2;
                animation: caer 4s linear infinite;
            }
            .obstaculo {
                z-index: 1;
            }
            #mensaje {
                font-size: 24px;
                color: #2e7d32;
                font-weight: bold;
                margin-top: 20px;
                min-height: 30px;
            }
        </style>
    </head>
    <body>
        <h1>🐛 Nivel 4: Carrera del Gusanito 🍃</h1>
        <div id="zona-juego">
            <div id="gusano" style="left: 20px; top: 20px;">🐛</div>
            <div id="meta" style="right: 20px; bottom: 20px;">🍃</div>
        </div>
        <div id="mensaje"></div>

        <script>
            const zona = document.getElementById("zona-juego");
            const gusano = document.getElementById("gusano");
            const meta = document.getElementById("meta");
            const mensaje = document.getElementById("mensaje");

            let offsetX = 0;
            let offsetY = 0;
            let arrastrando = false;

            // Solo se puede mover el gusano cuando lo tocan/arrastran
            gusano.addEventListener('mousedown', e => {
                arrastrando = true;
                offsetX = e.clientX - gusano.offsetLeft;
                offsetY = e.clientY - gusano.offsetTop;
                gusano.style.cursor = 'grabbing';
                e.preventDefault();
            });
            gusano.addEventListener('touchstart', e => {
                arrastrando = true;
                const touch = e.touches[0];
                offsetX = touch.clientX - gusano.offsetLeft;
                offsetY = touch.clientY - gusano.offsetTop;
                e.preventDefault();
            });

            window.addEventListener('mouseup', e => {
                arrastrando = false;
                gusano.style.cursor = 'grab';
            });
            window.addEventListener('touchend', e => {
                arrastrando = false;
            });

            zona.addEventListener('mousemove', e => {
                if (!arrastrando) return;
                moverGusano(e.clientX, e.clientY);
            });
            zona.addEventListener('touchmove', e => {
                if (!arrastrando) return;
                if (e.touches.length > 0) {
                    moverGusano(e.touches[0].clientX, e.touches[0].clientY);
                }
            });

            function moverGusano(x, y) {
                const zonaRect = zona.getBoundingClientRect();
                let gx = x - zonaRect.left - offsetX;
                let gy = y - zonaRect.top - offsetY;

                // Limitar dentro de zona-juego
                gx = Math.max(0, Math.min(zona.clientWidth - gusano.offsetWidth, gx));
                gy = Math.max(0, Math.min(zona.clientHeight - gusano.offsetHeight, gy));

                gusano.style.left = gx + 'px';
                gusano.style.top = gy + 'px';

                verificarMeta();
                verificarPiedras();
                verificarObstaculos();
            }

            function verificarColision(r1, r2) {
                return r1.left < r2.right && r1.right > r2.left &&
                    r1.top < r2.bottom && r1.bottom > r2.top;
            }

            function verificarMeta() {
                const gRect = gusano.getBoundingClientRect();
                const mRect = meta.getBoundingClientRect();

                if (verificarColision(gRect, mRect)) {
                    mensaje.textContent = "🎉 ¡Nivel completado!";
                    fetch('/completar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nivel: 4 })
                    }).then(res => res.json()).then(data => {
                        setTimeout(() => {
                            window.location.href = '/mapa';
                        }, 2000);
                    });
                }
            }

            function verificarPiedras() {
                const gRect = gusano.getBoundingClientRect();
                const piedras = document.querySelectorAll('.piedra');

                piedras.forEach(piedra => {
                    const pRect = piedra.getBoundingClientRect();
                    if (verificarColision(gRect, pRect)) {
                        mensaje.textContent = "💥 ¡Te golpeó una piedra!";
                        setTimeout(() => location.reload(), 1000);
                    }
                });
            }

            function verificarObstaculos() {
                const gRect = gusano.getBoundingClientRect();
                const obstaculos = document.querySelectorAll('.obstaculo');

                obstaculos.forEach(obs => {
                    const oRect = obs.getBoundingClientRect();
                    if (verificarColision(gRect, oRect)) {
                        mensaje.textContent = "🚧 ¡Te chocaste con un obstáculo!";
                        setTimeout(() => location.reload(), 1000);
                    }
                });
            }

            function iniciarPiedras() {
                setInterval(() => {
                    const piedra = document.createElement('div');
                    piedra.className = 'piedra';
                    piedra.textContent = '🪨';

                    const zonaWidth = zona.clientWidth;
                    const randomX = Math.floor(Math.random() * (zonaWidth - 30));
                    piedra.style.left = randomX + 'px';
                    piedra.style.top = '0px';

                    zona.appendChild(piedra);

                    let y = 0;
                    const velocidad = 4 + Math.random() * 5;

                    const mover = setInterval(() => {
                        y += velocidad;
                        piedra.style.top = y + 'px';

                        if (y > zona.clientHeight) {
                            clearInterval(mover);
                            piedra.remove();
                        } else {
                            verificarPiedras();
                        }
                    }, 20);
                }, 200);
            }

            window.addEventListener('load', () => {
                iniciarPiedras();
            });
        </script>
    </body>
    </html>
    """)

    elif n == 5:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 5 - Recolección de Polen</title>
        <style>
            body {
                background: linear-gradient(to bottom, #fffde7, #fff9c4);
                font-family: 'Segoe UI', sans-serif;
                color: #5e2c3c;
                text-align: center;
                margin: 0;
                padding: 0;
                overflow: hidden;
                user-select: none;
            }
            h1 {
                margin: 20px 0;
            }
            #juego {
                position: relative;
                width: 480px;
                height: 320px;
                margin: 0 auto;
                border: 3px solid #a1887f;
                border-radius: 15px;
                background: linear-gradient(to bottom, #e8f5e9, #c8e6c9);
                overflow: hidden;
            }
            #abeja {
                position: absolute;
                font-size: 40px;
                user-select: none;
                pointer-events: none;
                left: 220px;
                top: 140px;
                transition: left 0.05s linear, top 0.05s linear;
                z-index: 10;
            }
            .polen {
                position: absolute;
                font-size: 28px;
                user-select: none;
                pointer-events: none;
                animation: caer linear forwards;
                z-index: 5;
            }
            @keyframes caer {
                0% { top: -30px; }
                100% { top: 350px; }
            }
            #info {
                margin-top: 10px;
                font-size: 20px;
                font-weight: bold;
            }
            #mensaje {
                margin-top: 20px;
                font-size: 24px;
                color: #388e3c;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🐝 Nivel 5: Recolección de Polen 🌼</h1>
        <div id="juego">
            <div id="abeja">🐝</div>
        </div>
        <div id="info">Polen recolectado: <span id="contador">0</span> / 20</div>
        <div id="mensaje"></div>

        <script>
            const juego = document.getElementById('juego');
            const abeja = document.getElementById('abeja');
            const contadorSpan = document.getElementById('contador');
            const mensaje = document.getElementById('mensaje');

            let ancho = juego.clientWidth;
            let alto = juego.clientHeight;

            let polenRecolectado = 0;
            const objetivo = 20;
            const tiempoLimite = 60000; // 60 segundos

            // Posición inicial de la abeja
            let abejaX = ancho / 2 - 20;
            let abejaY = alto / 2 - 20;

            abeja.style.left = abejaX + 'px';
            abeja.style.top = abejaY + 'px';

            // Viento lateral: movimiento aleatorio que afecta abeja
            function viento() {
                return (Math.random() - 0.5) * 4; // -2 a +2 px
            }

            // Manejar control con mouse o tactil
            function moverAbeja(x, y) {
                // Viento
                const desplazamientoX = viento();

                // Limitar dentro del área
                abejaX = x - juego.getBoundingClientRect().left + desplazamientoX;
                abejaY = y - juego.getBoundingClientRect().top;

                if (abejaX < 0) abejaX = 0;
                if (abejaX > ancho - 40) abejaX = ancho - 40;
                if (abejaY < 0) abejaY = 0;
                if (abejaY > alto - 40) abejaY = alto - 40;

                abeja.style.left = abejaX + 'px';
                abeja.style.top = abejaY + 'px';

                // Chequear si toca polen
                chequearPolen();
            }

            // Crear polen que cae
            const polenes = [];
            const polenEmojis = ['🌸', '🌻', '🌷', '🌼', '💐', '🌹'];

            function crearPolen() {
                const polen = document.createElement('div');
                polen.classList.add('polen');
                polen.textContent = polenEmojis[Math.floor(Math.random() * polenEmojis.length)];
                polen.style.left = Math.random() * (ancho - 28) + 'px';
                polen.style.top = '-30px';

                // Duración aleatoria para caer entre 4 y 7 segundos
                const duracion = 4000 + Math.random() * 3000;
                polen.style.animationDuration = duracion + 'ms';

                juego.appendChild(polen);
                polenes.push({elemento: polen, duracion, inicio: Date.now(), recogido: false});
            }

            // Crear polen cada 700 ms
            let crearInterval = setInterval(crearPolen, 700);

            // Función que actualiza posición y revisa colisiones
            function actualizar() {
                const ahora = Date.now();

                for (let i = polenes.length - 1; i >= 0; i--) {
                    let p = polenes[i];
                    const progreso = (ahora - p.inicio) / p.duracion;
                    if (progreso >= 1) {
                        // Se fue fuera del juego, remover
                        if (!p.recogido) {
                            juego.removeChild(p.elemento);
                        }
                        polenes.splice(i, 1);
                        continue;
                    }
                    // Actualizamos posición top:
                    const top = progreso * (alto + 30) - 30;
                    p.elemento.style.top = top + 'px';
                }

                requestAnimationFrame(actualizar);
            }
            actualizar();

            // Chequear colisiones abeja-polén
            function chequearPolen() {
                for (let i = polenes.length - 1; i >= 0; i--) {
                    const p = polenes[i];
                    if (p.recogido) continue;

                    const rectPolen = p.elemento.getBoundingClientRect();
                    const rectAbeja = abeja.getBoundingClientRect();

                    const overlap = !(rectAbeja.right < rectPolen.left ||
                        rectAbeja.left > rectPolen.right ||
                        rectAbeja.bottom < rectPolen.top ||
                        rectAbeja.top > rectPolen.bottom);

                    if (overlap) {
                        // Recogemos polen
                        p.recogido = true;
                        juego.removeChild(p.elemento);
                        polenes.splice(i, 1);
                        polenRecolectado++;
                        contadorSpan.textContent = polenRecolectado;

                        if (polenRecolectado >= objetivo) {
                            terminarNivel();
                        }
                    }
                }
            }

            // Finalizar nivel
            function terminarNivel() {
                clearInterval(crearInterval);
                mensaje.textContent = "🎉 ¡Nivel completado!";
                // Bloquear control moviendo la abeja fuera del área
                abeja.style.pointerEvents = 'none';

                fetch('/completar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nivel: 5 })
                }).then(res => res.json()).then(data => {
                    setTimeout(() => {
                        window.location.href = '/mapa';
                    }, 2500);
                });
            }

            // Control con mouse
            juego.addEventListener('mousemove', e => {
                moverAbeja(e.clientX, e.clientY);
            });

            // Control táctil
            juego.addEventListener('touchmove', e => {
                if (e.touches.length > 0) {
                    moverAbeja(e.touches[0].clientX, e.touches[0].clientY);
                }
                e.preventDefault();
            }, { passive: false });

        </script>
    </body>
    </html>
    """)

    elif n == 6:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 6 - Flores Musicales</title>
        <style>
            body {
                background: linear-gradient(to bottom, #e0f7fa, #fce4ec);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #2e3d49;
                text-align: center;
                margin: 0; padding: 0;
            }
            h1 {
                margin: 20px 0;
                font-weight: 700;
            }
            #mensaje {
                margin-top: 20px;
                font-size: 24px;
                font-weight: bold;
                color: #388e3c;
            }
            #tablero {
                display: grid;
                grid-template-columns: repeat(4, 100px);
                grid-gap: 15px;
                justify-content: center;
                margin-top: 30px;
            }
            .flor {
                font-size: 64px;
                padding: 15px;
                background-color: #f8bbd0;
                border-radius: 20px;
                box-shadow: 0 0 15px #ba68c8;
                cursor: pointer;
                user-select: none;
                transition: transform 0.2s ease, box-shadow 0.3s ease;
            }
            .flor.activada {
                background-color: #fff59d;
                box-shadow: 0 0 30px #fbc02d;
                transform: scale(1.3);
            }
            button {
                margin-top: 30px;
                padding: 12px 30px;
                font-size: 18px;
                border-radius: 25px;
                border: none;
                background-color: #d81b60;
                color: white;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #ad1457;
            }
        </style>
    </head>
    <body>
        <h1>🎶 Nivel 6: Flores Musicales 🎶</h1>
        <div id="mensaje">Mira y repite la secuencia</div>
        <div id="tablero"></div>
        <button id="btn-reiniciar" style="display:none;">Jugar de nuevo</button>

        <script>
            const flores = ['🌹', '🌻', '🌷', '🌼'];
            const notasFrecuencia = [261.63, 329.63, 392.00, 523.25]; // Do, Mi, Sol, Do alto

            const tablero = document.getElementById('tablero');
            const mensaje = document.getElementById('mensaje');
            const btnReiniciar = document.getElementById('btn-reiniciar');

            let secuencia = [];
            let jugadorSecuencia = [];
            let turnoJugador = false;
            let nivel = 1;

            // Web Audio API para sonidos
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

            function sonarNota(freq) {
                const osc = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                osc.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                osc.type = 'sine';
                osc.frequency.value = freq;
                osc.start();
                gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
                osc.stop(audioCtx.currentTime + 0.5);
            }

            function crearTablero() {
                tablero.innerHTML = '';
                flores.forEach((flor, i) => {
                    const div = document.createElement('div');
                    div.classList.add('flor');
                    div.textContent = flor;
                    div.dataset.index = i;
                    div.addEventListener('click', jugadorClick);
                    div.addEventListener('touchstart', e => { e.preventDefault(); jugadorClick(e); }, { passive: false });
                    tablero.appendChild(div);
                });
            }

            function activarFlor(i) {
                return new Promise(resolve => {
                    const div = tablero.children[i];
                    div.classList.add('activada');
                    sonarNota(notasFrecuencia[i]);
                    setTimeout(() => {
                        div.classList.remove('activada');
                        setTimeout(resolve, 200);
                    }, 600);
                });
            }

            async function mostrarSecuencia() {
                turnoJugador = false;
                mensaje.textContent = `Nivel ${nivel}: Observa la secuencia`;
                for (let i = 0; i < secuencia.length; i++) {
                    await activarFlor(secuencia[i]);
                }
                turnoJugador = true;
                jugadorSecuencia = [];
                mensaje.textContent = `Nivel ${nivel}: Repite la secuencia`;
            }

            function agregarASecuencia() {
                const rand = Math.floor(Math.random() * flores.length);
                secuencia.push(rand);
            }

            async function iniciarJuego() {
                secuencia = [];
                jugadorSecuencia = [];
                nivel = 1;
                btnReiniciar.style.display = 'none';
                mensaje.textContent = 'Mira y repite la secuencia';
                agregarASecuencia();
                await mostrarSecuencia();
            }

            async function jugadorClick(e) {
                if (!turnoJugador) return;
                const idx = parseInt(e.currentTarget.dataset.index);
                jugadorSecuencia.push(idx);
                await activarFlor(idx);
                const posicion = jugadorSecuencia.length - 1;
                if (jugadorSecuencia[posicion] !== secuencia[posicion]) {
                    mensaje.textContent = '❌ Secuencia incorrecta, intenta de nuevo';
                    turnoJugador = false;
                    btnReiniciar.style.display = 'inline-block';
                    return;
                }
                if (jugadorSecuencia.length === secuencia.length) {
                    if (nivel === 8) {
                        mensaje.textContent = '🎉 ¡Nivel completado!';
                        turnoJugador = false;
                        btnReiniciar.style.display = 'inline-block';
                        // Avisar backend y volver a mapa
                        fetch('/completar', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ nivel: 6 })
                        }).then(() => {
                            setTimeout(() => window.location.href = '/mapa', 2000);
                        });
                        return;
                    }
                    nivel++;
                    mensaje.textContent = '✅ ¡Correcto! Preparando siguiente nivel...';
                    turnoJugador = false;
                    await new Promise(r => setTimeout(r, 1200));
                    agregarASecuencia();
                    await mostrarSecuencia();
                }
            }

            btnReiniciar.addEventListener('click', iniciarJuego);

            crearTablero();
            iniciarJuego();
        </script>
    </body>
    </html>
    """)

    elif n == 7:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 6 - Caza de Mariposas</title>
        <style>
            body {
                background: linear-gradient(to bottom, #d0f0fd, #a2d5f2);
                font-family: 'Segoe UI', sans-serif;
                color: #3a2e2e;
                margin: 0;
                overflow: hidden;
                user-select: none;
            }
            h1 {
                text-align: center;
                margin: 15px 0;
                color: #3a2e2e;
            }
            #juego {
                position: relative;
                width: 100vw;
                height: 80vh;
                margin: auto;
                background: linear-gradient(to top, #6fcf97, #a2d5f2);
                border: 3px solid #5e2c3c;
                border-radius: 15px;
                overflow: hidden;
            }
            .mariposa {
                position: absolute;
                font-size: 40px;
                user-select: none;
                pointer-events: none;
            }
            #canasta {
                position: absolute;
                bottom: 5px;
                left: 50%;
                transform: translateX(-50%);
                font-size: 60px;
                user-select: none;
            }
            #info {
                text-align: center;
                margin: 10px 0;
                font-size: 20px;
                font-weight: bold;
                color: #3a2e2e;
            }
            #mensaje {
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                margin-top: 10px;
                color: #5e2c3c;
                min-height: 30px;
            }
        </style>
    </head>
    <body>
        <h1>🦋 Nivel 6: Caza de Mariposas 🦋</h1>
        <div id="info">Mariposas atrapadas: <span id="contador">0</span> / 10 | Tiempo restante: <span id="tiempo">20</span>s</div>
        <div id="juego">
            <div id="canasta">🧺</div>
        </div>
        <div id="mensaje"></div>

        <script>
            const juego = document.getElementById('juego');
            const canasta = document.getElementById('canasta');
            const contadorElem = document.getElementById('contador');
            const tiempoElem = document.getElementById('tiempo');
            const mensaje = document.getElementById('mensaje');

            const ancho = window.innerWidth;
            const alto = window.innerHeight * 0.8;

            let atrapadas = 0;
            let tiempo = 20;
            let mariposas = [];
            let juegoActivo = true;

            // Mover la canasta con mouse/touch
            function moverCanasta(e) {
                if (!juegoActivo) return;
                let x = e.clientX || (e.touches && e.touches[0].clientX);
                if (x < 30) x = 30;
                if (x > window.innerWidth - 30) x = window.innerWidth - 30;
                canasta.style.left = x + 'px';
            }

            window.addEventListener('mousemove', moverCanasta);
            window.addEventListener('touchmove', moverCanasta);

            // Crear mariposas que caen del cielo
            function crearMariposa() {
                if (!juegoActivo) return;
                const m = document.createElement('div');
                m.classList.add('mariposa');
                m.textContent = '🦋';
                m.style.left = Math.random() * (juego.clientWidth - 40) + 'px';
                m.style.top = '-50px';
                juego.appendChild(m);
                mariposas.push({el: m, velocidad: 1 + Math.random() * 2});
            }

            // Chequear colisiones entre canasta y mariposas
            function colision(r1, r2) {
                return !(r2.left > r1.right || 
                        r2.right < r1.left || 
                        r2.top > r1.bottom || 
                        r2.bottom < r1.top);
            }

            // Actualizar posición mariposas y verificar captura
            function actualizar() {
                if (!juegoActivo) return;
                for (let i = mariposas.length - 1; i >= 0; i--) {
                    let m = mariposas[i];
                    let top = parseFloat(m.el.style.top);
                    top += m.velocidad;
                    m.el.style.top = top + 'px';

                    if (top > alto) {
                        // Mariposa cayó sin atrapar, se elimina
                        juego.removeChild(m.el);
                        mariposas.splice(i, 1);
                        continue;
                    }

                    // Revisar colisión con canasta
                    const canastaRect = canasta.getBoundingClientRect();
                    const mRect = m.el.getBoundingClientRect();
                    if (colision(canastaRect, mRect)) {
                        // Atrapó la mariposa
                        atrapadas++;
                        contadorElem.textContent = atrapadas;
                        juego.removeChild(m.el);
                        mariposas.splice(i, 1);

                        if (atrapadas === 10) {
                            terminarJuego(true);
                        }
                    }
                }
            }

            // Temporizador
            function actualizarTiempo() {
                if (!juegoActivo) return;
                tiempo--;
                tiempoElem.textContent = tiempo;
                if (tiempo <= 0) {
                    terminarJuego(false);
                }
            }

            // Terminar juego
            function terminarJuego(gano) {
                juegoActivo = false;
                if (gano) {
                    mensaje.textContent = "🎉 ¡Nivel completado!";
                    fetch('/completar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nivel: 7 })
                    }).then(res => res.json()).then(data => {
                        setTimeout(() => {
                            window.location.href = '/mapa';
                        }, 2500);
                    });
                } else {
                    mensaje.textContent = "⏰ Tiempo terminado. Intenta de nuevo.";
                }
            }

            // Ciclo principal
            function ciclo() {
                if (!juegoActivo) return;
                if (Math.random() < 0.15) crearMariposa();
                actualizar();
                requestAnimationFrame(ciclo);
            }

            // Iniciar temporizador
            setInterval(actualizarTiempo, 1000);

            ciclo();
        </script>
    </body>
    </html>
    """)

    elif n == 8:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 8 - Trivia Floral</title>
        <style>
            body {
                background: linear-gradient(to bottom, #e0f7fa, #80deea);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #004d40;
                text-align: center;
                margin: 0;
                padding: 20px;
            }
            h1 {
                margin-bottom: 15px;
            }
            #pregunta {
                font-size: 24px;
                margin-bottom: 20px;
            }
            .opcion {
                display: block;
                background-color: #a5d6a7;
                margin: 10px auto;
                padding: 12px 20px;
                width: 300px;
                border-radius: 15px;
                font-size: 20px;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                user-select: none;
                transition: background-color 0.3s ease;
            }
            .opcion:hover {
                background-color: #81c784;
            }
            #mensaje {
                margin-top: 25px;
                font-size: 22px;
                font-weight: bold;
                min-height: 30px;
            }
        </style>
    </head>
    <body>
        <h1>🌸 Nivel 8: Trivia Floral 🌸</h1>
        <div id="pregunta"></div>
        <div id="opciones"></div>
        <div id="mensaje"></div>

        <script>
            const preguntas = [
                {
                    pregunta: "¿Cuál es la función principal del polen en las flores? 🌼",
                    opciones: ["A) Alimentar a las abejas", "B) Reproducción", "C) Fotosíntesis", "D) Dar color a la flor"],
                    correcta: 1
                },
                {
                    pregunta: "¿Qué insecto es conocido por polinizar flores? 🐝",
                    opciones: ["A) Hormiga", "B) Mariposa", "C) Abeja", "D) Mosca"],
                    correcta: 2
                },
                {
                    pregunta: "¿Qué color tiene la mayoría de las flores para atraer polinizadores? 🌷",
                    opciones: ["A) Verde", "B) Rojo o colores vivos", "C) Marrón", "D) Negro"],
                    correcta: 1
                }
            ];

            let indice = 0;
            const preguntaDiv = document.getElementById('pregunta');
            const opcionesDiv = document.getElementById('opciones');
            const mensajeDiv = document.getElementById('mensaje');

            function mostrarPregunta() {
                mensajeDiv.textContent = "";
                const p = preguntas[indice];
                preguntaDiv.textContent = p.pregunta;
                opcionesDiv.innerHTML = "";
                p.opciones.forEach((opcion, i) => {
                    const btn = document.createElement('button');
                    btn.textContent = opcion;
                    btn.className = "opcion";
                    btn.onclick = () => verificarRespuesta(i);
                    opcionesDiv.appendChild(btn);
                });
            }

            function verificarRespuesta(opcionSeleccionada) {
                if(opcionSeleccionada === preguntas[indice].correcta) {
                    indice++;
                    if(indice >= preguntas.length) {
                        mensajeDiv.textContent = "🎉 ¡Nivel completado! Volviendo al mapa...";
                        fetch('/completar', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ nivel: 8 })
                        }).then(res => res.json()).then(data => {
                            setTimeout(() => { window.location.href = '/mapa'; }, 2500);
                        });
                    } else {
                        mostrarPregunta();
                    }
                } else {
                    mensajeDiv.textContent = "❌ Respuesta incorrecta. Intenta de nuevo.";
                }
            }

            mostrarPregunta();
        </script>
    </body>
    </html>
    """)

    elif n == 9:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 9 - Mensaje Especial</title>
        <style>
            body {
                background: linear-gradient(to bottom, #fff3e0, #ffe0b2);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #6d4c41;
                text-align: center;
                margin: 0;
                padding: 40px 20px;
            }
            button {
                background-color: #ffb74d;
                border: none;
                border-radius: 25px;
                padding: 15px 40px;
                font-size: 22px;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(255, 183, 77, 0.6);
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #ffa726;
            }
            #carta {
                margin: 40px auto 0;
                max-width: 400px;
                background: #fff3e0;
                border-radius: 20px;
                padding: 30px 25px;
                box-shadow: 0 6px 15px rgba(0,0,0,0.1);
                font-size: 20px;
                color: #5d4037;
                display: none;
                animation: desplegar 0.6s ease forwards;
                line-height: 1.5;
                font-style: italic;
            }
            @keyframes desplegar {
                from {
                    opacity: 0;
                    transform: scale(0.8);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            #btn-regresar {
                margin-top: 30px;
                background-color: #a1887f;
                padding: 12px 28px;
                font-size: 18px;
                border-radius: 20px;
                color: white;
                border: none;
                cursor: pointer;
                display: none;
                box-shadow: 0 4px 8px rgba(161,136,127,0.7);
                transition: background-color 0.3s ease;
            }
            #btn-regresar:hover {
                background-color: #8d6e63;
            }
        </style>
    </head>
    <body>
        <h1>🌷 Nivel 9: Mensaje Especial 🌷</h1>
        <button id="btn-lista">¿Lista?</button>

        <div id="carta">
            <p>
                Me encanta tu sonrisa porque ilumina todo a tu alrededor, tu cabello rojo es tan vibrante y hermoso como tú, tus tatuajes te hacen única y me fascinan cada detalle de tu cuerpo, que es simplemente perfecto para mí, me haces sentir tan feliz y afortunado de tenerte cerca, eres mi alegría diaria y la persona que más quiero.
            </p>
            <button id="btn-regresar">Volver al mapa</button>
        </div>

        <script>
            const btnLista = document.getElementById('btn-lista');
            const carta = document.getElementById('carta');
            const btnRegresar = document.getElementById('btn-regresar');

            btnLista.onclick = () => {
                btnLista.style.display = 'none';
                carta.style.display = 'block';
                btnRegresar.style.display = 'inline-block';
            };

            btnRegresar.onclick = () => {
                fetch('/completar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nivel: 10 })
                }).then(res => res.json()).then(data => {
                    window.location.href = '/mapa';
                });
            };
        </script>
    </body>
    </html>
    """)

    elif n == 10:
        return render_template_string("""
    <html>
    <head>
        <title>Nivel 10 - Ramo y Sorpresa</title>
        <style>
            body {
                background: linear-gradient(to bottom, #ffe6f0, #fce4ec);
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
                color: #a02c58;
                margin: 0; padding: 0;
            }
            h1 {
                margin: 20px 0;
            }
            #mensaje {
                font-size: 24px;
                margin: 20px auto;
                max-width: 600px;
                display: none;
            }
            #ramo {
                margin: 20px auto;
                font-size: 32px;
                line-height: 0.8;
                user-select: none;
                white-space: pre;
                display: none;
            }
            button {
                background-color: #a02c58;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px 30px;
                font-size: 20px;
                cursor: pointer;
                margin: 10px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #7a1f42;
            }
        </style>
    </head>
    <body>
        <h1>🎉 Nivel 10: Sorpresa Final 🎉</h1>
        <button id="btn-presiona">Presiona</button>
        
        <div id="mensaje">
            Te quiero mucho, Eli y estas 25 rosas, son para ti ❤️
        </div>
        
        <pre id="ramo"></pre>
        
        <button id="btn-play" style="display:none;">▶️ Reproducir canción</button>
        
        <script>
            const btnPresiona = document.getElementById('btn-presiona');
            const mensaje = document.getElementById('mensaje');
            const ramo = document.getElementById('ramo');
            const btnPlay = document.getElementById('btn-play');

            // Pirámide con 25 rosas (5 filas)
            const filas = [
                "    🌹🌹🌹    ",
                "   🌹🌹🌹🌹   ",
                "  🌹🌹🌹🌹🌹  ",
                " 🌹🌹🌹🌹🌹🌹 ",
                "🌹🌹🌹🌹🌹🌹🌹"
            ];

            btnPresiona.onclick = () => {
                btnPresiona.style.display = 'none';
                mensaje.style.display = 'block';
                ramo.style.display = 'block';
                btnPlay.style.display = 'inline-block';

                // Mostrar ramo en forma pirámide
                ramo.textContent = filas.join('\\n');
            };

            btnPlay.onclick = () => {
                // Abrir YouTube en nueva pestaña, minuto 1:47 (107s)
                window.open('https://youtu.be/LtT6QOShtWM?t=107', '_blank');
                btnPlay.disabled = true;
                btnPlay.textContent = "🎵 Canción abierta";
            };
        </script>
    </body>
    </html>
    """)


@app.route('/completar', methods=['POST'])
def completar():
    datos = request.json
    nivel = datos['nivel']
    progreso = leer_progreso()

    if nivel >= progreso['nivel_actual']:
        progreso['nivel_actual'] = nivel + 1 if nivel < 10 else 10
        progreso['puntos'] += 10
        guardar_progreso(progreso)

    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True)
