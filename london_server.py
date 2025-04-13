from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PeerConfig(BaseModel):
    public_key: str
    allowed_ip: str

@app.post("/api/add-peer")
async def add_peer(peer: PeerConfig):
    try:
        # Проверяем существование интерфейса wg0
        result = subprocess.run(
            ["/sbin/ip", "link", "show", "wg0"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail="WireGuard interface not found")

        # Добавляем пир
        cmd = [
            "/usr/bin/sudo", "/usr/bin/wg",
            "set", "wg0",
            "peer", peer.public_key,
            "allowed-ips", peer.allowed_ip
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error adding peer: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"Failed to add peer: {result.stderr}")

        return {"status": "success", "message": "Peer added successfully"}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 