from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db_connection

app = FastAPI(title="Game Server API", version="1.0")

# Model for updating data
class PlayerStats(BaseModel):
    player_id: int
    score: int
    money: int

@app.get("/")
def root():
    return {"status": "Server Backend is Running 🟢"}

@app.get("/players/{player_id}")
def get_player_info(player_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database Offline")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, level, is_banned FROM users WHERE id = %s", (player_id,))
    player = cursor.fetchone()
    conn.close()
    
    if not player:
        raise HTTPException(status_code=404, detail="Player not found in database")
    return player

@app.post("/update_stats/")
def update_player_stats(stats: PlayerStats):
    # Dummy response logic for updating MySQL
    return {
        "message": "Stats updated successfully",
        "player": stats.player_id,
        "new_balance": stats.money
    }
  
