"use strict";

var VPU = {
    WIREFRAME   : true,
	cbuffer  	: undefined,
	pbuffer  	: undefined,
    wbuffer 	: undefined,
    context     : undefined,
    canvas      : undefined,
    cbuffer_data: undefined,
    pbuffer_data: undefined,
    wbuffer_data: undefined,

    init  : function(){
        VPU.canvas = document.getElementById('canvas');
        VPU.context = VPU.canvas.getContext('2d');
        VPU.cbuffer = VPU.context.createImageData(Swarm.width, Swarm.height);
        VPU.pbuffer = VPU.context.createImageData(Swarm.width, Swarm.height);
        VPU.wbuffer = VPU.context.createImageData(Swarm.width, Swarm.height);
        VPU.cbuffer_data = VPU.cbuffer.data;
        VPU.pbuffer_data = VPU.pbuffer.data;
        VPU.wbuffer_data = VPU.wbuffer.data;
    },

	pset	 	: function(x,y,color){
        // Draw to pbuffer
        x = parseInt(x);
        y = parseInt(y);
        var pos = (((y*(Swarm.width*4))) + (x*4));
        VPU.pbuffer_data[pos+0] = parseInt(color[0]);
        VPU.pbuffer_data[pos+1] = parseInt(color[1]);
        VPU.pbuffer_data[pos+2] = parseInt(color[2]);
        VPU.pbuffer_data[pos+3] = 255;
    },

    clear   : function(){
        for(var i=0; i<Swarm.width*Swarm.height*4;i+=4){
            VPU.pbuffer_data[i]=0;
            VPU.pbuffer_data[i+1]=0;
            VPU.pbuffer_data[i+2]=0;
            VPU.pbuffer_data[i+3]=0;
        }
    },
    
	wset	 	: function(x,y){
		// Draw to wbuffer
	},

    line        : function(X1,Y1,X2,Y2,color){
        // Calculate "deltas" of the line (difference between two ending points)
        var dx = X2 - X1;
        var dy = Y2 - Y1;

        // Calculate the line equation based on deltas
        var D = (2 * dy) - dx;
        var y = Y1;

        // Draw the line based on arguments provided
        for(var x=X1; x<X2;x++){
        
            // Draw pixel at this location
            VPU.pset(x,y,color);

            // Progress the line drawing algorithm parameters
            if(D > 0){
                y = y + 1;
                D = D - 2*dx;
            }
            D = D + 2*dy;
        }
    },

    polygon     : function(pair_count, vertices, color){
        var lx = vertices[0];
        var ly = vertices[1];        
        var ix = lx;
        var iy = ly;
        for(var i = 0; i<pair_count*2; i+=2){
            var x = vertices[i];
            var y = vertices[i+1];
            VPU.line(lx,ly,x,y,color);
            lx = x;
            ly = y;
        }
        VPU.line(lx,ly,ix,iy,color);
        
    },

	cool		: function(){
		// Cool warmmap
	},

	squash		: function(){
		// Draw all buffers as layers to cbuffer
	},

	render		: function(){
        VPU.context=document.getElementById('canvas').getContext('2d');
        VPU.context.putImageData(VPU.pbuffer, 0, 0);
        VPU.cbuffer_data = VPU.cbuffer.data;
        VPU.pbuffer_data = VPU.pbuffer.data;
        VPU.wbuffer_data = VPU.wbuffer.data;
    },
    
};

