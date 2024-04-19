var exec = require('child_process').exec;
hexo.on('new', function(data){
exec('start  "D:\software_install\Typora\Typora.exe" ' + `"${data.path}"`);
}); 