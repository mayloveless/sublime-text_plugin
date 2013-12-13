#-*- coding: UTF-8 -*-  
import sublime, sublime_plugin
import os
import time
import os.path

plIndex = '''
/**
*@id: 
*@author  @mayloveless
*@date:  %s
*/
$Import('%s.source.init');
STK.pageletM.register("%s.index", function($) {

        var PL_HTML_ID = '%s';

        var node = $.E(PL_HTML_ID);
        var item = $.%s.source.init({
                'node'   : node
        });
        var that = {};
        
        that.destroy = function(){
                item.destroy();
        }
        return that;
});
'''

plInit = '''
/**
*@id: 
*@author @mayloveless
*@date:  %s
*/
$Import('kit.dom.parseDOM');
$Import('kit.extra.language');
$Import('ui.alert');

STK.pageletM.register("%s.init", function($) {
    var $L = $.kit.extra.language;

    return function(spec){
        var that = {}, delegate, domList;

        var prepare = function(){
            domList = $.kit.dom.parseDOM($.builder(spec.node).list);
            console.log(domList);
        };

        var build = function(){

        };

        var bind = function(){

        };

        var init = function(){
            prepare();
            build();
            bind();
        };
                
        var destroy = function(){
                    
        };
        
        init();

        that.destroy = destroy;

        return that;
    };
});
'''

class PlpackageCommand(sublime_plugin.WindowCommand):
        plName = ''
        saveAddress = ''
        parentDir = ''
        def run(self,dirs):
                fname = ''
                self.saveAddress = dirs[0]
                def done(commands):
                        cs = commands.split(',')
                        if not cs:
                                return
                        if len(cs) == 1:
                                self.plName = cs[0]
                        if len(cs) == 2:
                                self.plName = cs[0]
                                self.parentDir = cs[1]
                        
                        #make folder
                        packagePath  = os.path.join(self.saveAddress, self.plName)
                        os.makedirs(packagePath)
                        
                        #pl index.js
                        if self.parentDir : 
                            nameSpace ='pl.'+self.parentDir+'.'+ os.path.basename(self.saveAddress)+'.'+self.plName
                        else :
                            nameSpace ='pl.'+os.path.basename(self.saveAddress)+'.'+self.plName
                        plId = '_'.join(nameSpace.split('.')) 
                        now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                        plIndexContent = plIndex % (now,nameSpace,nameSpace,plId,nameSpace)
                        f = open(packagePath+'/'+'index.js','w') 
                        f.write(plIndexContent)
                        f.close()

                        #make source folder
                        sourcePath = packagePath+'/source'
                        os.makedirs(sourcePath)

                        #make init.js
                        plInitContent = plInit % (now,nameSpace+'.source')
                        f = open(sourcePath+'/'+'init.js','w') 
                        f.write(plInitContent)
                        f.close()
                       
                self.window.show_input_panel("Input the pl Name:", fname, done, None, None)