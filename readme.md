<p align="center">
  <img src="images/IMG-20260116-WA0016.jpg" alt="WebPTY Neural Console" width="100%">
</p>
# WebPTY – Neural Console

WebPTY é uma interface de terminal web em **tempo real**, construída com **Flask** no backend e **HTML/CSS/JavaScript puro** no frontend, focada em **diagnóstico de sistema**, **execução local de comandos** e **visualização estilo console real**, com compatibilidade total entre **Linux** e **Android (Termux)**.

> Projeto voltado para estudo de sistemas, interfaces low-level, automação local e engenharia reversa de ambientes.

---

## ✨ Funcionalidades

- **Terminal web interativo** (prompt real)
- Execução local de comandos via Flask
- Detecção automática de ambiente (Linux / Android / Termux)
- Painel de **System Status** em tempo real
- Coleta direta de dados via `/proc`
- Compatível com **ARM / x86**
- Layout **responsivo** (Desktop + Mobile)
- Modo tela cheia (landscape)
- Sem frameworks frontend (zero dependências externas)
- Interface inspirada em consoles reais (não fake HUD)

---

## 🧠 Arquitetura

```

WebPTY/
├── app.py                # Backend Flask
├── templates/
│   └── index.html       # Interface principal
├── static/
│   └── app.js           # Lógica do terminal (JS)
└── README.md

```

---

## ⚙️ Tecnologias Utilizadas

### Backend
- Python 3
- Flask
- subprocess
- Leitura direta de `/proc`

### Frontend
- HTML5
- CSS3 (Grid / Flex / Media Queries)
- JavaScript (Vanilla)
- Canvas API (waveform)

---

## 🚀 Instalação

### Linux
```bash
git clone https://github.com/seu-usuario/webpty.git
cd webpty
pip install flask
python app.py
```

Android (Termux)

```bash
pkg install python git
pip install flask
git clone https://github.com/seu-usuario/webpty.git
cd webpty
python app.py
```

Acesse:

```
http://127.0.0.1:5000
```

---

🖥️ Interface

Terminal

· Prompt real do sistema
· Suporte a comandos nativos
· Interpretação correta de quebras de linha
· Comandos locais como ls, pwd, whoami, etc.
· clear / cls funcionam no frontend

System Status

Atualizado automaticamente:

· OS / Kernel / Arquitetura
· Uptime e Load Average
· CPU (modelo real, ARM ou x86)
· Núcleos
· Memória (Total / Free / Available)
· Disco
· IP e rota de rede
· Informações Android (se aplicável)

---

🔍 Detecção de Ambiente

O sistema detecta automaticamente se está rodando em:

· Linux tradicional
· Android
· Android + Termux

Sem quebrar funcionalidades por ausência de comandos (ip, ifconfig, etc.).

---

🔐 Segurança (Importante)

⚠️ Este projeto executa comandos locais.

· Não exponha em rede pública
· Uso recomendado apenas em:
  · Ambiente local
  · Laboratório
  · VM
  · Estudo educacional

Nenhuma camada de autenticação é aplicada por padrão.

---

🧪 Uso Educacional

Ideal para:

· Estudo de sistemas operacionais
· Engenharia de software
· Low-level / Linux internals
· Interfaces de terminal
· Automação local
· Ambientes Android / ARM

---

📌 Roadmap (Ideias Futuras)

· Temperatura da CPU
· Frequência por core
· Detecção big.LITTLE
· Histórico de comandos
· Autocomplete
· WebSocket (tempo real)
· Modo somente leitura
· Export de logs

---

📄 Licença

MIT License

Uso livre para fins educacionais e pessoais.
Responsabilidade total do usuário sobre execução de comandos.

---

👨‍💻 Autor

Desenvolvido para estudo profundo de sistemas e interfaces de baixo nível.

---

🧠 Nota Final

Este projeto não simula um terminal.
Ele expõe o sistema real por uma interface web controlada.



