from tabulate import tabulate

class Booking:
    def __init__(self, id, customer_name, room_number, room_price, nights, service_fee, discount):
        self.id = id
        self.customer_name = customer_name
        self.room_number = room_number
        self.room_price = room_price
        self.nights = nights
        self.service_fee = service_fee
        self.discount = discount
        self.total_rent = 0
        self.rent_type = ""

        self.update_info()
    def calculate_total_rent(self):
        self.total_rent = self.room_price * self.nights + self.service_fee + self.discount
        if self.total_rent < 0:
            self.total_rent = 0

    def classify_rent(self):
        if self.total_rent < 1000000:
            self.rent_type = 'Tiết kiệm'
        elif self.total_rent < 3000000:
            self.rent_type = 'Tiêu chuẩn'
        elif self.total_rent < 7000000:
            self.rent_type = 'Cao cấp'
        else:
            self.rent_type = 'VIP'
    
    def update_info(self):
        self.calculate_total_rent()
        self.classify_rent()

def input_not_empty(field_name):
    while True:
        value = input(f'Nhập {field_name}: ')
        if not value:
            print(f'{field_name} không được để trống!')
            continue
        return value
    
def validate_price(field_name):
    while True:
        try:
            number = float(input(f'Nhập {field_name}: '))
            if number <= 0 :
                print(f'{field_name} phải lớn hơn hoặc bằng 0')
                continue

            return number
        
        except ValueError:
            print(f'{field_name} phải là số!')


def validate_nights():
    while True:
        try:
            quantity = float(input(f'Nhập số đêm thuê: '))
            if quantity < 1 or quantity > 365 :
                print(f'Số đêm thuê phải là số nguyên từ 1 đến 365')
                continue

            return quantity
        
        except ValueError:
            print(f'Số đêm thuê phải là số!')

class BookingManager:
    def __init__(self):
        self.bookings = []

    def find_id(self, id):
        for booking in self.bookings:
            if id.lower() == booking.id.lower():
                return booking
        return None
    
    def add_booking(self):
        while True:
            id = input_not_empty('mã đặt phòng').upper()
            booking = self.find_id(id)
            if booking:
                print('Mã đặt phòng không được trùng')
                continue
            break
        
        customer_name = input_not_empty('họ tên khách hàng').title()
        room_number = input_not_empty('số phòng')
        room_price = validate_price('giá phòng một đêm')
        nights = validate_nights()
        service_fee = validate_price('phụ phí dịch vụ')
        discount = validate_price('giảm giá')

        new_booking = Booking(
            id,
            customer_name,
            room_number,
            room_price,
            nights,
            service_fee,
            discount
        )

        self.bookings.append(new_booking)

        print('Thêm đặt phòng thành công!')


    def show_all(self):
        if not self.bookings:
            print('Danh sách đặt phòng đang rỗng!')
        else:
            data = []
            for booking in self.bookings:
                data.append([
                    booking.id,
                    booking.customer_name,
                    booking.room_number,
                    booking.room_price,
                    booking.nights,
                    booking.service_fee,
                    booking.discount,
                    booking.total_rent,
                    booking.rent_type 
                ])
            print(tabulate(data,headers=[
                'Mã đặt phòng',
                'Họ tên khách hàng',
                'Số phòng',
                'Giá phòng một đêm',
                'Số đêm thuê',
                'Phụ phí dịch vụ',
                'Giảm giá',
                'Tổng tiền thuê',
                'Phân loại tiền thuê'
            ], tablefmt= 'grid'))

    def update_booking(self):
        while True:
            id = input_not_empty('mã đặt phòng muốn cập nhật').upper()
            booking = self.find_id(id)
            if not booking:
                print('Không tìm thấy đặt phòng cần cập nhật!')
                continue
            break

        booking.room_price = validate_price('giá phòng một đêm')
        booking.nights = validate_nights()
        booking.service_fee = validate_price('phụ phí dịch vụ')
        booking.discount = validate_price('giảm giá')
        booking.update_info()

        print('Cập nhật đặt phòng thành công!')

    def delete_booking(self):
        id = input_not_empty('mã đặt phòng muốn xóa').upper()
        booking = self.find_id(id)
        if not booking:
            print('Không tìm thấy đặt phòng cần xóa!')
        else:
            confirm = input('Bạn có chắc muốn xóa đặt phòng này không? (Y/N): ')
            if confirm.lower() == 'n':
                print('Đã hủy thao tác xóa!')
            elif confirm.lower() == 'y':
                self.bookings.remove(booking)
                print('Xóa đặt phòng thành công!')
            else:
                print('Lựa chọn không hợp lệ')

    def search_booking(self):
        find_name = input('Nhập tên khách hàng hoặc số phòng bạn muốn tìm kiếm: ')
        results = []
        for booking in self.bookings:
            if find_name.lower() in booking.customer_name.lower() or find_name.lower() in booking.room_number.lower():
                results.append(booking)

        if not results:
            print(' Không tìm thấy đặt phòng phù hợp!')
        else:
            for result in results:
                print(f'{result.customer_name} - {result.room_number}')

def show_menu():
    print("""
================ MENU ================
1. Hiển thị danh sách đặt phòng
2. Thêm đặt phòng mới
3. Cập nhật đặt phòng
4. Xóa đặt phòng
5. Tìm kiếm đặt phòng
6. Thoát
=====================================""")
    
def main():
    booking = BookingManager()

    while True:
        show_menu()
        choice = input('Nhập lựa chọn của bạn: ')
        if choice == '1':
            booking.show_all()
        elif choice == '2':
            booking.add_booking()
        elif choice == '3':
            booking.update_booking()
        elif choice == '4':
            booking.delete_booking()
        elif choice == '5':
            booking.search_booking()
        elif choice == '6':
            print('Cảm ơn bạn đã sử dụng hệ thống quản lý đặt phòng khách sạn!')
            break
        else:
            print('Lựa chọn không hợp lệ!')

main()

