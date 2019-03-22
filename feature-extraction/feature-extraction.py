import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import pandas as pd
from collections import OrderedDict
import dateutil.parser
import glob
import csv
import os



def extract_scan_features(filename):

    feature_data = OrderedDict()

    f = netCDF4.Dataset(filename, 'r')
    f.set_auto_maskandscale(True)
    # print(f.data_model)

    # for name in f.ncattrs():
    #     print("Global attr", name, "=", getattr(f, name))

    # print(f.dimensions['scanV'])
    # print(f.dimensions['gateV'])
    # print(f.dimensions['radialV'])

    # print(f.variables['azimuthV'])
    # print(f.variables['distanceV'])
    # print(f.variables['elevationV'])
    # print(f.variables['numGatesV'])
    # print(f.variables['numRadialsV'])
    # print(f.variables['timeV'])
    # print(f.variables['Reflectivity'])
    # print(f.variables['RadialVelocity'])
    # print(f.variables['SpectrumWidth'])

    #######################################
    # Radar station data
    #######################################
    try:
        station_id = getattr(f, 'Station')
    except:
        station_id = 'null'

    try:
        station_name = getattr(f, 'StationName')
    except:
        station_name = 'null'

    try:
        station_lat = getattr(f, 'StationLatitude')
        station_lon = getattr(f, 'StationLongitude')
        station_elevation = getattr(f, 'StationElevationInMeters')
    except:
        station_lat = 'null'
        station_lon = 'null'
        station_elevation = 'null'

    time_start = getattr(f, 'time_coverage_start')

    

    timestamp = dateutil.parser.parse(time_start)
    month = timestamp.month
    day = timestamp.month
    hour = timestamp.hour
    minute = timestamp.minute



    lowest_elevation_angle_reflectivity = f.variables['elevationR'][0]
    lowest_elevation_angle_reflectivity = np.mean(lowest_elevation_angle_reflectivity)

    lowest_elevation_angle_velocity = f.variables['elevationV'][0]
    lowest_elevation_angle_velocity = np.mean(lowest_elevation_angle_velocity)

    lowest_elevation_angle_spectrum_width = f.variables['elevationV'][0]
    lowest_elevation_angle_spectrum_width = np.mean(lowest_elevation_angle_spectrum_width)

    lowest_elevation_gate_count_reflectivity = f.dimensions['gateR'].size
    lowest_elevation_gate_count_velocity = f.dimensions['gateV'].size
    lowest_elevation_gate_count_spectrum_width = f.dimensions['gateV'].size

    lowest_elevation_angle_count_reflectivity = f.dimensions['radialR'].size
    lowest_elevation_angle_count_velocity = f.dimensions['radialV'].size
    lowest_elevation_angle_count_spectrum_width = f.dimensions['radialV'].size


    feature_data['station_id'] = station_id
    feature_data['station_name'] = station_name
    feature_data['time_start'] = time_start
    feature_data['month'] = month
    feature_data['day'] = day
    feature_data['hour'] = hour
    feature_data['minute'] = minute
    feature_data['station_lat'] = station_lat
    feature_data['station_lon'] = station_lon
    feature_data['station_elevation'] = station_elevation

    feature_data['lowest_elevation_angle_reflectivity'] = lowest_elevation_angle_reflectivity
    feature_data['lowest_elevation_angle_velocity'] = lowest_elevation_angle_velocity
    feature_data['lowest_elevation_angle_spectrum_width'] = lowest_elevation_angle_spectrum_width

    feature_data['lowest_elevation_gate_count_reflectivity'] = lowest_elevation_gate_count_reflectivity
    feature_data['lowest_elevation_gate_count_velocity'] = lowest_elevation_gate_count_velocity
    feature_data['lowest_elevation_gate_count_spectrum_width'] = lowest_elevation_gate_count_spectrum_width

    feature_data['lowest_elevation_angle_count_reflectivity'] = lowest_elevation_angle_count_reflectivity
    feature_data['lowest_elevation_angle_count_velocity'] = lowest_elevation_angle_count_velocity
    feature_data['lowest_elevation_angle_count_spectrum_width'] = lowest_elevation_angle_count_spectrum_width

    #######################################
    # Lowest elevation data extaction funtions
    #######################################



    def get_reflectivity_from_lowest_elevation():
        elevation_angle = f.variables['elevationR'][0]
        elevation_angle = np.mean(elevation_angle)
        rounded_elevation_angle = round(elevation_angle, 2)

        reflectivity_at_elevation = f.variables['Reflectivity'][0]
        reflectivity_at_elevation = np.array(reflectivity_at_elevation)
        reflectivity_at_elevation[reflectivity_at_elevation == 0] = np.nan
        reflectivity_at_elevation[reflectivity_at_elevation == 1] = np.nan
        reflectivity_at_elevation = reflectivity_at_elevation / f.variables['Reflectivity'].scale_factor
        reflectivity_at_elevation = reflectivity_at_elevation.transpose()

        gates = np.array(f.variables['distanceR'])
        angles = np.array(f.variables['azimuthR'][0])
        min_index = np.argmin(angles)
        angles = np.roll(angles, min_index * -1)
        reflectivity_at_elevation = np.roll(reflectivity_at_elevation, min_index * -1, axis=1)

        # fig, ax = plt.subplots()
        # im = ax.pcolormesh(angles, gates, reflectivity_at_elevation)  # if you want contour plot
        # ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.4f}".format(
        #     rounded_elevation_angle) + " degrees")
        # ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
        # ax.set_ylabel('Distance from radar in m')
        # bar = fig.colorbar(im, ticks=range(0, 100, 20), orientation='horizontal')
        # bar.set_label('Reflectivity in dBz')

        # fig.show()
        # input("Press Enter to continue...")

        return reflectivity_at_elevation

    def get_velocity_from_lowest_elevation():
        elevation_angle = f.variables['elevationV'][0]
        elevation_angle = np.mean(elevation_angle)
        rounded_elevation_angle = round(elevation_angle, 2)

        velocity_at_elevation = f.variables['RadialVelocity'][0]
        velocity_at_elevation = np.array(velocity_at_elevation)
        velocity_at_elevation[velocity_at_elevation == 0] = np.nan
        velocity_at_elevation[velocity_at_elevation == 1] = np.nan
        velocity_at_elevation = velocity_at_elevation / f.variables['RadialVelocity'].scale_factor
        velocity_at_elevation = velocity_at_elevation.transpose()

        gates = np.array(f.variables['distanceV'])
        angles = np.array(f.variables['azimuthV'][0])
        min_index = np.argmin(angles)
        angles = np.roll(angles, min_index * -1)
        velocity_at_elevation = np.roll(velocity_at_elevation, min_index * -1, axis=1)

        # fig, ax = plt.subplots()
        # im = ax.pcolormesh(angles, gates, velocity_at_elevation)  # if you want contour plot
        # ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.4f}".format(
        #     rounded_elevation_angle) + " degrees")
        # ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
        # ax.set_ylabel('Distance from radar in m')
        # bar = fig.colorbar(im, ticks=range(-100, 100, 10), orientation='horizontal')
        # bar.set_label('Radial Velocity in m/s')

        # fig.show()
        # input("Press Enter to continue...")

        return velocity_at_elevation

    def get_spectrum_width_from_lowest_elevation():
        elevation_angle = f.variables['elevationV'][0]
        elevation_angle = np.mean(elevation_angle)
        rounded_elevation_angle = round(elevation_angle, 2)

        spectrum_width_at_elevation = f.variables['SpectrumWidth'][0]
        spectrum_width_at_elevation = np.array(spectrum_width_at_elevation)
        spectrum_width_at_elevation[spectrum_width_at_elevation == 0] = np.nan
        spectrum_width_at_elevation[spectrum_width_at_elevation == 1] = np.nan
        spectrum_width_at_elevation = spectrum_width_at_elevation / f.variables['SpectrumWidth'].scale_factor
        spectrum_width_at_elevation = spectrum_width_at_elevation.transpose()

        gates = np.array(f.variables['distanceV'])
        angles = np.array(f.variables['azimuthV'][0])
        min_index = np.argmin(angles)
        angles = np.roll(angles, min_index * -1)
        spectrum_width_at_elevation = np.roll(spectrum_width_at_elevation, min_index * -1, axis=1)

        # fig, ax = plt.subplots()
        # im = ax.pcolormesh(angles, gates, spectrum_width_at_elevation)  # if you want contour plot
        # ax.set_title(station_id + " / " + station_name + " / " + time_start + " / " + "{:.4f}".format(
        #     rounded_elevation_angle) + " degrees")
        # ax.set_xlabel('Azimuth angle in degrees: 0 = true north, 90 = east')
        # ax.set_ylabel('Distance from radar in m')
        # bar = fig.colorbar(im, ticks=range(-100, 100, 10), orientation='horizontal')
        # bar.set_label('Spectrum Width in m/s')

        # fig.show()
        # input("Press Enter to continue...")

        return spectrum_width_at_elevation




    #######################################
    # Refelctivity bined data
    #######################################

    r = get_reflectivity_from_lowest_elevation()
    r_diff_gate = np.absolute(np.diff(r, axis=0))
    r_diff_azimuth = np.absolute(np.diff(r, axis=1))

    r_hist, r_bin_edges = np.histogram(r, bins=40, range=(0,200))
    # print(r_hist)
    # print(r_bin_edges)
    for i in range(len(r_bin_edges)-1):
        key = 'r_hist_' + str(int(r_bin_edges[i])) + '_' + str(int(r_bin_edges[i + 1]))
        feature_data[key] = r_hist[i]

    r_diff_gate_hist, r_diff_gate_bin_edges = np.histogram(r_diff_gate, bins=40, range=(0,200))
    # print(r_diff_gate_hist)
    # print(r_diff_gate_bin_edges)
    for i in range(len(r_diff_gate_bin_edges)-1):
        key = 'r_diff_gate_hist_' + str(int(r_diff_gate_bin_edges[i])) + '_' + str(int(r_diff_gate_bin_edges[i + 1]))
        feature_data[key] = r_diff_gate_hist[i]

    r_diff_azimuth_hist, r_diff_gate_azimuth_edges = np.histogram(r_diff_gate, bins=40, range=(0,200))
    # print(r_diff_azimuth_hist)
    # print(r_diff_gate_azimuth_edges)
    for i in range(len(r_diff_gate_azimuth_edges)-1):
        key = 'r_diff_azimuth_hist_' + str(int(r_diff_gate_azimuth_edges[i])) + '_' + str(int(r_diff_gate_azimuth_edges[i + 1]))
        feature_data[key] = r_diff_azimuth_hist[i]


    # print(r.shape)
    # print(r_diff_gate.shape)
    # print(r_diff_azimuth.shape)
    # print()

    #######################################
    # Velocity bined data
    #######################################

    v = get_velocity_from_lowest_elevation()
    v_diff_gate = np.absolute(np.diff(v, axis=0))
    v_diff_azimuth =np.absolute(np.diff(v, axis=1))

    v_hist, v_bin_edges = np.histogram(v, bins=40, range=(0,200))
    # print(v_hist)
    # print(v_bin_edges)
    for i in range(len(v_bin_edges)-1):
        key = 'v_hist_' + str(int(v_bin_edges[i])) + '_' + str(int(v_bin_edges[i + 1]))
        feature_data[key] = v_hist[i]

    v_diff_gate_hist, v_diff_gate_bin_edges = np.histogram(v_diff_gate, bins=40, range=(0,200))
    # print(v_diff_gate_hist)
    # print(v_diff_gate_bin_edges)
    for i in range(len(v_diff_gate_bin_edges)-1):
        key = 'v_diff_gate_hist_' + str(int(v_diff_gate_bin_edges[i])) + '_' + str(int(v_diff_gate_bin_edges[i + 1]))
        feature_data[key] = v_diff_gate_hist[i]

    v_diff_azimuth_hist, v_diff_gate_azimuth_edges = np.histogram(v_diff_gate, bins=40, range=(0,200))
    # print(v_diff_azimuth_hist)
    # print(v_diff_gate_azimuth_edges)
    for i in range(len(v_diff_gate_azimuth_edges)-1):
        key = 'v_diff_azimuth_hist_' + str(int(v_diff_gate_azimuth_edges[i])) + '_' + str(int(v_diff_gate_azimuth_edges[i + 1]))
        feature_data[key] = v_diff_azimuth_hist[i]


    # print(v.shape)
    # print(v_diff_gate.shape)
    # print(v_diff_azimuth.shape)
    # print()

    #######################################
    # Spectrum Width bined data
    #######################################

    sw = get_spectrum_width_from_lowest_elevation()
    sw_diff_gate = np.absolute(np.diff(sw, axis=0))
    sw_diff_azimuth = np.absolute(np.diff(sw, axis=1))

    sw_hist, sw_bin_edges = np.histogram(sw, bins=40, range=(0,200))
    # print(sw_hist)
    # print(sw_bin_edges)
    for i in range(len(sw_bin_edges)-1):
        key = 'sw_hist_' + str(int(sw_bin_edges[i])) + '_' + str(int(sw_bin_edges[i + 1]))
        feature_data[key] = sw_hist[i]
    # print(sum(sw_hist))

    sw_diff_gate_hist, sw_diff_gate_bin_edges = np.histogram(sw_diff_gate, bins=40, range=(0,200))
    # print(sw_diff_gate_hist)
    # print(sw_diff_gate_bin_edges)
    for i in range(len(sw_diff_gate_bin_edges)-1):
        key = 'sw_diff_gate_hist_' + str(int(sw_diff_gate_bin_edges[i])) + '_' + str(int(sw_diff_gate_bin_edges[i + 1]))
        feature_data[key] = sw_diff_gate_hist[i]

    sw_diff_azimuth_hist, sw_diff_gate_azimuth_edges = np.histogram(sw_diff_gate, bins=40, range=(0,200))
    # print(sw_diff_azimuth_hist)
    # print(sw_diff_gate_azimuth_edges)
    for i in range(len(sw_diff_gate_azimuth_edges)-1):
        key = 'sw_diff_azimuth_hist_' + str(int(sw_diff_gate_azimuth_edges[i])) + '_' + str(int(sw_diff_gate_azimuth_edges[i + 1]))
        feature_data[key] = sw_diff_azimuth_hist[i]


    # print(sw.shape)
    # print(sw_diff_gate.shape)
    # print(sw_diff_azimuth.shape)
    # print()




    # print(feature_data)
    return feature_data





if __name__ == "__main__":
    t_dataset = []
    s_dataset = []


    # tornado_files_path = r'C:/Users/stefan/Desktop/Datasets/radar_data/data/EF3/'
    # tornado_files = glob.glob(tornado_files_path + '**/*.nc')
    # num_t = len(tornado_files)

    # for i, t in enumerate(tornado_files):
    #     data = extract_scan_features(t)
    #     data['is_tornado_present'] = 1
    #     data['filename'] = os.path.basename(t)
    #     t_dataset.append(data)
    #     print(t)
    #     print((i/num_t)*100)

    # with open('dataset.csv', 'w') as outfile:
    #     fp = csv.DictWriter(outfile, t_dataset[0].keys())
    #     fp.writeheader()
    #     fp.writerows(t_dataset)


    storm_files_path = r'C:/Users/stefan/Desktop/Datasets/radar_data/storm_unfiltered/out/'
    storm_files = glob.glob(storm_files_path + '*.nc')
    num_s = len(storm_files)

    for i, s in enumerate(storm_files):
        try:
            data = extract_scan_features(s)
        except:
            continue
        data['is_tornado_present'] = 0
        data['filename'] = os.path.basename(s)
        s_dataset.append(data)
        print(s)
        print((i/num_s)*100)

    with open('dataset2.csv', 'w') as outfile:
        fp = csv.DictWriter(outfile, s_dataset[0].keys())
        fp.writeheader()
        fp.writerows(s_dataset)