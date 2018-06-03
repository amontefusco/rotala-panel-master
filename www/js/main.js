var host = window.location.host;
var ws = new WebSocket('ws://'+host+'/ws');

var display1;
var display2;
var display3;

ws.onopen = function(){
	console.log("Websocket opened");
};

// Gestione messaggi in arrivo da Python

ws.onmessage = function(ev){
	data=JSON.parse(ev.data);
	
	if (data.target=="display1") {
		display1.setValue(data.value.toString());
	}	
	if (data.target=="display2") {
		display2.setValue(data.value.toString());
	}	
	if (data.target=="display3") {
		display3.setValue(data.value.toString());
	}
	if (data.target=="display4") {
		display4.setValue(data.value.toString());
	}	
	if (data.target=="display2") {
		display5.setValue(data.value.toString());
	}	
	if (data.target=="display3") {
		display6.setValue(data.value.toString());
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
		$("#button_mode").attr("src",data.value.toString());
	}	
	if (data.target=="button_zero2") {
		$("#button_mode").attr("src",data.value.toString());
	}	
	if (data.target=="button_zero3") {
		$("#button_mode").attr("src",data.value.toString());
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
	display1.colorOff        = "#101515";

	display1.setValue("0");


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

	display2.setValue("0");
	
	display3= new SegmentDisplay("display3");

	display3.pattern         = "###.#";
	display3.displayAngle    = 6.5;
	display3.digitHeight     = 32;
	display3.digitWidth      = 17.5;
	display3.digitDistance   = 3.1;
	display3.segmentWidth    = 2.8;
	display3.segmentDistance = 0.4;
	display3.segmentCount    = 7;
	display3.cornerType      = 3;
	display3.colorOn         = "#ff330f";
	display3.colorOff        = "#100505";

	display3.setValue("0");
	
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

	display4.setValue("0");	

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

	display5.setValue("0");
	
	display6= new SegmentDisplay("display6");

	display6.pattern         = "###.#";
	display6.displayAngle    = 6.5;
	display6.digitHeight     = 32;
	display6.digitWidth      = 17.5;
	display6.digitDistance   = 3.1;
	display6.segmentWidth    = 2.8;
	display6.segmentDistance = 0.4;
	display6.segmentCount    = 7;
	display6.cornerType      = 3;
	display6.colorOn         = "#ff330f";
	display6.colorOff        = "#100505";

	display6.setValue("0");	
	
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
		data={"event":"click","id": "button_mode","value" : $("#button_zero1").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	
	$("#button_zero2").click(function(){
		data={"event":"click","id": "button_mode","value" : $("#button_zero2").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 
	
	$("#button_zero3").click(function(){
		data={"event":"click","id": "button_mode","value" : $("#button_zero3").attr("src")};
		a=JSON.stringify(data);
		ws.send(a);
	}); 	
});
