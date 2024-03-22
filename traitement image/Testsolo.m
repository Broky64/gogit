close all
clear all
nomimage='plateau_pied.jpg';
Image1=imread(nomimage);
Gris=rgb2gray(Image1);

% figure
% image(Image1)
% figure
% imshow(Gris)
NB=imbinarize(Gris);
NBtest=1-NB;
figure
imshow(NB)
figure
imshow(NBtest)
NB2=imfill(NB,'holes');
NB2bis=imfill(NBtest, 'holes');
figure
imshow(NB2)
figure
imshow(NB2bis)
%%
close all
Igros=bwareaopen(NB2bis,20000);
figure
imshow(Igros);
Ifinal=logical(Igros);
stats=regionprops(Ifinal, 'boundingbox');

% figure
% imshow(Image1);
% hold on;

for cnt = 1 : numel(stats)
    bb = stats(cnt).BoundingBox;
    ratio(cnt)=bb(3)/bb(4);
    aire(cnt)=bb(3)*bb(4);
end
carre=and(ratio>0.7, ratio<1.3);
[val_aire, ind_pgc]=max(carre.*aire);
% rectangle('Position',stats(ind_pgc).BoundingBox,'edgecolor','r')
% Cxmin=ceil(stats(ind_pgc).BoundingBox(1));
% Cxmax=floor(stats(ind_pgc).BoundingBox(1)+stats(ind_pgc).BoundingBox(3));
% Cymin=ceil(stats(ind_pgc).BoundingBox(2));
% Cymax=floor(stats(ind_pgc).BoundingBox(2)+stats(ind_pgc).BoundingBox(4));
Image2=imcrop(Image1, stats(ind_pgc).BoundingBox);
figure
image(Image2)
