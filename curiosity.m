%%
try
    load('shpfiles.mat')
catch
    warning('.mat file inexistent')
    ShapeFile = shaperead('NIJ2016_JAN01_JUL31.shp');
    % occ_date: 'YEARMODA' i.e. '20160101' is 2016-Jan-01
    cd('PortlandpoliceDistrict')
    PortPoD = shaperead('Portland_Police_Districts.shp'); % This is Portland OR
    cd('..')
end

%% Portland Oregon
% after looking at the XML file in Google Chrome, I noticed that the
% parameters refer to Oregon. I looked at the map of Oregon and it is a
% match for the plot below. XML contains info on units and such
for i = 1:size(PortPoD,1)
    plot(PortPoD(i).X, PortPoD(i).Y)
    xbounds = PortPoD(i).BoundingBox(:,1);
    ybounds = PortPoD(i).BoundingBox(:,2);
    xavg = mean(xbounds);
    yavg = mean(ybounds);
    % we will use the bounding box to obtain the center and print #
    text(xavg, yavg, PortPoD(i).DISTRICT)
    hold on
end
hold off
% The precint codes: NO: North Precint, CE: Central Precint, EA: East

%% quick check
Area = 0;
for i = 41:60
    Area = Area + PortPoD(i).Shape_Area;
end
% I am investigating the sum of the areas of each of the districts in the
% East precint. By looking at the map, the area of the east precint is
% estmated at 36.0 square miles. The Area above is 36.27 and so we can
% safely assume that the units is square miles.
% What exactly is the shape_length? I doubt we need it anyways

% proportion of area over total area
% population density is ideal

% employment levels, education levels
% http://www.bls.gov/regions/west/or_portland_msa.htm
% https://geomap.ffiec.gov/FFIECGeocMap/GeocodeMap1.aspx