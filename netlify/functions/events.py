import json
from datetime import datetime

# ==========================================
# LOGIKA PBO (OOP) - DATA KONSER
# ==========================================
class Event:
    def __init__(self, nama, artis, tanggal, harga):
        self.nama = nama
        self.artis = artis
        self.tanggal = tanggal
        self.__harga = harga  # Enkapsulasi

    @property
    def harga(self):
        return self.__harga

    def detail(self):
        return f"{self.nama} oleh {self.artis} pada {self.tanggal}"

class Tiket:
    def __init__(self, pembeli, event):
        self.pembeli = pembeli
        self.event = event
        self.status = "LUNAS"
        self.kode = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

# Data Konser
daftar_event = [
    Event("World Tour", "BLACKPINK", "13 Desember 2026", 1500000),
    Event("Pesta Pora", "Hindia", "28 September 2026", 450000),
    Event("Semerindu", "Afgan", "15 Oktober 2026", 750000)
]

# ==========================================
# NETLIFY FUNCTION HANDLER
# ==========================================
def handler(event, context):
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
    }
    
    # Handle CORS preflight
    if method == 'OPTIONS':
        return {"statusCode": 200, "headers": headers, "body": ""}
    
    # GET /api/events
    if method == 'GET' and path.endswith('/api/events'):
        data = [
            {
                "id": i,
                "nama": e.nama,
                "artis": e.artis,
                "tanggal": e.tanggal,
                "harga": e.harga
            } 
            for i, e in enumerate(daftar_event)
        ]
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(data)
        }

    # POST /api/pesan
    if method == 'POST' and path.endswith('/api/pesan'):
        try:
            body = json.loads(event.get('body', '{}'))
            nama_pembeli = body.get('nama', 'Tamu')
            event_id = int(body.get('event_id', 0))
            
            if 0 <= event_id < len(daftar_event):
                event_dipilih = daftar_event[event_id]
                tiket_baru = Tiket(nama_pembeli, event_dipilih)
                
                return {
                    "statusCode": 200,
                    "headers": headers,
                    "body": json.dumps({
                        "success": True,
                        "tiket": {
                            "kode": tiket_baru.kode,
                            "event": tiket_baru.event.detail(),
                            "pembeli": tiket_baru.pembeli,
                            "status": tiket_baru.status,
                            "harga": tiket_baru.event.harga
                        }
                    })
                }
            else:
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"success": False, "message": "Event tidak valid"})
                }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps({"success": False, "message": str(e)})
            }

    # Default 404
    return {
        "statusCode": 404,
        "headers": headers,
        "body": json.dumps({"message": "Endpoint tidak ditemukan"})
    }