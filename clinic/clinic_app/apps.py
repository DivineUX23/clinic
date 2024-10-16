from django.apps import AppConfig


class ClinicAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic_app'


"""
{"status":"success","message":"Retrieved successfully","data":{"request_token":"8c656ce8757eeddb34aced59f1518161e7c3a7158a5941c8f83c74f5b67bf727","couriers":
                                                               
            [{"courier_id":"test_2_courier",
              "courier_name":"Richard Express",     
              "courier_image":"",
              "service_code":"test_2_courier",
              "insurance":{"code":"not available",
                           "fee":0},
              "discount":{"percentage":5,
                          "symbol":"%",
                          "discounted":50},
              "service_type":"pickup",
              "waybill":true,
              "on_demand":true,7
              "is_cod_available":true,
              "tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":1450.25,
              "rate_card_currency":"NGN",
              "pickup_eta":"Within 24 Hours",
              "pickup_eta_time":"2024-10-09 14:57:48",
              "dropoff_station":null,
              "pickup_station":null,
              "delivery_eta":"Between 1 - 4 business working days","delivery_eta_time":"2024-10-11 14:57:48",
              "info":null,"currency":"NGN","vat":75,
              "total":1450.25,"tracking":{"bars":4,
                                          "label":"Good"}
                                          },

             
             {"courier_id":"test_3_courier","courier_name":"Millie Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_3_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":12,"symbol":"%","discounted":101},"service_type":"dropoff","waybill":true,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":1266.21,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":{"name":"Astroworld park","address":"No 15 Walker NBA YoungBoy Street","country":"Nigeria","phone":null},"pickup_station":{"name":"Astroworld park","address":"No 15 Walker NBA YoungBoy Street","phone":null},"delivery_eta":"Between 12 - 48 Hours","delivery_eta_time":"2024-10-11 14:57:48","info":null,"currency":"NGN","vat":63,"total":1266.21,"tracking":{"bars":4,"label":"Good"}},
             
             {"courier_id":"test_1_courier","courier_name":"Bubble Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_1_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":10,"symbol":"%","discounted":60},"service_type":"pickup","waybill":false,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":990.15,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":null,"pickup_station":null,"delivery_eta":"Same day delivery","delivery_eta_time":"2024-10-09 02:57:48","info":null,"currency":"NGN","vat":45,"total":990.15,"tracking":{"bars":4,"label":"Good"}}],
            

            "fastest_courier":{"courier_id":"test_1_courier","courier_name":"Bubble Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_1_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":10,"symbol":"%","discounted":60},"service_type":"pickup","waybill":false,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":990.15,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":null,"pickup_station":null,"delivery_eta":"Same day delivery","delivery_eta_time":"2024-10-09 02:57:48","info":null,"currency":"NGN","vat":45,"total":990.15,"tracking":{"bars":4,"label":"Good"}},
            
            "cheapest_courier":{"courier_id":"test_1_courier","courier_name":"Bubble Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_1_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":10,"symbol":"%","discounted":60},"service_type":"pickup","waybill":false,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":990.15,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":null,"pickup_station":null,"delivery_eta":"Same day delivery","delivery_eta_time":"2024-10-09 02:57:48","info":null,"currency":"NGN","vat":45,"total":990.15,"tracking":{"bars":4,"label":"Good"}},
            
            "checkout_data":{"ship_from":{"name":"Mather Osas","phone":"+2347067239473","email":"Sam@gmail.com","address":"1, Ugbowo, Benin City, Edo State, 4444, Nigeria"},"ship_to":{"name":"Mather Osas","phone":"+2347067239473","email":"Sam@gmail.com","address":"1, Ugbowo, Benin City, Edo State, 4444, Nigeria"},"currency":"NGN","package_amount":4000,"package_weight":2,"pickup_date":"October 8th 2024","is_invoice_required":false}}}

"""

