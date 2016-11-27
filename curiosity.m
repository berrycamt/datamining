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
% the bounds matrix has x1,x2,y1,y2,center_x,center_y
bounds = zeros(size(PortPoD,1),6);
for i = 1:size(PortPoD,1)
    plot(PortPoD(i).X, PortPoD(i).Y,'k')
    xbounds = PortPoD(i).BoundingBox(:,1);
    ybounds = PortPoD(i).BoundingBox(:,2);
    xavg = mean(xbounds);
    yavg = mean(ybounds);
    bounds(i,:) = [xbounds(1),xbounds(2),ybounds(1),ybounds(2),xavg,yavg];
    % we will use the bounding box to obtain the center and print #
    text(xavg, yavg, PortPoD(i).DISTRICT)
    hold on
end
hold off
set(gca,'xticklabel',[])
set(gca,'yticklabel',[])
% print -djpeg 'figure1.jpg'
% The precint codes: NO: North Precint, CE: Central Precint, EA: East

% save bounds as a csv file that will be used to cluster and impute
% csvwrite('bounds.csv',bounds);

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

%% tracts
vec = zeros(120466,1);
for i = 1:size(vec,1)
    vec(i) = ShapeFile(i).census_tra;
end

% looks like these tracts are actually 100 times what I have in he txt file
% from the census bureau.

% find indices where the tract number is missing
indices = vec > 0; % so ~indices is where census tract is empty: 4894 empty census tract
% plot these points to see where they are

%% scatter plot of the locations with missing tract number
X = zeros(sum(~indices),1);
Y = zeros(sum(~indices),1);
k = 1;
for i = 1:size(indices,1)
    if ~indices(i)
        X(k) = ShapeFile(i).X;
        Y(k) = ShapeFile(i).Y;
        k = k+1;
    end
end
scatter(X,Y)

%%
for i = 1:60
    bounds = PortPoD(i).BoundingBox;
    x1 = bounds(1,1);
    x2 = bounds(2,1);
    y1 = bounds(1,2);
    y2 = bounds(2,2);
     plot([x1 x1],[y1,y2],'r',[x2,x2],[y1,y2],'r',[x1,x2],[y1,y1],'r',[x1,x2],[y2,y2],'r')
     hold on
end
hold off
% after visual inspection of the tract number imputed in for the first
% missing observation, we are correct.
