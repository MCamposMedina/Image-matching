
// This macro chops an image into NxN tiles, where N is the number
// of divisions chosen by the user.
dir = getDir("##########"); // directory that contains the folders with the input files

target="ROI/"; // The specific folder to convert
images_names="Tiling/"
list_ROIs = getFileList(dir + target); // get the names of the subfolders contained in the target folder
list_images = getFileList(dir + images_names); // get the names of the subfolders contained in the target folder
N = list_ROIs.length;

for (J = 0; J < N; J++) {

	print(list_images[J]);
	print(list_ROIs[J]);
	ss = list_images[J];
	new_name = replace(ss,".tif","");
	
	newImage(new_name, "8-bit black", 1230, 1230, 1);
	roiManager("Open", dir+target+list_ROIs[J]);
	

	
	
	//RoiManager.getRoiManager().close();
	n=roiManager("count");
	for (i = 0; i < n ; i++) {
	
		roiManager("Select", i);
		run("Add...", "value=254");
	
	}
	roiManager("Deselect")
	close("ROI Manager");
	
//	roiManager_m.close();
	saveAs("Tiff", dir  + "Results_ROI/" +new_name); // saves images to the directory "Results" at the desktop
	close('*');
}