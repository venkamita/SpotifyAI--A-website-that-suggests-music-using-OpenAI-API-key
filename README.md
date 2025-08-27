# 🎵 AI Spotify Playlist Generator  

Generate personalized Spotify playlists using AI prompts.  
Built with **Flask** (Python) + **HTML** during a hackathon.  

---

## 🚀 About the Project  
This was my **2nd hackathon project**.  
- Simpler functionality than the original product idea.  
- Built quickly with **prompt engineering + APIs** (learning by doing ✨).  
- Goal wasn’t to win, but to build something end-to-end and ship it.  

---

## ⚙️ Tech Stack  
- **Flask (Python)** – backend server  
- **HTML/CSS** – frontend UI  
- **Spotify Web API** – to create & manage playlists  
- **AIML API** – for generating AI-powered playlist suggestions  

---

## 🔑 Setup  

1. Clone the repo:  
   ```bash
   git clone https://github.com/your-username/ai-spotify-playlist-generator.git
   cd ai-spotify-playlist-generator
   ```

2. Create a `.env` file with your own keys:  
   ```env
   FLASK_SECRET_KEY=your-secret-key
   SPOTIFY_CLIENT_ID=your-spotify-client-id
   SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
   SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
   AI_BASE_URL=https://api.aimlapi.com
   AI_API_KEY=your-ai-api-key
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:  
   ```bash
   flask run
   ```

---

## 🧑‍💻 How It Works  
1. User enters a text prompt (e.g. *“chill study vibes with lofi”*).  
2. The AI (via AIML API) interprets the vibe and suggests matching track ideas.  
3. The app connects to the **Spotify Web API** to generate a playlist.  

---

## 📌 Notes  
- Prompt limit is **256 characters**.  
- Built under hackathon constraints (expect bugs & rough edges).  
- Meant as a learning project → contributions and improvements welcome.  

---

## 🙌 Acknowledgments  
- [Spotify for Developers](https://developer.spotify.com/dashboard) – for OAuth + playlist API  
- [AIML API](https://aimlapi.com/app/) – for free AI text API  
- Hackathon team & mentors  
