import  math

__author__ = 'watchara.p'

def MaxLatLongOnBearing(centerLat, centerLon, bearing, distance):
   lonRads = math.radians(centerLon)
   latRads = math.radians(centerLat)
   bearingRads = math.radians(bearing)
   maxLatRads = math.asin(math.sin(latRads) * math.cos(distance / 6371) + math.cos(latRads) * math.sin(distance / 6371) * math.cos(bearingRads))
   maxLonRads = lonRads + math.atan2((math.sin(bearingRads) * math.sin(distance / 6371) * math.cos(latRads)), (math.cos(distance / 6371) - math.sin(latRads) * math.sin(maxLatRads)))
   maxLat = math.degrees(maxLatRads)
   maxLon = math.degrees(maxLonRads)
   return maxLat, maxLon

km = 5
scale_m=100
interval = int((km*1000/scale_m) + 1) #count zero
miles_conv_fac = 0.621371192
miles = km*miles_conv_fac

q = int(5000/2/100)

lon0 = 101.1310336
lat0 = 12.6953578
# top left x,y(-2500,2500)
# xy0_lat,xy0_lon = MaxLatLongOnBearing(lat0,lon0,225,miles)
# x50y0_lat,x50y0_lon =MaxLatLongOnBearing(lat0,lon0,135,miles)
# x0y50_lat,x0y50_lon = MaxLatLongOnBearing(lat0,lon0,315,miles)
xy0_lat,xy0_lon = MaxLatLongOnBearing(lat0,lon0,45,miles)
x50y0_lat,x50y0_lon =MaxLatLongOnBearing(lat0,lon0,315,miles)
x0y50_lat,x0y50_lon = MaxLatLongOnBearing(lat0,lon0,135,miles)
# print("{"+"position: new google.maps.LatLng({} , {}), type:'info'".format(xy0_lat,xy0_lon)+"},")
# print("{"+"position: new google.maps.LatLng({} , {}), type:'info'".format(xy0_lat,xy0_lon)+"},")
step_x = (x50y0_lon-xy0_lon)/interval
step_y = (x0y50_lat-xy0_lat)/interval
for xxx in range(0,50):
    for yyy in range(0,50):
        print("{" + "position: new google.maps.LatLng({} , {}), type:'info'".format(xy0_lat+(yyy*step_y), xy0_lon+(xxx*step_x)) + "},")
# for x_n in range(0,interval,1):
#     for y_n in range(0,interval,1):
#         print("x:{}, y:{}".format(x_n,y_n))
#         x_x = x_n-q
#         y_y = y_n-q
#         print(x_x,y_y)
        # print("{"+"position: new google.maps.LatLng({} , {}), type:'info'".format(xy0_lat+(y_y*step_y), xy0_lon+(x_x*step_x))+"},")

# print("position: new google.maps.LatLng({} , {}), type:'info'".format(x50y0_lat,x50y0_lon))
# print("position: new google.maps.LatLng({} , {}), type:'info'".format(xy0_lat,xy0_lon))


# x_lf_lat,x_lf_lon = MaxLatLongOnBearing(lat0,lon0,90,2.5*miles_conv_fac)
#
# for x in range(0,5100,100):
#     x_n_lat,x_n_lon = MaxLatLongOnBearing(xy0_lat,xy0_lon,90,x/1000*miles_conv_fac)
#     print("position: new google.maps.LatLng({} , {}), type:'info'".format(x_n_lat,x_n_lon))

# ulcrnLat, ulcrnLon = MaxLatLongOnBearing(lat0,lon0,45,miles)
# urcrnLat, urcrnLon = MaxLatLongOnBearing(lat0, lon0,135,miles)
# llrcrnLat,llrcrnLon = MaxLatLongOnBearing(lat0,lon0,225, miles)
# llcrnLat, llcrnLon = MaxLatLongOnBearing(lat0, lon0,315, miles)
#
# i90Lat,i90Lon = MaxLatLongOnBearing(lat0,lon0,90,miles)
#
# print("position: new google.maps.LatLng({} , {}), type:'info'".format(urcrnLat,urcrnLon))
# print("position: new google.maps.LatLng({} , {}), type:'info'".format(llrcrnLat,llrcrnLon))
# print("position: new google.maps.LatLng({} , {}), type:'info'".format(ulcrnLat,ulcrnLon))
# print("position: new google.maps.LatLng({} , {}), type:'info'".format(llcrnLat,llcrnLon))
# #
# print(i90Lat,i90Lon)