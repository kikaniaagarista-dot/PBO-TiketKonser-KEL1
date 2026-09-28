import json
from datetime import datetime

class Event:
    def __init__(self, nama, artis, tanggal, harga):
        self.nama = nama
        self.artis = artis
        self.tanggal = tanggal
        self.__harga = harga

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

daftar_event = [
    Event("World Tour", "BLACKPINK", "13 Desember 2026", 1500000),
    Event("Pesta Pora", "Hindia", "28 September 2026", 450000),
    Event("Semerindu", "Afgan", "15 Oktober 2026", 750000)
]

def handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }
    
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