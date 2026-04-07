from langchain_core.tools import tool

# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 4, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.3},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 1", "rating": 4.6},
    ]
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    """
    # TODO: Sinh viên tự triển khai logic tra cứu FLIGHTS_DB
    origin_n = (origin or "").strip().lower()
    destination_n = (destination or "").strip().lower()
    flights = []
    for (o, d), fs in FLIGHTS_DB.items():
        if o.strip().lower() == origin_n and d.strip().lower() == destination_n:
            flights = fs
            break
    if not flights:
        return "Không tìm thấy chuyến bay giữa hai thành phố này."
    flights.sort(key=lambda x: x["price"])
    return "\n".join([f"🛫 {flight['airline']} | {flight['departure']} → {flight['arrival']} | {flight['price']}đ | 🪑 {flight['class']}" for flight in flights[:6]])

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp.
    """
    # TODO: Sinh viên tự triển khai logic lọc và sắp xếp theo rating
    city_n = (city or "").strip().lower()
    hotels = []
    for k, hs in HOTELS_DB.items():
        if k.strip().lower() == city_n:
            hotels = hs
            break
    if not hotels:
        return "Không tìm thấy khách sạn tại thành phố này."
    hotels = [h for h in hotels if h.get("price_per_night", 0) <= max_price_per_night]
    hotels.sort(key=lambda x: x["rating"], reverse=True)
    return "\n".join([f"🏨 {hotel['name']} | {hotel['price_per_night']}đ | {hotel['stars']} sao | {hotel['area']}" for hotel in hotels[:6]])

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    total_budget: tổng ngân sách ban đầu (VNĐ)
    expenses: chuỗi mô tả các khoản chi (VD: 'vé máy bay: 890000, khách sạn: 650000')
    """
    # TODO: Sinh viên tự triển khai logic parse chuỗi và tính toán
    expenses = expenses.split(",")
    expenses = {expense.split(":")[0].strip(): int(expense.split(":")[1]) for expense in expenses}
    total_expenses = sum(expenses.values())
    remaining_budget = total_budget - total_expenses
    if remaining_budget < 0:
        return "Ngân sách của bạn không đủ để chi trả các khoản chi phí."
    return f"Ngân sách của bạn còn lại: {remaining_budget}đ"