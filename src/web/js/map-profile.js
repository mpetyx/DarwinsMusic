function getUrlVars() {
	var vars = {};
	var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
		vars[key] = value;
	});
	return vars;
}
			
var gid = 0;
if ((getUrlVars()["gid"]) == "1") gid=1; else gid=0;

var db = "data/jazz.json";
if (gid == "1") db = "data/rock.json";

$(function(){
	$.getJSON(db, function(data){
		var val = 2000;
		
		aggregatedHitsValues = jvm.values.apply({}, jvm.values(data.total_hits)),
		hitsValues = Array.prototype.concat.apply([], jvm.values(data.hits));
		uniqueValues = Array.prototype.concat.apply([], jvm.values(data.viewers));
		//aggregatedHitsValues = Array.prototype.concat.apply([], jvm.values(data.total_hits));
		
		$('#music_map').vectorMap({
			map: 'world_mill_en',
			markers: data.coords,
			series: {
				markers: [{
					attribute: 'fill',
					scale: ['#FEE5D9', '#A50F15'],
					values: data.hits[val],
					min: jvm.min(hitsValues),
					max: jvm.max(hitsValues)
					},{
					attribute: 'r',
					scale: [0, 20],
					values: data.viewers[val],
					min: jvm.min(uniqueValues),
					max: jvm.max(uniqueValues)
				}],
				regions: [{
					scale: ['#DEEBF7', '#08519C'],
					attribute: 'fill',
					values: data.total_hits[val],
					min: jvm.min(aggregatedHitsValues),
					max: jvm.max(aggregatedHitsValues)
				}]
			},
			
			onMarkerLabelShow: function(event, label, index){
				label.html(
					''+data.names[index]+'<br/>'+ 
					'Number of hits: '+data.hits[val][index]+'<br/>'+
					'Number of listeners: '+data.viewers[val][index]
				);
			},
			
			onRegionLabelShow: function(event, label, code){
				label.html(
					''+label.html()+'<br/>'+
					'Number of hits: '+data.total_hits[val][code]
				);
			}
		});
		
		var mapObject = $('#music_map ').vectorMap('get', 'mapObject');
					
		$("#slider").slider({
			value: val,
			min: 1960, //data[0][0],
			max: 2010, //data[data.length-1][0],
			step: 10,
			
			slide: function( event, ui ) {
				val = ui.value;
				mapObject.series.regions[0].setValues(data.country_names[ui.value]);
				mapObject.series.markers[0].setValues(data.hits[ui.value]);
				mapObject.series.markers[1].setValues(data.viewers[ui.value]);
			}
		})
		.each(function() {
			var opt = $(this).data().uiSlider.options;
			var vals = opt.max -  opt.min;
			
			for(var i = 0; i <= vals; i=i+10) {
				var el = $('<label>'+(i+opt.min)+'</label>').css('left', (i/vals*100)+'%');
				$('#slider').append(el);
			}
		});
	});
});
