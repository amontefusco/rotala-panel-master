
var tmpImg = new Image();
tmpImg.src = "images/ProbeRunning.jpg";
var tmpImg2 = new Image();
tmpImg2.src = "images/MovingRel.jpg";
var tmpImg3 = new Image();
tmpImg3.src = "images/RunningToAbs.jpg";

var host = window.location.host;
var ws = new WebSocket('ws://'+host+'/ws');

var display1;
var display2;
var display3;
var display4;
var display5;
var display6;
var display8;
var display9;
var appoggio;


ws.onopen = function(){
	console.log("Websocket opened");
};

// Gestione messaggi in arrivo da Python

ws.onmessage = function(ev){
	data=JSON.parse(ev.data);
	
	
// *************** DRO Page Displays ****************/

	if (data.target=="display1") {
		display1.setValue(data.value.toFixed(1).padStart(5, " "));
		
	}	
	if (data.target=="display2") {
		display2.setValue(data.value.toFixed(1).padStart(5, " "));

	}	
	if (data.target=="display3") {
		display3.setValue(data.value.toFixed(1).padStart(4, " "));


// *************** Auto Page Displays ****************/
	}
	if (data.target=="display4") {
		display4.setValue(data.value.toFixed(1).padStart(5, " "));
	}
	if (data.target=="display5") {
		display5.setValue(data.value.toFixed(1).padStart(5, " "));
	}
	if (data.target=="display6") {
		display6.setValue(data.value.toFixed(1).padStart(4, " "));
	}
	
// *************** Setup Page Mini Displays ****************/

	if (data.target=="display8") {
		display8.setValue(data.value.toFixed(1).padStart(5, " "));
	}
	if (data.target=="display9") {
		display9.setValue(data.value.toFixed(1).padStart(5, " "));
	}	
	
	
	if (data.target=="abs_incr") {
		$("#abs_incr").text(data.value.toString());
	}	
	if (data.target=="mm_inch") {
		$("#mm_inch").text(data.value.toString());
	}	
	if (data.target=="button_units") {
		$("#button_units").attr("src",data.value.toString());
	}	
	if (data.target=="button_mode") {
		$("#button_mode").attr("src",data.value.toString());
	}
	if (data.target=="button_zero1") {
		$("#button_zero1").attr("src",data.value.toString());
	}	
	if (data.target=="button_zero2") {
		$("#button_zero2").attr("src",data.value.toString());
	}
	if (data.target=="fence_probe") {
		$("#fence_probe").attr("src",data.value.toString());
	}	
	if (data.target=="height_probe") {
		$("#height_probe").attr("src",data.value.toString());
	}	
	if (data.target=="fence_homing") {
		$("#fence_homing").attr("src",data.value.toString());
	}	
	if (data.target=="height_homing") {
		$("#height_homing").attr("src",data.value.toString());
	}	
	if (data.target=="button_zero3") {
		$("#button_zero3").attr("src",data.value.toString());
	}
	if (data.target=="Left") {
		$("#Left").attr("src",data.value.toString());
	}
	if (data.target=="Left2") {
		$("#Left2").attr("src",data.value.toString());
	}	
	if (data.target=="Center") {
		$("#Center").attr("src",data.value.toString());
		// display hold on panel
		if (data.hold == "true") {
			HoldOn.open({
				message: "Motor running, please wait",
				theme: "sk-cube-grid"
			});
		} else {
			HoldOn.close();
		};
	}
	if (data.target=="Center2") {
		$("#Center2").attr("src",data.value.toString());
		// display hold on panel
		if (data.hold == "true") {
			HoldOn.open({
				message: "Motor running, please wait",
				theme: "sk-cube-grid"
			});
		} else {
			HoldOn.close();
		};
	}	
	if (data.target=="Center3") {
		$("#Center3").attr("src",data.value.toString());
		// display hold on panel
		if (data.hold == "true") {
			HoldOn.open({
				message: "Motor running, please wait",
				theme: "sk-cube-grid"
			});
		} else {
			HoldOn.close();
		};
	}
	if (data.target=="Right") {
		$("#Right").attr("src",data.value.toString());
	}
		if (data.target=="Up") {
		$("#Up").attr("src",data.value.toString());
	}	
	if (data.target=="Down") {
		$("#Down").attr("src",data.value.toString());
	}
	if (data.target=="Reboot") {
		$("#Reboot").attr("src",data.value.toString());
	}	
	if (data.target=="Shutdown") {
		$("#Shutdown").attr("src",data.value.toString());
	}	
};

ws.onclose = function(ev){
	console.log("Websocket closed");
};

ws.onerror = function(ev){
	console.log("Websocket error");
};

 	/*-- Display Attributes Control --*/
 
$(document).ready(function() {
	display1 = new SegmentDisplay("display1");

	display1.pattern         = "###.#";
	display1.displayAngle    = 6.5;
	display1.digitHeight     = 32;
	display1.digitWidth      = 17.5;
	display1.digitDistance   = 3.1;
	display1.segmentWidth    = 2.8;
	display1.segmentDistance = 0.4;
	display1.segmentCount    = 7;
	display1.cornerType      = 3;
	display1.colorOn         = "#ff330f";
	display1.colorOff        = "#100505";

	display1.setValue("000.0");


	display2= new SegmentDisplay("display2");

	display2.pattern         = "###.#";
	display2.displayAngle    = 6.5;
	display2.digitHeight     = 32;
	display2.digitWidth      = 17.5;
	display2.digitDistance   = 3.1;
	display2.segmentWidth    = 2.8;
	display2.segmentDistance = 0.4;
	display2.segmentCount    = 7;
	display2.cornerType      = 3;
	display2.colorOn         = "#ff330f";
	display2.colorOff        = "#100505";

	display2.setValue("000.0");
	
	display3= new SegmentDisplay("display3");

	display3.pattern         = "##.#";
	display3.displayAngle    = 6.5;
	display3.digitHeight     = 32;
	display3.digitWidth      = 17.5;
	display3.digitDistance   = 3.1;
	display3.segmentWidth    = 2.8;
	display3.segmentDistance = 0.4;
	display3.segmentCount    = 7;
	display3.cornerType      = 3;
	display3.colorOn         = "#33ee0f";
	display3.colorOff        = "#100505";

	display3.setValue("00.0");
	
	display4= new SegmentDisplay("display4");

	display4.pattern         = "###.#";
	display4.displayAngle    = 6.5;
	display4.digitHeight     = 32;
	display4.digitWidth      = 17.5;
	display4.digitDistance   = 3.1;
	display4.segmentWidth    = 2.8;
	display4.segmentDistance = 0.4;
	display4.segmentCount    = 7;
	display4.cornerType      = 3;
	display4.colorOn         = "#ff330f";
	display4.colorOff        = "#100505";

	display4.setValue("000.0");	

	display5= new SegmentDisplay("display5");

	display5.pattern         = "###.#";
	display5.displayAngle    = 6.5;
	display5.digitHeight     = 32;
	display5.digitWidth      = 17.5;
	display5.digitDistance   = 3.1;
	display5.segmentWidth    = 2.8;
	display5.segmentDistance = 0.4;
	display5.segmentCount    = 7;
	display5.cornerType      = 3;
	display5.colorOn         = "#ff330f";
	display5.colorOff        = "#100505";

	display5.setValue("000.0");
	
	display6= new SegmentDisplay("display6");

	display6.pattern         = "##.#";
	display6.displayAngle    = 6.5;
	display6.digitHeight     = 32;
	display6.digitWidth      = 17.5;
	display6.digitDistance   = 3.1;
	display6.segmentWidth    = 2.8;
	display6.segmentDistance = 0.4;
	display6.segmentCount    = 7;
	display6.cornerType      = 3;
	display6.colorOn         = "#33ee0f";
	display6.colorOff        = "#100505";

	display6.setValue("00.0");
	
	
	display8= new SegmentDisplay("display8");

	display8.pattern         = "###.#";
	display8.displayAngle    = 6.5;
	display8.digitHeight     = 2;
	display8.digitWidth      = 1;
	display8.digitDistance   = 0.2;
	display8.segmentWidth    = 0.1;
	display8.segmentDistance = 0.1;
	display8.segmentCount    = 7;
	display8.cornerType      = 3;
	display8.colorOn         = "#33ee0f";
	display8.colorOff        = "#100505";

	display8.setValue("000.0");
	
	
	display9= new SegmentDisplay("display9");

	display9.pattern         = "###.#";
	display9.displayAngle    = 6.5;
	display9.digitHeight     = 2;
	display9.digitWidth      = 1;
	display9.digitDistance   = 0.2;
	display9.segmentWidth    = 0.1;
	display9.segmentDistance = 0.1;
	display9.segmentCount    = 7;
	display9.cornerType      = 3;
	display9.colorOn         = "#33ee0f";
	display9.colorOff        = "#100505";

	display9.setValue("000.0");
	
	
	
	display7= new SegmentDisplay("display7");

	display7.pattern         = "##:##:##";
	display7.displayAngle    = 6.5;
	display7.digitHeight     = 32;
	display7.digitWidth      = 17.5;
	display7.digitDistance   = 3.1;
	display7.segmentWidth    = 2.8;
	display7.segmentDistance = 0.4;
	display7.segmentCount    = 7;
	display7.cornerType      = 3;
	display7.colorOn         = "#ff330f";
	display7.colorOff        = "#100505";

	display7.setValue('12:34:30');
	

  //window.setInterval('animate()', 100);

  
  function animate() {
    var time    = new Date();
    var hours   = time.getHours();
    var minutes = time.getMinutes();
    var seconds = time.getSeconds();
    var value   = ((hours < 10) ? ' ' : '') + hours
                + ':' + ((minutes < 10) ? '0' : '') + minutes
                + ':' + ((seconds < 10) ? '0' : '') + seconds;
    display7.setValue(value);
  }

 /*
// bring buttons to default status
  $("#Center").attr("src","/images/RunToAbs.jpg");
  $("#Center2").attr("src","/images/RunToAbs.jpg");
  $("#Center3").attr("src","/images/MoveRel.jpg");
 */

/*-- Bottom Buttons --*/
	
	$("#abs_incr").click(function(){
		data={"event":"click","id":"abs_incr", "value" :$("#abs_incr").text()};
		a=JSON.stringify(data);
		ws.send(a);
	});

	$("#mm_inch").click(function(){
		data={"event":"click","id": "mm_inch","value" : $("#mm_inch").text()};
		a=JSON.stringify(data);
		ws.send(a);
	}); 

/*-- Photo Buttons --*/
	
	$("#button_units").click(function(){
		data={"event":"click","id":"button_units", "value" :$("#button_units").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	});

	$("#button_mode").click(function(){
		data={"event":"click","id": "button_mode","value" : $("#button_mode").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	
	$("#button_zero1").click(function(){
		data={"event":"click","id": "button_zero1","value" : $("#button_zero1").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	
	$("#button_zero2").click(function(){
		data={"event":"click","id": "button_zero2","value" : $("#button_zero2").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	
	$("#button_zero3").click(function(){
		alert("Ci sono");
		data={"event":"click","id": "button_zero3","value" : $("#button_zero3").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	});
	
	$("#Left").click(function(){
		data={"event":"click","id": "Left","value" : $("#Left").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	});
	$("#Left2").click(function(){
		data={"event":"click","id": "Left2","value" : $("#Left2").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
/*		$("#Center").click(function(){
		data={"event":"click","id": "Center","value" : $("#Center").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); */
	$("#Right").click(function(){
		data={"event":"click","id": "Right","value" : $("#Right").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	});
	$("#Up").click(function(){
		data={"event":"click","id": "Up","value" : $("#Up").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	
	$("#Down").click(function(){
		data={"event":"click","id": "Down","value" : $("#Down").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	});
	
/*-- ********************** Motion Buttons *********************** --*/
	
	$("#Center").click(function(){
		//alert("Ci sono");
		data={"event":"setup","id":"fence", "value" :$("#FenceInput").val()};
		a=JSON.stringify(data);
		ws.send(a);
	});
	
	$("#Center2").click(function(){
		//alert("Ci sono");
		data={"event":"setup","id":"height", "value" :$("#HeightInput").val()};
		a=JSON.stringify(data);
		ws.send(a);
	});
	$("#Center3").click(function(){
		//alert("Ci sono");
		data={"event":"setup","id":"relativeFence", "value" :$("#FenceInput").val()};
		a=JSON.stringify(data);
		ws.send(a);
	});
	$("#Center4").click(function(){
		//alert("Ci sono");
		data={"event":"setup","id":"relativeHeight", "value" :$("#HeightInput").val()};
		a=JSON.stringify(data);
		ws.send(a);
	});
	
	
	/*-- ********************** Probe Buttons *********************** --*/
	
	$("#fence_probe").click(function(){
		data={"event":"click","id": "fence_probe","value" : $("#fence_probe").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	$("#height_probe").click(function(){
		data={"event":"click","id": "height_probe","value" : $("#height_probe").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	});

	
	/*-- ********************** Home Buttons *********************** --*/
	
	$("#fence_homing").click(function(){
		data={"event":"click","id": "fence_homing","value" : $("#fence_homing").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	$("#height_homing").click(function(){
		//alert("Ci sono");
		data={"event":"click","id": "height_homing","value" : $("#height_homing").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	});

	/*-- ********************** Power Buttons *********************** --*/

	$("#powerOff").click(function(){
		//alert("Ci sono");
		data={"event":"click","id":"Shutdown", "value" :$("#powerOff").val()};
		a=JSON.stringify(data);
		ws.send(a);
	});	
	$("#reboot").click(function(){
		//alert("Ci sono");
		data={"event":"click","id":"Reboot", "value" :$("#reboot").val()};
		a=JSON.stringify(data);
		ws.send(a);
	});	
});
