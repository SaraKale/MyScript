/********************************
	打开每个AI文件并导出为PNG
	
	使用方法：
	打开Illustrator，在文件——脚本——其他脚本，选择.jsx脚本即可，它就会自动处理了。
	注意文件路径末尾要加/，否则会导出到上一层文件夹
*********************************/

var folderPath = "C:/脚本/int/"; // 输入ai文件路径
var exportPath = "C:/脚本/out/"; // 导出PNG的路径
var resolution = 300; // 分辨率设置为300dpi，选项：屏幕72dpi，中150dpi，高300dpi

var files = Folder(folderPath).getFiles("*.ai");

for (var i = 0; i < files.length; i++) {
    var doc = app.open(files[i]);
    
    // 获取文档的画板
    var artboards = doc.artboards;
    
    for (var j = 0; j < artboards.length; j++) {
        // 设置活动画板
        doc.artboards.setActiveArtboardIndex(j);
        
        // 导出为PNG
        var exportOptions = new ExportOptionsPNG24();
        exportOptions.horizontalScale = resolution;
		exportOptions.verticalScale = resolution;
        exportOptions.transparency = true; //包含透明通道
        
		//导出文件路径
        var exportFile = new File(exportPath + doc.name.replace(/\.ai$/, "_artboard" + (j + 1) + ".png"));
        doc.exportFile(exportFile, ExportType.PNG24, exportOptions);
    }
    
    doc.close(SaveOptions.DONOTSAVECHANGES);
}

alert("导出完成！");
