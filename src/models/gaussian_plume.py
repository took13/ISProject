###########################################################################
# GAUSSIAN PLUME MODEL FOR TEACHING PURPOSES                              #
# PAUL CONNOLLY (UNIVERSITY OF MANCHESTER, 2017)                          #
# THIS CODE IS PROVIDED `AS IS' WITH NO GUARANTEE OF ACCURACY             #
# IT IS USED TO DEMONSTRATE THE EFFECTS OF ATMOSPHERIC STABILITY,         #
# WINDSPEED AND DIRECTION AND MULTIPLE STACKS ON THE DISPERSION OF        #
# POLLUTANTS FROM POINT SOURCES                                           #
###########################################################################

import numpy as np
import sys
from scipy.special import erfcinv as erfcinv
import tqdm as tqdm
import math
from src.models.gauss_func import gauss_func
import json
from src.models.weather import Weather

class Gaussian():

    def __init__(self):
        pass

    def MainCalc(self, centerLat, centerLon):
############## Get wind profile from OpenWeatherMap ###########
        wea = Weather("Rayong",centerLat,centerLon)
        self.wind_deg = wea.wind_deg
        self.wind_spd = wea.wind_speed
##############################################################
        # stability of the atmosphere
        # self.wind_deg = wind_deg
        # self.wind_spd = wind_spd
        self.centerLat = centerLat
        self.centerLon = centerLon
        CONSTANT_STABILITY = 1;
        ANNUAL_CYCLE = 2;
        stability_str = ['Very unstable', 'Moderately unstable', 'Slightly unstable', \
                         'Neutral', 'Moderately stable', 'Very stable'];
        # Aerosol properties
        HUMIDIFY = 2;
        DRY_AEROSOL = 1;

        SODIUM_CHLORIDE = 1;
        SULPHURIC_ACID = 2;
        ORGANIC_ACID = 3;
        AMMONIUM_NITRATE = 4;
        nu = [2., 2.5, 1., 2.];
        rho_s = [2160., 1840., 1500., 1725.];
        Ms = [58.44e-3, 98e-3, 200e-3, 80e-3];
        Mw = 18e-3;

        dxy = 100;  # resolution of the model in both x and y directions
        dz = 10;
        x = np.mgrid[-2500:2500 + dxy:dxy];  # solve on a 5 km domain
        y = x;  # x-grid is same as y-grid
        ###########################################################################


        # SECTION 1: Configuration
        # Variables can be changed by the user+++++++++++++++++++++++++++++++++++++
        RH = 0.90;
        aerosol_type = SODIUM_CHLORIDE;

        dry_size = 60e-9;
        humidify = DRY_AEROSOL;

        stab1 = 1;  # set from 1-6
        stability_used = CONSTANT_STABILITY;

        # output = PLAN_VIEW;
        # output=SURFACE_TIME;
        x_slice = 26;  # position (1-50) to take the slice in the x-direction
        y_slice = 1;  # position (1-50) to plot concentrations vs time

        # wind = PREVAILING_WIND;
        # wind=CONSTANT_WIND;
        stacks = 1;
        stack_x = [0., 1000., -200.];
        stack_y = [0., 250., -500.];

        Q = [40., 40., 40.];  # mass emitted per unit time
        H = [50., 50., 50.];  # stack height, m
        # days=50;          # run the model for 365 days
        days = 2;  # run the model for 365 days
        # --------------------------------------------------------------------------
        times = np.mgrid[1:(days) * 24 + 1:1] / 24.;

        Dy = 10.;
        Dz = 10.;

        # SECTION 2: Act on the configuration information

        # Decide which stability profile to use
        if stability_used == CONSTANT_STABILITY:

            stability = stab1 * np.ones((days * 24, 1));
            stability_str = stability_str[stab1 - 1];
        elif stability_used == ANNUAL_CYCLE:

            stability = np.round(2.5 * np.cos(times * 2. * np.pi / (365.)) + 3.5);
            stability_str = 'Annual cycle';
        else:
            sys.exit()

        # decide what kind of run to do, plan view or y-z slice, or time series
        # if output == PLAN_VIEW or output == SURFACE_TIME or output == NO_PLOT:

        C1 = np.zeros((len(x), len(y), days * 24));  # array to store data, initialised to be zero

        [x, y] = np.meshgrid(x, y);  # x and y defined at all positions on the grid
        z = np.zeros(np.shape(x));  # z is defined to be at ground level.
        # elif output == HEIGHT_SLICE:
        #     z = np.mgrid[0:500 + dz:dz];  # z-grid
        #
        #     C1 = np.zeros((len(y), len(z), days * 24));  # array to store data, initialised to be zero
        #
        #     [y, z] = np.meshgrid(y, z);  # y and z defined at all positions on the grid
        #     x = x[x_slice] * np.ones(np.shape(y));  # x is defined to be x at x_slice
        # else:
        #     sys.exit()

        # wind_deg = 180

        # Set the wind based on input flags++++++++++++++++++++++++++++++++++++++++
        wind_speed = self.wind_spd * np.ones((days * 24, 1));  # m/s
        # if wind == CONSTANT_WIND:
        #     wind_dir = self.wind_deg * np.ones((days * 24, 1));
        #     # wind_dir=0.*np.ones((days*24,1));
        #     wind_dir_str = 'Constant wind';
        # elif wind == FLUCTUATING_WIND:
        #     wind_dir = 360. * np.random.rand(days * 24, 1);
        #     wind_dir_str = 'Random wind';
        # elif wind == PREVAILING_WIND:
            # wind_dir=-np.sqrt(2.)*erfcinv(2.*np.random.rand(24*days,1))*40.; #norminv(rand(days.*24,1),0,40);
        wind_dir = -np.sqrt(2.) * erfcinv(2. * np.random.rand(24 * days, 1)) * 15.5;  # norminv(rand(days.*24,1),0,40);
        # note at this point you can add on the prevailing wind direction, i.e.
        wind_dir = wind_dir + self.wind_deg;
        wind_dir[np.where(wind_dir >= 360.)] = \
            np.mod(wind_dir[np.where(wind_dir >= 360)], 360);
        #     wind_dir_str = 'Prevailing wind';
        # else:
        #     sys.exit()
        # --------------------------------------------------------------------------
        # SECTION 3: Main loop
        # For all times...
        C1 = np.zeros((len(x), len(y), len(wind_dir)))
        # for i in tqdm.tqdm(range(0, len(wind_dir))):
        for i in range(0, len(wind_dir)):
            for j in range(0, stacks):
                C = np.ones((len(x), len(y)))
                C = gauss_func(Q[j], wind_speed[i], wind_dir[i], x, y, z,
                               stack_x[j], stack_y[j], H[j], Dy, Dz, stability[i]);
                C1[:, :, i] = C1[:, :, i] + C;

        ########################## Convert Cartesian to Google Latitude, Longitude ##################
        #############################################################################################
        def MaxLatLongOnBearing(centerLat, centerLon, bearing, distance):
           lonRads = math.radians(centerLon)
           latRads = math.radians(centerLat)
           bearingRads = math.radians(bearing)
           maxLatRads = math.asin(math.sin(latRads) * math.cos(distance / 6371) + math.cos(latRads) * math.sin(distance / 6371) * math.cos(bearingRads))
           maxLonRads = lonRads + math.atan2((math.sin(bearingRads) * math.sin(distance / 6371) * math.cos(latRads)), (math.cos(distance / 6371) - math.sin(latRads) * math.sin(maxLatRads)))
           maxLat = math.degrees(maxLatRads)
           maxLon = math.degrees(maxLonRads)
           return maxLat, maxLon

        # Map Center
        lat_center = self.centerLat # 12.6953578
        lon_center = self.centerLon # 101.1310336


        # Concentrate area
        km = 5
        scale_m=100
        interval = int((km*1000/scale_m) + 1) #count zero
        miles_conv_fac = 0.621371192
        miles = km*miles_conv_fac

        # xy0_lat,xy0_lon = MaxLatLongOnBearing(lat_center, lon_center, 225-wind_deg, miles)
        # x50y0_lat,x50y0_lon =MaxLatLongOnBearing(lat_center, lon_center, 135-wind_deg, miles)
        # x0y50_lat,x0y50_lon = MaxLatLongOnBearing(lat_center, lon_center, 315-wind_deg, miles)

        xy0_lat,xy0_lon = MaxLatLongOnBearing(lat_center,lon_center,225,miles)
        x50y0_lat,x50y0_lon =MaxLatLongOnBearing(lat_center,lon_center,135,miles)
        x0y50_lat,x0y50_lon = MaxLatLongOnBearing(lat_center,lon_center,315,miles)

        step_x = (x50y0_lon-xy0_lon)/interval #len(x) #interval
        step_y = (x0y50_lat-xy0_lat)/interval #len(y) #interval


        Cxy = np.mean(C1, axis=2)*1e6

        data=[]
        # item = ''
        for x_n in range(0,len(x)):
           for y_n in range(0,len(y)):
               if (Cxy[y_n,x_n] > 1):
                   lat = xy0_lat+(y_n*step_y)
                   lon = xy0_lon+(x_n*step_x)
                   weight = Cxy[y_n,x_n]*10
                   # item = "{"+"location: new google.maps.LatLng({},{}), weight:{}".format(lat,lon,weight)+"}"
                   # item = {
                   #      "location": "new google.maps.LatLng({},{})".format(lat,lon),
                   #      "weight": weight
                   #      }
                   item = {"latitude": lat,
                            "longitude": lon,
                            "weight": weight}
                   data.append(item)
        return json.dumps(data)










